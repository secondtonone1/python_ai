'''
客服工作台 WebSocket 连接管理器 (单例)
======================================
管理"客服 id -> WebSocket 连接集合"的映射, 支撑服务端向工作台**主动推送**
(替代原先"会话列表每 5 秒 / 消息每 3 秒"的 HTTP 轮询):
- staff_session  会话信息变更: 新会话转人工 / 被接管 / 被关闭 / 有新活动
- staff_message  新消息入库: 访客消息 / 机器人回答 / 客服回复

与访客侧 WsManager (按 session 分发, 点到点) 的区别:
工作台是"广播"模型 —— 任何客服都能收到全局会话事件,
由前端按"当前列表状态 + 当前选中会话"自行决定如何渲染。

推送时逐个连接 try/except: 某个工作台断线不影响其他工作台 (对应 69 课异常捕获)。
'''
from aiservice.common.constants import WsType
from aiservice.common.logger import get_logger


def _fmt_datetime(value) -> str:
    """把 MySQL 返回的 datetime 转成前端同款 'YYYY-MM-DDTHH:MM:SS' 文本"""
    if value is None:
        return ''
    if hasattr(value, 'strftime'):
        return value.strftime('%Y-%m-%dT%H:%M:%S')
    return str(value)


class StaffWsManager:
    """客服工作台连接管理器 (单例)"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, '_ready', False):
            return
        self._connections: dict[int, set] = {}  # staff_id -> {WebSocket, ...}
        self._logger = get_logger(__name__)
        self._ready = True

    @classmethod
    def instance(cls) -> 'StaffWsManager':
        return cls()

    # ---------------- 连接管理 ----------------

    def connect(self, staff_id: int, websocket) -> None:
        """注册一个工作台连接"""
        self._connections.setdefault(staff_id, set()).add(websocket)
        total = sum(len(s) for s in self._connections.values())
        self._logger.info(f'工作台接入: staff={staff_id}, 当前在线连接数: {total}')

    def disconnect(self, staff_id: int, websocket) -> None:
        """注销一个工作台连接"""
        conns = self._connections.get(staff_id)
        if conns is None:
            return
        conns.discard(websocket)
        if not conns:
            del self._connections[staff_id]

    # ---------------- 广播 ----------------

    async def broadcast(self, data: dict) -> None:
        """向所有在线工作台广播一条消息 (个别连接失败不影响其他连接)"""
        for staff_id, conns in list(self._connections.items()):
            for websocket in list(conns):
                try:
                    await websocket.send_json(data)
                except Exception:
                    self._logger.warning(f'向工作台 staff={staff_id} 推送失败, 移除连接')
                    self.disconnect(staff_id, websocket)

    async def publish_session(self, session: dict) -> None:
        """广播一条"会话信息变更" (入参为 session_dao 的原始行, 内部统一序列化)"""
        if not session:
            return
        await self.broadcast({
            'type': WsType.STAFF_SESSION,
            'session': {
                'id': session['id'],
                'visitor_name': session.get('visitor_name', ''),
                'status': session.get('status', ''),
                'created_at': _fmt_datetime(session.get('created_at')),
                'updated_at': _fmt_datetime(session.get('updated_at')),
            },
        })

    async def publish_message(self, message: dict) -> None:
        """广播一条"新消息" (入参为消息字典, 字段与 history 接口保持一致)"""
        if not message:
            return
        payload = {key: message[key] for key in
                   ('id', 'session_id', 'role', 'content', 'source', 'rating')
                   if key in message}
        await self.broadcast({'type': WsType.STAFF_MESSAGE, 'message': payload})
