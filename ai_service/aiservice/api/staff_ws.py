'''
客服工作台 WebSocket 推送通道
=============================
工作台实时数据的"订阅源": 客服登录后建立本连接, 服务端把所有
会话事件 (staff_session / staff_message) 实时推过来 —— 替代原来的轮询。

连接地址:  ws://host/ws/staff?staff_id=1
消息协议 (JSON):
    客户端 -> 服务端: {"type": "ping"} (心跳保活)
    服务端 -> 客户端: {"type": "staff_session", "session": {...}}  会话列表变更
                     {"type": "staff_message", "message": {...}}  新消息入库
                     {"type": "pong"} / {"type": "error", ...}
鉴权说明: staff_id 放在 query 里, 与 REST 请求头 X-Staff-Id 同级的
"演示级"方案, 生产环境应换 JWT (见 docs/02 演进路线)。
'''
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from aiservice.common.constants import WsType
from aiservice.common.logger import get_logger
from aiservice.service.staff_service import StaffService
from aiservice.service.staff_ws_manager import StaffWsManager

router = APIRouter(tags=['WebSocket'])
_staff_ws_manager = StaffWsManager.instance()
_staff_service = StaffService()
_logger = get_logger(__name__)


@router.websocket('/ws/staff')
async def ws_staff(websocket: WebSocket,
                   staff_id: int = Query(..., description='客服 id (登录接口返回)')):
    """工作台推送通道: 鉴权通过后注册连接, 服务端事件实时推送"""
    # 1. 鉴权: 身份无效直接关闭 (与 REST 的 401 对应)
    try:
        _staff_service.get_staff(staff_id)
    except Exception:
        await websocket.close(code=4401, reason='invalid staff id')
        return

    # 2. 接受连接并注册
    await websocket.accept()
    _staff_ws_manager.connect(staff_id, websocket)
    _logger.info(f'工作台 WebSocket 接入: staff={staff_id}')
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get('type')
            if msg_type == WsType.PING:
                await websocket.send_json({'type': WsType.PONG})
            else:
                await websocket.send_json({
                    'type': WsType.ERROR, 'code': 400,
                    'message': f'未知消息类型: {msg_type}'})
    except WebSocketDisconnect:
        _logger.info(f'工作台 WebSocket 断开: staff={staff_id}')
    except Exception:
        _logger.exception(f'工作台 WebSocket 异常: staff={staff_id}')
        try:
            await websocket.send_json({'type': WsType.ERROR, 'code': 500, 'message': '服务器内部错误'})
        except Exception:
            pass
    finally:
        _staff_ws_manager.disconnect(staff_id, websocket)
