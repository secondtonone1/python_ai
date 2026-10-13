'''
客服 REST 接口
==============
- 同步 def 端点: FastAPI 自动放进线程池 (纯数据库操作)
- async def 端点: 需要 await WebSocket 推送 (takeover/close/reply)
  —— 阻塞的数据库部分仍 run_in_executor, 推送只发生在事件循环上
'''
import asyncio

from fastapi import APIRouter, Depends, Query

from aiservice.api.deps import get_staff, ok
from aiservice.common.constants import SessionStatus
from aiservice.schema.models import (ApiResponse, KnowledgeCreateRequest,
                                     KnowledgeUpdateRequest, PolishRequest,
                                     StaffLoginRequest, StaffReplyRequest)
from aiservice.service.staff_service import StaffService

router = APIRouter(prefix='/api/staff', tags=['客服接口'])
_staff_service = StaffService()


# ---------------- 登录 ----------------

@router.post('/login', response_model=ApiResponse, summary='客服登录')
def login(req: StaffLoginRequest):
    """登录成功返回客服信息, 前端保存 id 并在请求头 X-Staff-Id 携带"""
    return ok(_staff_service.login(req.username, req.password))


# ---------------- 会话管理 ----------------

@router.get('/sessions', response_model=ApiResponse, summary='会话列表')
def list_sessions(status: str = Query(default='waiting_human', description='会话状态'),
                  staff: dict = Depends(get_staff)):
    """按状态查询会话: bot / waiting_human / human / closed
    (登录/切换状态/断线重连时全量拉取用; 平时列表由 WebSocket 推送增量维护)
    """
    return ok(_staff_service.list_sessions(status))


@router.post('/sessions/{session_id}/takeover', response_model=ApiResponse, summary='人工接管')
async def takeover(session_id: int, staff: dict = Depends(get_staff)):
    """接管会话: waiting_human -> human; 变更结果实时推送访客与所有工作台"""
    loop = asyncio.get_running_loop()
    session = await loop.run_in_executor(None, _staff_service.takeover, session_id)
    await _staff_service.push_session_update(session)                      # 工作台列表
    await _staff_service.push_visitor_status(session_id, SessionStatus.HUMAN)  # 访客提示
    return ok({'session_id': session_id, 'status': SessionStatus.HUMAN})


@router.get('/sessions/{session_id}/messages', response_model=ApiResponse, summary='增量消息')
def session_messages(session_id: int,
                     after_id: int = Query(default=0, description='只取 id 大于该值的消息'),
                     staff: dict = Depends(get_staff)):
    """增量查询消息 (工作台打开会话拉历史 / 断线重连后补齐推送间隙用)"""
    return ok(_staff_service.messages_after(session_id, after_id))


@router.post('/sessions/{session_id}/reply', response_model=ApiResponse, summary='回复访客')
async def reply(session_id: int, req: StaffReplyRequest, staff: dict = Depends(get_staff)):
    """回复访客: 入库(线程池) + 推送访客 WebSocket + 推送全部工作台"""
    loop = asyncio.get_running_loop()
    message = await loop.run_in_executor(
        None, _staff_service.reply_prepare, session_id, req.content)
    # 访客页面实时收到 (现有通道)
    await _staff_service.push_staff_reply(session_id, message)
    # 工作台实时看到: 新消息 + 会话信息变更 (本咨询师与其他在线咨询师)
    await _staff_service.push_message_update(message)
    session = await loop.run_in_executor(None, _staff_service.get_session, session_id)
    await _staff_service.push_session_update(session)
    return ok(message)


@router.post('/sessions/{session_id}/polish', response_model=ApiResponse,
             summary='AI 检索润色 (咨询师助手)')
def polish(session_id: int, req: PolishRequest | None = None,
           staff: dict = Depends(get_staff)):
    """AI 检索润色 (需已接入会话):
    - req 为空或 req.content 为空 -> 根据来访者最近消息 + 知识库检索, 生成新回复草稿;
    - req.content 非空 -> 润色这段"咨询师已写草稿"。
    未配置大模型时自动降级内置润色; 返回 data.mode = generate|polish。
    """
    content = req.content if req is not None else None
    return ok(_staff_service.polish_draft(session_id, content))


@router.post('/sessions/{session_id}/close', response_model=ApiResponse, summary='关闭会话')
async def close_session(session_id: int, staff: dict = Depends(get_staff)):
    """关闭会话; 变更结果实时推送访客与所有工作台"""
    loop = asyncio.get_running_loop()
    session = await loop.run_in_executor(None, _staff_service.close_session, session_id)
    await _staff_service.push_session_update(session)                       # 工作台列表
    await _staff_service.push_visitor_status(session_id, SessionStatus.CLOSED)  # 访客提示
    return ok({'session_id': session_id, 'status': SessionStatus.CLOSED})


# ---------------- 统计报表 ----------------

@router.get('/stats', response_model=ApiResponse, summary='运营统计')
def stats(staff: dict = Depends(get_staff)):
    """会话量 / 消息量 / 机器人命中率 / 满意度"""
    return ok(_staff_service.stats())


# ---------------- 知识库管理 ----------------

@router.get('/knowledge', response_model=ApiResponse, summary='知识库列表')
def list_knowledge(staff: dict = Depends(get_staff)):
    return ok(_staff_service.list_knowledge())


@router.post('/knowledge', response_model=ApiResponse, summary='新增知识')
def add_knowledge(req: KnowledgeCreateRequest, staff: dict = Depends(get_staff)):
    knowledge_id = _staff_service.add_knowledge(
        req.category, req.question, req.keywords, req.answer)
    return ok({'knowledge_id': knowledge_id})


@router.put('/knowledge/{knowledge_id}', response_model=ApiResponse, summary='更新知识')
def update_knowledge(knowledge_id: int, req: KnowledgeUpdateRequest,
                     staff: dict = Depends(get_staff)):
    """只更新传入的字段 (None 的字段不更新)"""
    fields = {k: v for k, v in req.model_dump().items() if v is not None}
    _staff_service.update_knowledge(knowledge_id, fields)
    return ok({'knowledge_id': knowledge_id})


@router.delete('/knowledge/{knowledge_id}', response_model=ApiResponse, summary='删除知识')
def delete_knowledge(knowledge_id: int, staff: dict = Depends(get_staff)):
    _staff_service.delete_knowledge(knowledge_id)
    return ok({'knowledge_id': knowledge_id})
