'''
页面路由
========
把前端页面(static/)暴露给浏览器:
- GET /       来访者聊天页
- GET /staff  咨询师工作台
'''
from fastapi import APIRouter
from fastapi.responses import FileResponse

from aiservice.common.config import PROJECT_ROOT

router = APIRouter(tags=['页面'])
_STATIC_DIR = PROJECT_ROOT / 'aiservice' / 'static'


@router.get('/', include_in_schema=False)
def index_page():
    """来访者聊天页"""
    return FileResponse(_STATIC_DIR / 'index.html')


@router.get('/staff', include_in_schema=False)
def staff_page():
    """咨询师工作台"""
    return FileResponse(_STATIC_DIR / 'staff.html')
