'''
Pydantic 请求/响应模型
======================
FastAPI 中所有接口的入参与出参都用 Pydantic 模型声明:
1. 入参自动校验(类型/必填/取值范围), 不合法自动返回 422
2. 自动生成 /docs 接口文档
3. 出参用 response_model 声明后自动过滤多余字段
'''
from datetime import datetime

from pydantic import BaseModel, Field


# ---------------- 统一响应 ----------------

class ApiResponse(BaseModel):
    """统一响应格式: 所有接口返回 {code, message, data}"""
    code: int = Field(description='错误码, 200 表示成功')
    message: str = Field(default='ok', description='提示信息')
    data: object = Field(default=None, description='业务数据')


# ---------------- 访客侧 ----------------

class CreateSessionRequest(BaseModel):
    """创建会话请求"""
    visitor_name: str | None = Field(default=None, max_length=32, description='访客昵称')


class SessionInfo(BaseModel):
    """会话信息"""
    id: int
    visitor_name: str
    status: str
    created_at: datetime
    updated_at: datetime


class MessageInfo(BaseModel):
    """消息信息"""
    id: int
    session_id: int
    role: str
    content: str
    source: str | None = None
    rating: int | None = None
    created_at: datetime


class RateRequest(BaseModel):
    """满意度评价请求"""
    rating: int = Field(description='1=满意 -1=不满意', ge=-1, le=1)


# ---------------- 客服侧 ----------------

class StaffLoginRequest(BaseModel):
    """客服登录请求"""
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=64)


class StaffInfo(BaseModel):
    """客服信息"""
    id: int
    username: str
    display_name: str


class StaffReplyRequest(BaseModel):
    """客服回复请求"""
    content: str = Field(min_length=1, max_length=2000, description='回复内容')


class KnowledgeCreateRequest(BaseModel):
    """知识库新增请求"""
    category: str = Field(default='', max_length=64)
    question: str = Field(min_length=1, max_length=255)
    keywords: str = Field(min_length=1, max_length=255, description='关键词, 逗号分隔')
    answer: str = Field(min_length=1, max_length=5000)


class KnowledgeUpdateRequest(BaseModel):
    """知识库更新请求 (字段均可选, 只更新传入的字段)"""
    category: str | None = Field(default=None, max_length=64)
    question: str | None = Field(default=None, min_length=1, max_length=255)
    keywords: str | None = Field(default=None, min_length=1, max_length=255)
    answer: str | None = Field(default=None, min_length=1, max_length=5000)
    enabled: int | None = Field(default=None, description='1启用 0停用', ge=0, le=1)


class KnowledgeInfo(BaseModel):
    """知识库条目信息"""
    id: int
    category: str
    question: str
    keywords: str
    answer: str
    enabled: int
    hit_count: int
    created_at: datetime
