'''
接口层公共依赖
==============
1. ok(): 统一成功响应格式 {code, message, data}
2. get_staff(): FastAPI 依赖注入 —— 从请求头解析客服身份并校验
   (对应课程 33-45 装饰器: 依赖注入是"装饰器思想"在框架中的体现)
'''
from fastapi import Header

from aiservice.common.exceptions import AuthError
from aiservice.service.staff_service import StaffService


def ok(data=None) -> dict:
    """统一成功响应"""
    return {'code': 200, 'message': 'ok', 'data': data}


def get_staff(x_staff_id: int | None = Header(default=None)) -> dict:
    """校验请求头 X-Staff-Id 对应的客服身份。
    登录成功后前端在 localStorage 保存客服 id, 后续请求自动带上该请求头。
    注意: 这是演示级鉴权方案, 生产环境应使用 JWT (见 docs/02 演进路线)。
    """
    if x_staff_id is None:
        raise AuthError('缺少 X-Staff-Id 请求头, 请先登录')
    return StaffService().get_staff(x_staff_id)
