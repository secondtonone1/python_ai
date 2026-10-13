from fastapi import FastAPI
# 创建应用
app = FastAPI(title='FastAPI教学Demo', version='1.0')

# 注册/路由回调函数
@app.get('/')
async def root():
    return {"msg": "Hello FastAPI"}

# 异步写法，适合IO任务（数据库、http请求）
@app.get("/async")
async def demo_async():
    return {"data": "async"}

# 普通同步函数也支持，CPU密集任务可以用
@app.get("/sync")
def demo_sync():
    return {"data": "sync"}

@app.get("/user/list")
async def get_user_list(page: int = 1, size: int = 10):
    # page默认值1，size默认10
    return {"page": page, "size": size}

from typing import Optional
@app.get("/search")
async def search(keyword: Optional[str] = None):
    return {"keyword": keyword}

from pydantic import BaseModel, Field

# 定义请求体模型
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="用户名")
    password: str = Field(min_length=6)
    age: int | None = Field(default=None, ge=0, le=120) # 可选，0~120

class UserOut(BaseModel):
    username: str
    age: int | None

@app.post("/user/create",response_model=UserOut)
async def create_user(user: UserCreate):
    # FastAPI自动把前端json解析成UserCreate对象，并自动校验
    print(f'user data is \n{user.model_dump()}')
    return  user

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    # 类型标注int，FastAPI自动校验，如果传入字符串会直接报错
    return {"user_id": user_id}


from fastapi import status
from fastapi.responses import JSONResponse

@app.get("/item/{item_id}", status_code=status.HTTP_201_CREATED)
async def get_item(item_id: int):
    if item_id <= 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"msg": "id不能小于等于0"}
        )
    return {"item_id": item_id}

