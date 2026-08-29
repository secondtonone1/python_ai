'''
访客 REST 接口
==============
注意端点函数用的是普通 def(同步函数): FastAPI 会把它放到线程池中执行,
这样内部的阻塞数据库操作不会卡住事件循环 (对应课程 67-70 线程池)。
'''
from fastapi import APIRouter, Request

from aiservice.api.deps import ok
from aiservice.schema.models import ApiResponse, CreateSessionRequest, RateRequest
from aiservice.service.chat_service import ChatService

router = APIRouter(prefix='/api', tags=['访客接口'])
_chat_service = ChatService()


@router.post('/session', response_model=ApiResponse, summary='创建会话')
def create_session(req: CreateSessionRequest, request: Request):
    """创建客服会话, 返回会话信息 (带 IP 限流)"""
    session = _chat_service.create_session(req.visitor_name, request.client.host)
    return ok(session)


@router.get('/session/{session_id}/history', response_model=ApiResponse, summary='会话历史')
def session_history(session_id: int):
    """查询会话的历史消息"""
    return ok(_chat_service.history(session_id))


@router.post('/message/{message_id}/rate', response_model=ApiResponse, summary='满意度评价')
def rate_message(message_id: int, req: RateRequest):
    """对机器人回答做满意度评价: 1=满意 -1=不满意"""
    _chat_service.rate_message(message_id, req.rating)
    return ok({'message_id': message_id, 'rating': req.rating})
