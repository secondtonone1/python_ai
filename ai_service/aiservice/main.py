'''
FastAPI 应用工厂
================
create_app() 模式 (企业级惯例): 应用组装与启动解耦, 便于测试与多环境部署。

本文件包含三个企业级要点:
1. lifespan 生命周期管理: 启动时初始化配置/日志/连接池 + 拉起后台任务, 退出时回收资源
2. 统一异常映射: 业务异常 MonitorError -> 统一 JSON 响应格式 {code, message}
3. 参数校验错误映射: Pydantic 校验失败也转成统一格式 (默认是 FastAPI 的 422 格式)
'''
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from aiservice.api import chat, pages, staff, staff_ws, ws
from aiservice.common.config import Config
from aiservice.common.exceptions import MonitorError, RateLimitError
from aiservice.common.logger import get_logger, setup_logging
from aiservice.dao.db_pool import DbPool
from aiservice.dao.session_dao import SessionDao
from aiservice.service.rate_limiter import RateLimiter


# ---------------- 后台任务 ----------------

async def _background_loop() -> None:
    """后台周期任务: 会话超时归档 + 限流器内存清理 (阻塞 SQL 交给线程池执行)"""
    logger = get_logger(__name__)
    session_dao = SessionDao()
    timeout = int(Config.instance().get('bot.session_timeout_minutes', 30))
    loop = asyncio.get_running_loop()
    while True:
        await asyncio.sleep(60)
        try:
            archived = await loop.run_in_executor(None, session_dao.archive_timeout, timeout)
            if archived:
                logger.info(f'后台任务: 归档超时会话 {archived} 个')
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.warning(f'后台归档任务异常: {e}')
        # 清理限流器中超过 2 个窗口无访问的 key, 防止内存膨胀 (对应 docs/02 可靠性设计)
        RateLimiter.cleanup_all()


# ---------------- 生命周期 ----------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = Config.instance()
    setup_logging(config)
    logger = get_logger(__name__)
    # 初始化数据库连接池: Web 服务不因数据库瞬时不可用而拒绝启动,
    # 数据接口在数据库恢复后即可自动可用 (连接池懒建连)
    try:
        DbPool.instance(config.section('database'))
    except Exception as e:
        logger.warning(f'数据库连接失败(数据接口将不可用): {e}')
    # 拉起后台归档任务
    background_task = asyncio.create_task(_background_loop())
    logger.info('心聆 MindEcho 在线心理支持平台启动完成')
    yield
    # 退出: 取消后台任务 + 关闭连接池
    background_task.cancel()
    try:
        DbPool.instance().close()
    except Exception:
        pass
    logger.info('服务已关闭')


# ---------------- 异常映射 ----------------

async def monitor_error_handler(request: Request, exc: MonitorError) -> JSONResponse:
    """业务异常 -> 统一 JSON 响应 (错误码即 HTTP 状态码)"""
    headers = None
    if isinstance(exc, RateLimitError):
        headers = {'Retry-After': str(int(exc.retry_after) + 1)}
    return JSONResponse(status_code=exc.code,
                        content={'code': exc.code, 'message': exc.message},
                        headers=headers)


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Pydantic 参数校验失败 -> 统一格式 (默认 422 格式改为 400 统一格式)"""
    first = exc.errors()[0] if exc.errors() else {}
    location = '.'.join(str(item) for item in first.get('loc', []))
    return JSONResponse(status_code=400,
                        content={'code': 400,
                                 'message': f'参数校验失败 [{location}]: {first.get("msg", "")}'})


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTPException(如路由不存在 404) -> 统一格式"""
    return JSONResponse(status_code=exc.status_code,
                        content={'code': exc.status_code, 'message': str(exc.detail)})


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """兜底异常处理器: 未预期异常(如数据库连接失败)也返回统一 JSON 格式。

    完整堆栈记录到日志, 对外只返回通用错误
    (安全实践: 不向客户端暴露内部实现细节)
    """
    get_logger(__name__).exception(f'未处理异常: {request.method} {request.url.path}')
    return JSONResponse(status_code=500,
                        content={'code': 500, 'message': '服务器内部错误, 请稍后再试'})


# ---------------- 应用工厂 ----------------

def create_app() -> FastAPI:
    app = FastAPI(
        title='心聆 MindEcho 在线心理支持平台',
        description='02_advance 阶段 AI 方向综合项目: 规则引擎驱动的 AI 心理咨询师, '
                    '可插拔设计; 咨询师端提供 AI 检索润色助手, 后续可无缝接入真实大模型',
        version='1.1.0',
        lifespan=lifespan,
    )
    app.add_exception_handler(MonitorError, monitor_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(pages.router)
    app.include_router(chat.router)
    app.include_router(staff.router)
    app.include_router(ws.router)
    app.include_router(staff_ws.router)

    @app.get('/api/health', tags=['系统'], summary='健康检查')
    def health():
        return {'code': 200, 'message': 'ok', 'data': {'status': 'up'}}

    return app


# 模块级 app 实例: uvicorn 通过 "aiservice.main:app" 导入
app = create_app()
