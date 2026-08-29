'''
滑动窗口限流器
==============
企业级服务必备的"自我保护"能力: 限制单个客户端在时间窗口内的请求次数,
防止被刷接口/恶意攻击。

实现: 为每个 key(如会话 id / IP)维护一个时间戳队列(deque),
窗口外的过期时间戳出队, 队列长度即窗口内的请求次数。
多线程环境(uvicorn 线程池)下需要加锁 (对应课程 59/60 线程安全与互斥锁)。
后续阶段可用 Redis 实现分布式限流 (见 docs/02 演进路线)。
'''
import threading
import time
from collections import deque

from aiservice.common.logger import get_logger


class RateLimiter:
    """滑动窗口限流器: 每个 key 独立计数, 窗口滑动自动释放配额"""

    _registry: list['RateLimiter'] = []   # 全部实例注册表 (供后台任务统一清理)
    _registry_lock = threading.Lock()

    def __init__(self, max_requests: int, window_seconds: float):
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._hits: dict[str, deque] = {}
        self._lock = threading.RLock()
        self._logger = get_logger(__name__)
        with RateLimiter._registry_lock:
            RateLimiter._registry.append(self)

    def allow(self, key: str, now: float | None = None) -> tuple[bool, float]:
        """请求是否放行, 返回 (是否放行, 建议等待秒数)
        :param now: 当前时间戳, 单元测试时可注入模拟时间
        """
        with self._lock:
            now = time.time() if now is None else now
            queue = self._hits.setdefault(key, deque())
            # 清理窗口外的过期记录
            while queue and now - queue[0] > self._window_seconds:
                queue.popleft()
            if len(queue) >= self._max_requests:
                retry_after = self._window_seconds - (now - queue[0]) + 0.01
                return False, round(retry_after, 2)
            queue.append(now)
            return True, 0.0

    def cleanup(self, now: float | None = None) -> None:
        """清理长时间无访问的 key, 防止内存无限膨胀 (后台任务周期调用)"""
        with self._lock:
            now = time.time() if now is None else now
            expired_keys = [
                key for key, queue in self._hits.items()
                if not queue or now - queue[-1] > self._window_seconds * 2
            ]
            for key in expired_keys:
                del self._hits[key]

    @classmethod
    def cleanup_all(cls, now: float | None = None) -> None:
        """清理所有限流器实例中过期 key (由 main.py 后台任务周期调用)"""
        for limiter in list(cls._registry):
            try:
                limiter.cleanup(now)
            except Exception:
                pass  # 单个实例清理失败不影响其他实例
