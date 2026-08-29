'''
统一异常体系
============
企业级项目通常定义自己的异常基类, 好处:
1. 业务错误携带"错误码", 由 FastAPI 异常处理器统一转换为 JSON 响应
2. 上层按异常类型捕获, 不用判断错误字符串
对应课程 01_base/07_异常处理。
'''
from aiservice.common.constants import ErrorCode


class MonitorError(Exception):
    """项目统一异常基类: 所有业务异常都携带错误码"""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'[{self.code}] {self.message}'


class ParamError(MonitorError):
    """参数错误 (400)"""

    def __init__(self, message: str = '参数错误'):
        super().__init__(ErrorCode.PARAM_ERROR, message)


class AuthError(MonitorError):
    """认证失败 (401)"""

    def __init__(self, message: str = '认证失败'):
        super().__init__(ErrorCode.UNAUTHORIZED, message)


class NoPermissionError(MonitorError):
    """无权限 (403)"""

    def __init__(self, message: str = '无权限执行该操作'):
        super().__init__(ErrorCode.NO_PERMISSION, message)


class NotFoundError(MonitorError):
    """资源不存在 (404)"""

    def __init__(self, message: str = '资源不存在'):
        super().__init__(ErrorCode.NOT_FOUND, message)


class RateLimitError(MonitorError):
    """请求过于频繁 (429), 附带建议等待秒数"""

    def __init__(self, message: str = '请求过于频繁, 请稍后再试', retry_after: float = 1.0):
        super().__init__(ErrorCode.RATE_LIMITED, message)
        self.retry_after = retry_after
