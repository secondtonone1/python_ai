'''
WebSocket 流式对话接口
======================
对应课程 84-89 网络编程知识的 Web 形态: WebSocket 是"HTTP 升级而来的长连接",
与 TCP 长连接一样是双向流式通道, 但浏览器原生支持。

消息协议 (JSON, 见 docs/03_API文档.md):
    客户端 -> 服务端: {"type": "chat", "content": "..."} / {"type": "ping"}
    服务端 -> 客户端: {"type": "chunk", "delta": "..."} 流式分片
                     {"type": "message_end", "message": {...}}
                     {"type": "session_status", "status": "..."}
                     {"type": "staff_reply", "message": {...}} 人工回复实时推送
                     {"type": "error", "code": ..., "message": "..."}
'''
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from aiservice.common.constants import WsType
from aiservice.common.logger import get_logger
from aiservice.service.chat_service import ChatService
from aiservice.service.ws_manager import WsManager

router = APIRouter(tags=['WebSocket'])
_chat_service = ChatService()
_ws_manager = WsManager.instance()
_logger = get_logger(__name__)


@router.websocket('/ws/chat/{session_id}')
async def ws_chat(websocket: WebSocket, session_id: int):
    """流式对话通道: 一个会话的所有消息都走这个连接"""
    await websocket.accept()
    _ws_manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get('type')
            if msg_type == WsType.CHAT:
                # 聊天消息 -> 编排服务处理 (内部包含限流/引擎/流式回复)
                await _chat_service.handle_chat(session_id, websocket, data.get('content', ''))
            elif msg_type == WsType.PING:
                # 心跳保活 (对应 TCP 长连接的心跳概念)
                await websocket.send_json({'type': WsType.PONG})
            else:
                await websocket.send_json({
                    'type': WsType.ERROR, 'code': 400,
                    'message': f'未知消息类型: {msg_type}'})
    except WebSocketDisconnect:
        _logger.info(f'WebSocket 断开: session={session_id}')
    except Exception:
        _logger.exception(f'WebSocket 处理异常: session={session_id}')
        try:
            await websocket.send_json({'type': WsType.ERROR, 'code': 500, 'message': '服务器内部错误'})
        except Exception:
            pass
    finally:
        _ws_manager.disconnect(session_id, websocket)
