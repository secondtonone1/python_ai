'''
WebSocket 连接管理器 (单例)
===========================
管理"会话 id -> WebSocket 连接集合"的映射, 支撑服务端主动推送:
- 机器人流式输出: 逐分片推给访客
- 人工客服回复: 实时推给访客浏览器 (无需轮询)

一个会话可能有多个连接(访客开了多个页面), 推送时广播给全部连接。
'''
from aiservice.common.logger import get_logger


class WsManager:
    """WebSocket 连接管理器 (单例, 对应课程 16_单例模式.py)"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, '_ready', False):
            return
        self._connections: dict[int, set] = {}  # session_id -> {WebSocket, ...}
        self._logger = get_logger(__name__)
        self._ready = True

    @classmethod
    def instance(cls) -> 'WsManager':
        return cls()

    def connect(self, session_id: int, websocket) -> None:
        """注册连接"""
        self._connections.setdefault(session_id, set()).add(websocket)
        self._logger.info(f'WebSocket 接入: session={session_id}, 当前连接数: {len(self._connections[session_id])}')

    def disconnect(self, session_id: int, websocket) -> None:
        """注销连接"""
        conns = self._connections.get(session_id)
        if conns is None:
            return
        conns.discard(websocket)
        if not conns:
            del self._connections[session_id]
        self._logger.info(f'WebSocket 断开: session={session_id}')

    async def send_to_session(self, session_id: int, data: dict) -> None:
        """向某个会话的所有连接推送一条消息 (个别连接失败不影响其他连接)"""
        for websocket in list(self._connections.get(session_id, ())):
            try:
                await websocket.send_json(data)
            except Exception:
                self._logger.warning(f'向 session={session_id} 推送消息失败, 移除连接')
                self.disconnect(session_id, websocket)
