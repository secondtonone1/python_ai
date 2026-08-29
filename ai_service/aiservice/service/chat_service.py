'''
访客侧聊天服务 (编排层)
=======================
职责: 编排"限流 -> 会话 -> 消息入库 -> AI引擎 -> 流式输出 -> 转人工"的完整链路。

协程 + 线程池的设计 (对应课程 73-83 协程、88 工业级协程服务):
- 数据库操作与规则引擎计算是阻塞代码, 放到 run_in_executor 交给线程池执行
- 事件循环只负责"分片发送 + 节奏控制", 不会被阻塞代码卡住
'''
import asyncio
import threading
from dataclasses import dataclass

from aiservice.common.config import Config
from aiservice.common.constants import MessageRole, MessageSource, SessionStatus, WsType
from aiservice.common.exceptions import NotFoundError, ParamError
from aiservice.common.logger import get_logger
from aiservice.dao.knowledge_dao import KnowledgeDao
from aiservice.dao.message_dao import MessageDao
from aiservice.dao.session_dao import SessionDao
from aiservice.service.bot_engine import RuleEngine, split_answer
from aiservice.service.rate_limiter import RateLimiter
from aiservice.service.ws_manager import WsManager


@dataclass
class _ChatResult:
    """一次聊天处理(阻塞部分)的结果"""
    ok: bool = True
    error: dict | None = None             # 失败时: {'type', 'code', 'message'}
    session_status: str = ''              # 会话当前状态
    answer: str = ''                      # 机器人回答全文
    bot_message: dict | None = None       # 已入库的机器人消息
    need_human: bool = False              # 是否转人工


class ChatService:
    def __init__(self):
        self._config = Config.instance()
        self._logger = get_logger(__name__)
        self._session_dao = SessionDao()
        self._message_dao = MessageDao()
        self._knowledge_dao = KnowledgeDao()
        self._engine = RuleEngine(
            fallback_message=str(self._config.get('bot.fallback_message')),
            pending_prompt=str(self._config.get('bot.pending_prompt')),
        )
        self._ws_manager = WsManager.instance()
        # 限流器: 聊天消息每会话限流
        self._chat_limiter = RateLimiter(
            int(self._config.get('rate_limit.chat_per_minute', 20)), 60.0)
        # 限流器: 创建会话每 IP 限流 (防刷)
        self._session_limiter = RateLimiter(
            int(self._config.get('rate_limit.session_per_minute', 10)), 60.0)
        # 追问状态(内存): session_id -> 上轮追问选项; 服务重启即丢失, 属可接受的简化
        self._pending: dict[int, list[dict]] = {}
        self._pending_lock = threading.RLock()
        self._stream_delay = float(self._config.get('bot.stream_chunk_delay', 0.05))
        self._chunk_size = int(self._config.get('bot.stream_chunk_size', 8))

    # ---------------- REST 接口支撑 ----------------

    def create_session(self, visitor_name: str | None, client_ip: str) -> dict:
        """创建会话 (带 IP 限流)"""
        allowed, retry_after = self._session_limiter.allow(client_ip)
        if not allowed:
            from aiservice.common.exceptions import RateLimitError
            raise RateLimitError(f'操作过于频繁, 请 {retry_after}s 后再试', retry_after)
        session_id = self._session_dao.create(visitor_name or '访客')
        self._logger.info(f'创建会话: id={session_id} 访客={visitor_name or "访客"} ip={client_ip}')
        return self._session_dao.get(session_id)

    def history(self, session_id: int) -> list[dict]:
        """查询会话历史消息"""
        self._require_session(session_id)
        return self._message_dao.list_by_session(session_id)

    def rate_message(self, message_id: int, rating: int) -> None:
        """满意度评价"""
        if self._message_dao.rate(message_id, rating) == 0:
            raise NotFoundError('消息不存在或不可评价')
        self._logger.info(f'消息 {message_id} 收到评价: {rating}')

    # ---------------- WebSocket 聊天处理 ----------------

    async def handle_chat(self, session_id: int, websocket, content: str) -> None:
        """处理一条 WebSocket 聊天消息 (核心编排)

        流程: 限流 -> 会话校验 -> 存用户消息 -> 状态分流
              -> (机器人) 引擎计算 -> 流式分片推送 -> 存机器人消息 -> 必要时转人工
        """
        # 阻塞部分(限流/数据库/引擎计算)整体交给线程池, 不阻塞事件循环
        loop = asyncio.get_running_loop()
        result: _ChatResult = await loop.run_in_executor(
            None, self._process_chat, session_id, content)

        if not result.ok:
            await websocket.send_json(result.error)
            return
        if result.session_status == SessionStatus.HUMAN:
            # 人工接管中: 用户消息已入库, 客服端通过轮询可见, 提示访客即可
            await websocket.send_json({'type': WsType.SESSION_STATUS, 'status': SessionStatus.HUMAN})
            return
        # 机器人流式输出 (模拟大模型 token 流)
        for chunk in split_answer(result.answer, self._chunk_size):
            await websocket.send_json({'type': WsType.CHUNK, 'delta': chunk})
            await asyncio.sleep(self._stream_delay)
        await websocket.send_json({'type': WsType.MESSAGE_END, 'message': result.bot_message})
        if result.need_human:
            await websocket.send_json({'type': WsType.SESSION_STATUS, 'status': SessionStatus.WAITING_HUMAN})

    def _process_chat(self, session_id: int, content: str) -> _ChatResult:
        """聊天处理的阻塞部分 (运行在线程池中): 限流/校验/入库/引擎计算"""
        content = (content or '').strip()
        if not content:
            return _ChatResult(ok=False, error={
                'type': WsType.ERROR, 'code': 400, 'message': '消息内容不能为空'})

        # 1. 限流 (按会话)
        allowed, retry_after = self._chat_limiter.allow(f'session:{session_id}')
        if not allowed:
            return _ChatResult(ok=False, error={
                'type': WsType.ERROR, 'code': 429,
                'message': f'发送过于频繁, 请 {retry_after}s 后再试'})

        # 2. 会话校验
        session = self._session_dao.get(session_id)
        if session is None:
            return _ChatResult(ok=False, error={
                'type': WsType.ERROR, 'code': 404, 'message': '会话不存在'})
        # 已关闭/已归档的会话不接受新消息
        if session['status'] in (SessionStatus.CLOSED, SessionStatus.ARCHIVED):
            return _ChatResult(ok=False, error={
                'type': WsType.ERROR, 'code': 400,
                'message': '会话已结束, 请刷新页面创建新会话'})

        # 3. 用户消息入库 + 刷新会话活动时间
        self._message_dao.add(session_id, MessageRole.USER, content)
        self._session_dao.touch(session_id)

        # 4. 状态分流: 人工接管中的会话, 消息留给客服(客服端轮询可见)
        if session['status'] == SessionStatus.HUMAN:
            return _ChatResult(ok=True, session_status=SessionStatus.HUMAN)

        # 5. 机器人接待: 取追问上下文 -> 引擎计算
        pending = self._get_pending(session_id)
        reply = self._engine.reply(content, self._knowledge_dao.list_enabled(), pending)
        self._save_pending(session_id, reply.pending)
        if reply.knowledge_id:
            self._knowledge_dao.hit_increment(reply.knowledge_id)

        # 6. 机器人消息入库
        bot_message_id = self._message_dao.add(session_id, MessageRole.BOT, reply.answer, reply.source)
        bot_message = {
            'id': bot_message_id, 'session_id': session_id,
            'role': MessageRole.BOT, 'content': reply.answer,
            'source': reply.source, 'rating': None,
        }
        if reply.source == MessageSource.KNOWLEDGE:
            self._logger.info(f'会话 {session_id} 知识库命中: id={reply.knowledge_id} 问题="{content[:20]}"')
        else:
            self._logger.info(f'会话 {session_id} 机器人未命中, 转人工 (问题="{content[:20]}")')

        # 7. 转人工状态落库
        if reply.need_human:
            self._session_dao.update_status(session_id, SessionStatus.WAITING_HUMAN)

        return _ChatResult(ok=True, answer=reply.answer, bot_message=bot_message,
                           need_human=reply.need_human)

    # ---------------- 内部工具 ----------------

    def _require_session(self, session_id: int) -> None:
        if self._session_dao.get(session_id) is None:
            raise NotFoundError('会话不存在')

    def _get_pending(self, session_id: int) -> list[dict] | None:
        with self._pending_lock:
            return self._pending.get(session_id)

    def _save_pending(self, session_id: int, pending: list[dict] | None) -> None:
        with self._pending_lock:
            if pending:
                self._pending[session_id] = pending
            else:
                self._pending.pop(session_id, None)
