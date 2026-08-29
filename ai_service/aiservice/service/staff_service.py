'''
人工客服服务
============
职责: 客服登录 / 会话列表 / 人工接管 / 回复(实时推送访客) / 关闭会话
      / 统计报表 / 知识库管理。

认证设计说明: 登录成功后客户端在请求头 X-Staff-Id 携带客服 id,
服务端按 id 校验身份 —— 这是"演示级"方案, 生产环境应使用 JWT,
后续课程(Redis 阶段)可升级为 token + Redis 会话 (见 docs/02 演进路线)。
'''
import hashlib

from aiservice.common.config import Config
from aiservice.common.constants import MessageRole, MessageSource, SessionStatus, WsType
from aiservice.common.exceptions import AuthError, NoPermissionError, NotFoundError, ParamError
from aiservice.common.logger import get_logger
from aiservice.dao.knowledge_dao import KnowledgeDao
from aiservice.dao.message_dao import MessageDao
from aiservice.dao.session_dao import SessionDao
from aiservice.dao.staff_dao import StaffDao
from aiservice.service.ws_manager import WsManager


class StaffService:
    def __init__(self):
        self._config = Config.instance()
        self._logger = get_logger(__name__)
        self._staff_dao = StaffDao()
        self._session_dao = SessionDao()
        self._message_dao = MessageDao()
        self._knowledge_dao = KnowledgeDao()
        self._ws_manager = WsManager.instance()

    # ---------------- 登录认证 ----------------

    def login(self, username: str, password: str) -> dict:
        """客服登录: 校验 SHA256(盐+密码) 哈希"""
        staff = self._staff_dao.get_by_username(username)
        if staff is None or not self._verify_password(password, staff['password_hash']):
            raise AuthError('用户名或密码错误')
        self._logger.info(f'客服登录成功: {username}')
        return {'id': staff['id'], 'username': staff['username'],
                'display_name': staff['display_name']}

    def get_staff(self, staff_id: int) -> dict:
        """按 id 校验客服身份 (请求头 X-Staff-Id)"""
        staff = self._staff_dao.get_by_id(staff_id)
        if staff is None:
            raise AuthError('客服身份无效, 请重新登录')
        return {'id': staff['id'], 'username': staff['username'],
                'display_name': staff['display_name']}

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """SHA256(盐 + 明文) 与库中哈希比对"""
        salt = str(self._config.get('staff.password_salt', ''))
        digest = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return digest == password_hash

    # ---------------- 会话管理 ----------------

    def list_sessions(self, status: str) -> list[dict]:
        """按状态查询会话列表"""
        valid = (SessionStatus.BOT, SessionStatus.WAITING_HUMAN,
                 SessionStatus.HUMAN, SessionStatus.CLOSED)
        if status not in valid:
            raise ParamError(f'无效的会话状态: {status}')
        return self._session_dao.list_by_status(status)

    def takeover(self, session_id: int) -> None:
        """人工接管会话: waiting_human -> human"""
        session = self._require_session(session_id)
        if session['status'] not in (SessionStatus.WAITING_HUMAN, SessionStatus.BOT):
            raise ParamError(f'会话当前状态为 {session["status"]}, 无法接管')
        self._session_dao.update_status(session_id, SessionStatus.HUMAN)
        self._logger.info(f'客服接管会话: {session_id}')

    def messages_after(self, session_id: int, after_id: int) -> list[dict]:
        """查询增量消息 (工作台轮询用)"""
        self._require_session(session_id)
        return self._message_dao.list_after_id(session_id, after_id)

    def reply_prepare(self, session_id: int, content: str) -> dict:
        """回复的阻塞部分: 校验会话状态 -> 消息入库 (运行在线程池中)"""
        session = self._require_session(session_id)
        if session['status'] != SessionStatus.HUMAN:
            raise NoPermissionError('请先接管会话, 再回复消息')
        message_id = self._message_dao.add(session_id, MessageRole.STAFF, content, MessageSource.HUMAN)
        self._session_dao.touch(session_id)
        self._logger.info(f'客服回复会话 {session_id}: "{content[:20]}"')
        return {'id': message_id, 'session_id': session_id, 'role': MessageRole.STAFF,
                'content': content, 'source': MessageSource.HUMAN, 'rating': None}

    async def push_staff_reply(self, session_id: int, message: dict) -> None:
        """回复的异步部分: 实时推送给访客的 WebSocket (访客无需轮询)"""
        await self._ws_manager.send_to_session(session_id, {
            'type': WsType.STAFF_REPLY, 'message': message})

    def close_session(self, session_id: int) -> None:
        """关闭会话"""
        self._require_session(session_id)
        self._session_dao.close(session_id)
        self._logger.info(f'客服关闭会话: {session_id}')

    # ---------------- 统计报表 ----------------

    def stats(self) -> dict:
        """运营统计: 会话量/消息量/机器人命中率/满意度"""
        status_counts = {row['status']: row['cnt'] for row in self._session_dao.count_by_status()}
        bot = self._message_dao.bot_stats()
        bot_total = bot['bot_total'] or 0
        knowledge_hits = bot['knowledge_hits'] or 0
        return {
            'session_total': sum(status_counts.values()),
            'session_by_status': status_counts,
            'message_today': self._message_dao.count_today(),
            'bot_answer_total': bot_total,
            'bot_hit_rate': round(knowledge_hits / bot_total, 4) if bot_total else 0.0,
            'rating_count': bot['rated_count'] or 0,
            'avg_rating': round(float(bot['avg_rating']), 2) if bot['avg_rating'] is not None else None,
        }

    # ---------------- 知识库管理 ----------------

    def list_knowledge(self) -> list[dict]:
        return self._knowledge_dao.list_all()

    def add_knowledge(self, category: str, question: str, keywords: str, answer: str) -> int:
        knowledge_id = self._knowledge_dao.add(category, question, keywords, answer)
        self._logger.info(f'新增知识条目: id={knowledge_id} 问题="{question}"')
        return knowledge_id

    def update_knowledge(self, knowledge_id: int, fields: dict) -> None:
        if self._knowledge_dao.update(knowledge_id, fields) == 0:
            raise NotFoundError('知识条目不存在')
        self._logger.info(f'更新知识条目: id={knowledge_id}')

    def delete_knowledge(self, knowledge_id: int) -> None:
        if self._knowledge_dao.delete(knowledge_id) == 0:
            raise NotFoundError('知识条目不存在')
        self._logger.info(f'删除知识条目: id={knowledge_id}')

    # ---------------- 内部工具 ----------------

    def _require_session(self, session_id: int) -> dict:
        session = self._session_dao.get(session_id)
        if session is None:
            raise NotFoundError('会话不存在')
        return session
