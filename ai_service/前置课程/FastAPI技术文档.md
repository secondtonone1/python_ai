# FastAPI 技术文档

> 前置课程讲义 · Web 框架入门
>
> 适用版本：FastAPI 0.11x 及以上 / Pydantic v2 / Python 3.10+（本文全部示例在 FastAPI 0.141 + Pydantic 2.13 上运行验证通过）
>
> 前置知识：会基础 Python（类型注解、面向对象、装饰器、上下文管理器）。**不要求你事先了解 Flask 或任何 Web 知识，也不要求异步基础**——我们从"在浏览器输入一个网址"讲起，异步部分会用生活类比带你入门。

---

## 1 从一个网址说起：认识 Web 与 FastAPI

在写第一行代码之前，我们先弄清楚几个最基本的问题：网页是什么？在浏览器里输入一个网址后发生了什么？我们这门课要写的程序在其中扮演什么角色？FastAPI 又是个什么东西？把这些想明白，后面的概念都会顺理成章。

### 1.1 你每天都在使用 Web

用浏览器看新闻、查资料、购物、用网页版邮箱，乃至很多手机 App 里点开的页面——它们都有一个共同点：

- 你在一个**客户端**（绝大多数时候是浏览器）上操作；
- 背后有一台（实际是很多台）远方的**服务器**在为你服务。

你在浏览器里看到的文字、图片、按钮、视频，不是凭空出现的，而是**服务器通过网络"送"过来的**。我们这门课要学的，就是怎么用 Python 写出"送出这些内容"的服务器程序。

### 1.2 在浏览器输入一个网址，发生了什么

假设你在地址栏输入 `http://www.example.com/books` 然后回车，想看看有哪些书。整个过程可以拆成四步：

1. 浏览器把"我想要 `/books` 这个资源"打包成一个**请求（Request）**，通过网络发给服务器；
2. 服务器收到请求，看了看路径是 `/books`，于是去准备数据（可能要查询数据库）；
3. 服务器把准备好的内容打包成一个**响应（Response）**，发回给浏览器；
4. 浏览器收到响应，把内容渲染成你看到的页面。

这个"请求—响应"的来回，全世界的浏览器和服务器都遵循同一套对话规矩，这套规矩叫 **HTTP**（超文本传输协议）。你可以把它理解成浏览器和服务器之间的"共同语言"：浏览器用 HTTP 提问，服务器用 HTTP 回答。

```
浏览器（客户端）                            服务器（你将来写的 Python 程序）
      │                                              │
      │  ① 请求 Request：我想要 /books 的内容          │
      │ ───────────────────────────────────────────▶ │
      │                                              │ ② 处理：查数据库、做计算
      │  ③ 响应 Response：这是你要的数据              │
      │ ◀─────────────────────────────────────────── │
      │                                              │
      │  ④ 浏览器把数据显示成页面                      │
```

请记住这种对话的两个特点：**一问一答、答完即结束**。浏览器不主动发问，服务器就不会主动说话——这一点在第 9 章讲 WebSocket（让服务器能主动推送）时还会提到。

### 1.3 前端与后端：一个管"长相"，一个管"脑子"

一次网页访问里，其实有两种不同的工作：

- **前端**：服务器把内容送过来之后，浏览器负责把文字、颜色、排版、按钮、动画呈现出来，并响应你的点击、输入。这部分由 HTML、CSS、JavaScript 完成，运行在你的浏览器里。
- **后端**：运行在服务器上，负责"处理逻辑、存取数据"——判断你有没有登录、查询你要的图书、计算价格、把数据存进数据库。

用餐厅打个比方：

| 餐厅里的角色 | 对应 Web 里的角色 | 干什么 |
|---|---|---|
| 菜单、装修、服务员 | 前端 | 你看得到、摸得着，负责接待和呈现 |
| 后厨 | 后端 | 你看不到，负责真正"做菜"（处理逻辑） |
| 冰柜、仓库里的食材 | 数据库 | 存放原材料（数据），后厨按需取用 |

你点菜（浏览器发请求）→ 后厨从仓库取食材、把菜做好（后端处理逻辑、读写数据库）→ 服务员把菜端上桌（响应返回、前端显示）。

**我们这门课要写的是"后厨"，也就是后端**：让 Python 程序充当服务器，接收浏览器的请求、处理逻辑、返回响应。

### 1.4 后端要做哪些事？为什么需要"框架"

现在问题来了：如果不借助任何工具，要用 Python 从零写一个能回应浏览器的后端，你得自己完成这五件事：

1. 监听一个网络端口，等待客户端连接；
2. 从到来的**原始字节流**里，按 HTTP 规矩解析出：请求方法（GET / POST）、路径（`/books`）、参数、请求头、请求体；
3. 根据路径，决定"应该执行哪个函数"；
4. 执行业务逻辑、查询数据库；
5. 把结果重新按 HTTP 规矩拼成字节流，发回去。

你会发现，第 1、2、3、5 件事对几乎所有网站都一样——不管你做的是图书网站、订单系统还是博客，它们与你的具体业务毫无关系，却非常繁琐、极易出错。

**Web 框架（Web Framework）就是把这些重复劳动提前做好的工具**。有了框架之后：

- 你只需声明"哪个路径对应哪个函数"（这叫**路由**）；
- 框架帮你监听端口、解析请求，并把请求包装成一个好用的对象；
- 你在函数里把数据 `return` 出去，框架帮你拼成合法的响应。

于是你可以把精力集中在第 4 件事——真正的业务逻辑上。打个比方：框架就像已经帮你把灶台、锅具、水电、排烟系统都装好的厨房，你这个"厨师"只管专心做菜，不必每次都从砌灶台开始。

### 1.5 FastAPI 是什么

**FastAPI 是一个现代的、高性能的 Python Web 框架**，同样用来编写网站和接口（后端）。它的名字来自 **Fast（快速）+ API（接口）**，尤其擅长编写"接口服务"。它有几个非常亮眼的特点：

- **基于类型注解**：你用 Python 自带的类型提示（type hints）声明参数和数据结构，框架据此**自动完成数据校验**——类型不对、超出范围的请求会被直接挡下，并清楚告诉你哪里错了；
- **自动生成接口文档**：代码写完，立刻得到一个**可以在网页上直接点击调试**的接口说明页面（`/docs`），不需要手写一行文档；
- **原生支持"异步"**：能高效处理大量并发请求，也原生支持 WebSocket 实时连接；
- **性能出色**：在官方基准测试中，它的性能接近 Node.js、Go 这类以高并发见长的技术。

**为什么会出现 FastAPI 这样的框架？** 传统的 Web 框架大多以"同步"方式工作：来一个请求，就派一个执行单元从头服务到尾。可 Web 请求的大部分时间其实都花在"等待"上——等数据库返回、等另一个网络接口回应。在等待的时候，这个执行单元被占着却什么也做不了，想提高并发就只能不断加开执行单元（线程），开销不小。FastAPI 用"异步"方式工作，让执行单元在等待时转而去处理别的请求，从而用更少的资源扛住更多并发；与此同时，它还把"数据校验"和"接口文档"这两件本来要手写的苦差事一并自动化了。

**FastAPI 特别适合**：

- **AI / 大模型应用的后端**——LangChain、Dify 等主流 AI 生态都以 FastAPI 为默认框架；
- 高并发、大量 IO 等待的服务；
- 需要清晰接口文档、多人协作的项目；
- 需要实时推送（WebSocket）的服务。

### 1.6 先建立一个直觉：什么是"异步"

FastAPI 最核心、也最容易让人犯怵的词就是"异步"。这里我们先用一个生活例子建立直觉，**不求甚解，有个印象即可**，第 7、8 章会带你把它彻底搞懂并亲手实测。

想象一个厨师在厨房做菜：

- **同步的做法**：厨师炖上一锅汤，这锅汤要小火煮 30 分钟。在这 30 分钟里，厨师就站在锅前干等，什么也不做；其他人点的菜也只能排队等着。
- **异步的做法**：厨师把汤炖上之后，**利用这 30 分钟的"等待时间"转身去切菜、炒菜、准备别的菜**；等汤煮好了，再回过来处理这锅汤。

同样是一个厨师（一个执行单元），异步的做法在"等待"时不闲着，于是能同时照看很多锅、服务很多人。

回到 Web 开发：一个请求大部分时间都在"等"（等数据库、等外部接口）。所谓异步，就是让程序**在等待的时候让出自己，去服务其他请求**，等数据回来了再继续。这件事能极大地提升并发能力，但也有一个陷阱——如果你在本该"等待"的时候硬要占着不放（比如在异步代码里写了一个干等的操作），反而会把所有人都卡住。这个陷阱长什么样、怎么避免，正是第 7、8 章的重头戏。

### 1.7 本文的学习路线

下面是我们的行进地图：

| 阶段 | 章节 | 在干什么 |
|---|---|---|
| ① 先跑起来 | 第 2 章 | 装好 FastAPI，写出第一个程序，并亲眼看到自动生成的接口文档 `/docs` |
| ② 学会基本操作 | 第 3–6 章 | 路径与参数；用 Pydantic 做数据校验；用 Depends 做依赖注入与鉴权；错误处理 |
| ③ 打通原理 | 第 7、8 章（重点） | 理解 ASGI 与事件循环，彻底搞懂异步、并发以及"阻塞会卡住所有人"的陷阱 |
| ④ 实时与工程化 | 第 9–12 章 | WebSocket 实时推送；应用工厂与 lifespan；中间件与 CORS；项目分层实践 |
| ⑤ 动手巩固 | 第 14、15 章 | 练习题与参考答案 |

最重要的学习建议只有一条：**边看边敲**。每个示例都请亲手运行，再试着改一改——把返回文字换成自己的名字、故意传错参数看框架怎么报错。Web 开发是"做"会的，不是"读"会的。

### 1.8 学习目标

学完本文后，你应当达到如下目标（现在不必完全看懂，学完再回来对照）：

1. 说清浏览器与服务器之间"请求—响应"的过程，以及 Web 框架帮我们做了哪些重复工作；
2. 说清 ASGI 与传统 WSGI 的区别，以及事件循环模型对并发能力的实际影响；
3. 用 FastAPI 写出带路径参数、查询参数、请求体的接口，并区分参数的不同来源；
4. 用 Pydantic 模型把数据校验声明化，并利用自动生成的接口文档；
5. 用 `Depends` 实现依赖注入，包括基于请求头的鉴权；
6. 判断一个接口该用 `async def` 还是普通 `def`，并说明阻塞代码的后果与解法；
7. 用 WebSocket 实现服务端主动推送；
8. 用应用工厂 + `lifespan` 组织一个可扩展的项目结构。

准备好了吗？我们从安装 FastAPI、跑起第一个程序开始。


---

## 2 环境准备与第一个应用

### 2.1 安装

```bash
# 推荐：带标准依赖（含 uvicorn、fastapi-cli 命令行工具）
pip install "fastapi[standard]"

# 或者分开装
pip install fastapi uvicorn

# 写接口测试时需要（TestClient 依赖 httpx）
pip install httpx
```

确认版本：

```bash
python -c "import fastapi, pydantic; print('fastapi', fastapi.__version__); print('pydantic', pydantic.VERSION)"
```

### 2.2 最小应用

新建 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI(title='Demo API', version='1.0.0')


@app.get('/')
def read_root():
    return {'message': 'hello fastapi'}


@app.get('/health')
def health():
    return {'status': 'up'}
```

与 Flask 的对照：

| | Flask | FastAPI |
|---|---|---|
| 创建应用 | `app = Flask(__name__)` | `app = FastAPI()` |
| 路由装饰器 | `@app.get('/')` | `@app.get('/')` |
| 返回值 | `dict` 自动转 JSON | `dict` 自动转 JSON |

装饰器写法几乎一样，**真正的差别从第 3 章开始**。

### 2.3 启动方式

方式一，FastAPI 命令行（FastAPI 0.111 起提供）：

```bash
fastapi dev main.py
```

`fastapi dev` 会自动开启热重载，并默认监听 `127.0.0.1:8000`。生产环境使用：

```bash
fastapi run main.py
```

方式二，直接用 uvicorn（最通用）：

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

`main:app` 的含义是"模块 `main` 中的变量 `app`"，与 Flask 的 `flask --app` 思路一致。

### 2.4 自动生成的接口文档

启动后访问下面三个地址，**不需要写一行文档代码**：

| 地址 | 内容 |
|---|---|
| `http://127.0.0.1:8000/docs` | Swagger UI，可直接在页面上调试接口 |
| `http://127.0.0.1:8000/redoc` | ReDoc，适合阅读的文档样式 |
| `http://127.0.0.1:8000/openapi.json` | OpenAPI 规范原文（JSON） |

文档的内容来自三处：路由装饰器提供路径与方法，函数签名提供参数，Pydantic 模型提供字段与约束。**这意味着写好类型注解就等于写好了文档**，这是 FastAPI 相对于 Flask 最直接的收益。


---

## 3 路径操作与参数

### 3.1 参数的四种来源

FastAPI 通过**函数签名**判断每个参数的来源，规则如下：

| 参数位置 | 来源 | 例子 |
|---|---|---|
| 出现在路径中 | 路径参数 | `/users/{user_id}` |
| 简单类型（`str`/`int`/`float`/`bool`） | 查询参数 | `/search?keyword=x` |
| Pydantic 模型 | 请求体 | `POST` 的 JSON |
| 用 `Header`/`Cookie`/`Depends` 标注 | 请求头 / Cookie / 依赖 | `x_token: str = Header(...)` |

### 3.2 路径参数

```python
from fastapi import FastAPI

app = FastAPI()


@app.get('/users/{user_id}')
def get_user(user_id: int):
    # 声明为 int 后，FastAPI 自动做类型转换
    return {'user_id': user_id, 'type': str(type(user_id))}


@app.get('/files/{file_path:path}')
def get_file(file_path: str):
    # :path 允许匹配含斜杠的路径，如 a/b/c.txt
    return {'path': file_path}
```

传入 `abc` 这样的非数字时，FastAPI 会返回 **422**（而不是 Flask 的 404），并在响应体中说明哪个参数校验失败。这个差异会在第 4 章展开。

需要给路径参数加约束时，用 `Path`：

```python
from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()


@app.get('/users/{user_id}')
def get_user(user_id: Annotated[int, Path(ge=1, le=1000, description='用户 ID')]):
    return {'user_id': user_id}
```

### 3.3 查询参数

```python
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get('/search')
def search(
    keyword: str = '',
    page: Annotated[int, Query(ge=1, description='页码')] = 1,
    size: Annotated[int, Query(ge=1, le=100, description='每页条数')] = 10,
    tag: Annotated[list[str] | None, Query(description='可重复传参')] = None,
):
    return {'keyword': keyword, 'page': page, 'size': size, 'tag': tag or []}
```

几点与 Flask 的关键差异：

1. **默认值即"可选"**。给了默认值的参数可以不传；没给默认值的参数是必填。
2. **校验是声明式的**。`Query(ge=1)` 表示"必须大于等于 1"，超范围自动返回 422 并说明原因；Flask 里这段判断要手写。
3. **列表参数直接用 `list[str]`**。访问 `/search?tag=a&tag=b` 会得到 `['a', 'b']`，不需要 `getlist`。

> 说明：FastAPI 现在推荐把校验信息放进 `Annotated[...]` 里。你也可以写成 `page: int = Query(default=1, ge=1)`，两种写法等价，前者更利于类型检查工具。

### 3.4 请求体

请求体用 Pydantic 模型声明：

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class BookCreate(BaseModel):
    """新增图书的请求体"""
    title: str = Field(min_length=1, max_length=100, description='书名')
    author: str = Field(default='', max_length=50, description='作者')
    price: float = Field(default=0.0, ge=0, description='价格，不能为负')


@app.post('/books', status_code=201)
def create_book(book: BookCreate):
    # book 已经是一个校验通过的 BookCreate 实例，字段可直接用属性访问
    return {'id': 1, 'title': book.title, 'author': book.author, 'price': book.price}
```

对照 Flask 的写法，差别非常明显：

```python
# Flask 的写法：校验逻辑与业务逻辑混在一起
# @app.post('/books')
# def create_book():
#     data = request.get_json(silent=True)
#     if data is None:
#         return {'code': 400, 'message': '请求体必须是合法 JSON'}, 400
#     title = str(data.get('title', '')).strip()
#     if not title:
#         return {'code': 400, 'message': 'title 不能为空'}, 400
#     if len(title) > 100:
#         return {'code': 400, 'message': 'title 过长'}, 400
#     price = float(data.get('price', 0))
#     if price < 0:
#         return {'code': 400, 'message': 'price 不能为负'}, 400
#     ...业务逻辑...
```

FastAPI 把这段校验代码**从业务逻辑里彻底移除**，写进了类型声明。字段越多，收益越大。

### 3.5 请求头与 Cookie

```python
from typing import Annotated

from fastapi import Cookie, FastAPI, Header

app = FastAPI()


@app.get('/me')
def me(
    x_token: Annotated[str | None, Header()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
):
    return {'token': x_token, 'session_id': session_id}
```

参数名的转换规则：下划线会自动映射为连字符，所以 `x_token` 对应请求头 `x-token`，`session_id` 对应 Cookie `session_id`。


---

## 4 Pydantic 数据校验

### 4.1 模型定义

Pydantic 模型就是一个继承 `BaseModel` 的类，字段用类型注解声明：

```python
from datetime import datetime

from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    name: str
    email: str | None = None
    created_at: datetime | None = None


# 直接用 Python 对象构造，会自动做类型转换与校验
u = UserInfo(id=1, name='张三')
print(u.model_dump())
# {'id': 1, 'name': '张三', 'email': None, 'created_at': None}

# 从 JSON 字符串或字典构造
u2 = UserInfo.model_validate({'id': '2', 'name': '李四'})
print(u2.id, type(u2.id))     # 2 <class 'int'>  —— 字符串 "2" 被转换成了 int
```

**类型转换是 Pydantic 的核心能力**：`'2'` 会被转成 `2`，`'2026-09-25T10:00:00'` 会被转成 `datetime`。无法转换或违反约束时，抛出 `ValidationError`——在 FastAPI 中它会被自动转成 422 响应。

### 4.2 字段约束 `Field`

```python
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100, description='书名')
    price: float = Field(default=0.0, ge=0, le=99999, description='价格')
    stock: int = Field(default=0, ge=0, description='库存')
    tags: list[str] = Field(default_factory=list, description='标签')
```

常用约束：

| 参数 | 适用类型 | 含义 |
|---|---|---|
| `min_length` / `max_length` | 字符串、列表 | 长度范围 |
| `ge` / `gt` / `le` / `lt` | 数值 | 大于等于 / 大于 / 小于等于 / 小于 |
| `pattern` | 字符串 | 正则匹配 |
| `default` | 全部 | 默认值（有默认值即为可选） |
| `default_factory` | 可变类型 | 默认值工厂，**列表、字典必须用它** |
| `description` | 全部 | 字段说明，出现在 `/docs` 中 |

> 重要：`tags: list[str] = []` 是 Python 的经典陷阱，多个实例会共享同一个列表。Pydantic 对此会告警，正确写法是 `default_factory=list`。

### 4.3 校验失败时的响应

请求 `/books` 时传 `{"title": "", "price": -5}`，FastAPI 返回 **422** 与结构化错误：

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "input": ""
    },
    {
      "type": "greater_than_equal",
      "loc": ["body", "price"],
      "msg": "Input should be greater than or equal to 0",
      "input": -5
    }
  ]
}
```

注意 `loc` 字段：它精确定位到出错的字段路径，前端可以直接把提示挂到对应输入框上。这是手写校验很难低成本做到的。

### 4.4 响应模型与字段过滤

用 `response_model` 声明返回值结构，FastAPI 会**自动过滤掉未声明的字段**——这是防止敏感信息外泄的重要机制：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserIn(BaseModel):
    name: str
    password: str          # 接收时必须有


class UserOut(BaseModel):
    name: str              # 返回时只暴露这些字段


@app.post('/users', response_model=UserOut)
def create_user(user: UserIn):
    # 即使这里返回了 password，也会被 response_model 过滤掉
    return {'name': user.name, 'password': user.password}
```

也可以在装饰器上直接写返回类型注解：

```python
@app.post('/users')
def create_user(user: UserIn) -> UserOut:
    return UserOut(name=user.name)
```

### 4.5 自定义校验器

内置约束覆盖不到的业务规则，用 `field_validator`：

```python
from pydantic import BaseModel, field_validator


class BookCreate(BaseModel):
    title: str
    isbn: str

    @field_validator('isbn')
    @classmethod
    def check_isbn(cls, value: str) -> str:
        cleaned = value.replace('-', '').strip()
        if len(cleaned) not in (10, 13) or not cleaned.isdigit():
            raise ValueError('ISBN 必须是 10 位或 13 位数字')
        return cleaned          # 返回清洗后的值，替换原值
```

需要注意两点：

1. **必须加 `@classmethod`**。这是 Pydantic v2 的要求，漏掉会报错或告警。
2. **抛 `ValueError`**。Pydantic 会把它包装成一条标准的校验错误；抛其它异常类型则不会被当作校验错误处理。

跨字段的校验用 `model_validator`：

```python
from pydantic import BaseModel, model_validator


class DateRange(BaseModel):
    start: str
    end: str

    @model_validator(mode='after')
    def check_order(self):
        if self.start > self.end:
            raise ValueError('start 不能晚于 end')
        return self
```

### 4.6 Pydantic v1 到 v2 速查

网上大量教程仍是 v1 写法，与 v2 不兼容。对照表如下：

| 用途 | Pydantic v1 | Pydantic v2 |
|---|---|---|
| 模型配置 | `class Config:` | `model_config = ConfigDict(...)` |
| 字典序列化 | `.dict()` | `.model_dump()` |
| JSON 序列化 | `.json()` | `.model_dump_json()` |
| 从字典构造 | `.parse_obj()` | `.model_validate()` |
| 字段校验器 | `@validator` | `@field_validator`（需配 `@classmethod`） |
| 模型级校验器 | `@root_validator` | `@model_validator` |
| ORM 对象转模型 | `orm_mode = True` | `from_attributes=True` |

排查"按教程写却报错"的问题时，先确认教程用的是哪个大版本。


---

## 5 依赖注入 `Depends`

### 5.1 依赖注入解决什么问题

很多接口在进入业务逻辑之前，都要做同样的事：校验登录态、取数据库连接、解析分页参数、记录当前用户。如果每个接口都复制一遍，会产生大量重复代码。

依赖注入的思路是：**把"接口执行前必须先准备好的东西"声明成参数**，由框架负责准备好并传进来。Flask 里没有对应的原生机制，通常要用装饰器自己实现。

### 5.2 函数依赖

```python
from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI()


def pagination(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
) -> dict:
    return {'page': page, 'size': size, 'offset': (page - 1) * size}


@app.get('/books')
def list_books(pager: Annotated[dict, Depends(pagination)]):
    return {'pager': pager}
```

`Depends(pagination)` 告诉 FastAPI：调用这个接口前，先执行 `pagination`，把它声明的查询参数解析好，返回值注入 `pager` 参数。

### 5.3 类依赖

需要携带状态或多个相关方法时，用类作为依赖更合适：

```python
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


class CurrentStaff:
    """从请求头解析当前咨询师身份"""

    def __init__(self, x_staff_id: Annotated[int | None, Header()] = None):
        if x_staff_id is None:
            raise HTTPException(status_code=401, detail='缺少 X-Staff-Id 请求头，请先登录')
        self.staff_id = x_staff_id

    @property
    def display(self) -> str:
        return f'staff-{self.staff_id}'


@app.get('/api/staff/sessions')
def list_sessions(staff: Annotated[CurrentStaff, Depends(CurrentStaff)]):
    return {'viewer': staff.display, 'sessions': []}
```

在依赖里抛 `HTTPException` 是标准做法：身份不合法时，接口函数根本不会被执行，直接返回 401。

### 5.4 子依赖与缓存

依赖可以嵌套，内层依赖会被自动解析：

```python
def get_config() -> dict:
    return {'env': 'dev'}


def get_client(cfg: Annotated[dict, Depends(get_config)]) -> str:
    return f"client-for-{cfg['env']}"


@app.get('/info')
def info(client: Annotated[str, Depends(get_client)]):
    return {'client': client}
```

**同一请求内，同一个依赖默认只执行一次**，结果会被缓存复用。你可以直接验证这一点：

```python
called = []


def tracker() -> int:
    called.append(1)
    return len(called)


@app.get('/cache-demo')
def cache_demo(a: Annotated[int, Depends(tracker)], b: Annotated[int, Depends(tracker)]):
    # 同一个请求内 tracker 只执行一次，a 与 b 相等
    return {'a': a, 'b': b, 'called_times': len(called)}
```

若确实需要每次都重新执行，可以在 `Depends` 中传入 `use_cache=False`。

### 5.5 依赖注入的实质

`Depends` 让"鉴权、分页、数据库会话、当前用户"这些**横切关注点**从接口函数中剥离出去。它的三个直接收益：

1. 接口函数的签名只表达业务需要什么，逻辑更干净；
2. 依赖本身可以独立单元测试，只需要构造参数即可；
3. 鉴权逻辑集中在一处，规则变更时不用逐个接口修改。


---

## 6 错误处理

### 6.1 `HTTPException`

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get('/users/{user_id}')
def get_user(user_id: int):
    if user_id > 1000:
        raise HTTPException(status_code=404, detail='用户不存在')
    return {'user_id': user_id}
```

抛出后 FastAPI 会返回 `{"detail": "用户不存在"}` 与对应的状态码。注意与校验失败的 422 区分：**422 是"请求格式不合法"，`HTTPException` 是"请求合法但业务上不允许"**。

### 6.2 统一响应格式

FastAPI 默认的错误格式是 `{"detail": ...}`，而 4.3 节提到的校验错误是 `{"detail": [{...}]}`。团队若要求所有接口统一为 `{code, message, data}`，需要注册异常处理器。

### 6.3 自定义异常与异常处理器

```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()


class AppError(Exception):
    """业务异常基类，携带错误码"""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class ParamError(AppError):
    def __init__(self, message: str = '参数错误'):
        super().__init__(400, message)


class NotFoundError(AppError):
    def __init__(self, message: str = '资源不存在'):
        super().__init__(404, message)


@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.code,
                        content={'code': exc.code, 'message': exc.message})


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    # 把默认的 422 改成 400，并压平错误信息
    first = exc.errors()[0] if exc.errors() else {}
    location = '.'.join(str(item) for item in first.get('loc', []))
    return JSONResponse(
        status_code=400,
        content={'code': 400, 'message': f'参数校验失败 [{location}]: {first.get("msg", "")}'},
    )


@app.exception_handler(Exception)
async def handle_unexpected(request: Request, exc: Exception):
    # 兜底：完整堆栈只写日志，对外返回通用提示
    return JSONResponse(status_code=500,
                        content={'code': 500, 'message': '服务器内部错误，请稍后再试'})


@app.get('/orders/{order_id}')
def get_order(order_id: int):
    if order_id <= 0:
        raise ParamError('order_id 必须为正整数')
    raise NotFoundError(f'订单 {order_id} 不存在')
```

需要注意 `@app.exception_handler(Exception)` 这个兜底处理器的**注册顺序与优先级**：FastAPI（Starlette）会优先匹配更具体的异常类型，因此 `AppError` 处理器仍会生效；但兜底处理器**不会**捕获 `HTTPException`（它由内置处理器处理），这比 Flask 里手写 `except Exception` 时要自己判断 `isinstance(err, HTTPException)` 更省心。

#### 7.3.1 两个实测细节（写测试时会遇到）

上面这段代码已实测通过，但有两个行为容易让人困惑，先记下来可以少排半小时的错。

**一、兜底处理器会“先响应、后重新抛出”。**
`@app.exception_handler(Exception)` 被 Starlette 注册在 `ServerErrorMiddleware` 上。它发送完 500 响应之后，**会把同一个异常再抛出去**，交给服务器的日志系统记录完整堆栈。由此带来两种表现：

- 真实部署（uvicorn）中，客户端能正常收到你定义的 500 JSON，同时服务器控制台打印完整堆栈——这正是我们要的效果；
- 但用 `TestClient` 写测试时，它默认会把这个异常重新抛给你的测试代码。

```python
from fastapi.testclient import TestClient

client = TestClient(app)                                  # 请求 /crash 会直接抛 ValueError
client = TestClient(app, raise_server_exceptions=False)   # 才能拿到 500 响应体
```

所以测试“未预期异常返回 500 且不泄露内部细节”时，必须用后一种写法。

**二、路由不存在的 404 不会进入兜底处理器。**
请求一个未注册的路径时，404 由路由层直接返回，不经过异常处理器，因此仍保持 404，不会被兜底逻辑改写成 500。用 `client.get('/no-such-route')` 即可验证。


---

## 7 FastAPI 是怎么跑起来的：ASGI 与事件循环

到这里，你已经用 FastAPI 写过不少接口，也见识了自动文档与数据校验。

这一章我们退到框架背后，回答两个根本问题：浏览器发来的请求究竟是怎么到达你函数的？FastAPI 主打的“异步”到底是怎么一回事？把这两个问题搞懂，第 8 章的并发实战才会真正落地。

### 7.1 先理解它的“前任”：同步模型

要看懂 FastAPI 的工作方式，我们先了解一种更传统、也更直观的后端工作模型——**同步模型**（它的正式名称叫 WSGI，这里先理解机制，名称先记住即可）。

在这种模型下，服务器每接到一个请求，就派一个执行单元（通常是线程）专门服务它：从接收、处理到返回全程跟进，直到这个请求处理完，执行单元才被释放、转去服务下一个请求。

这种模型简单直观，但有两条天然的限制：

1. **没有原生的长连接能力**。像 WebSocket 那样需要协议升级、双方持续通信的场景，“一问一答、返回即结束”的同步模型无法直接表达，只能借助额外的库绕开。
2. **并发能力靠堆叠执行单元**。当一个请求大部分时间在等待 IO（数据库、外部接口）时，执行单元被占着却只能干等；想提高并发就只能不断加开线程，而线程本身也有内存与切换开销。

ASGI（Asynchronous Server Gateway Interface，异步服务器网关接口）正是为解决这两条限制而设计的后继规范，FastAPI 就构建在它之上。

### 7.2 ASGI 规范

ASGI 应用是一个**异步可调用对象**，接收三个参数：

| 参数 | 含义 |
|---|---|
| `scope` | 字典，描述这次连接（协议类型、路径、请求头、查询串等） |
| `receive` | 异步函数，用于接收来自客户端的事件 |
| `send` | 异步函数，用于向客户端发送事件 |

一个纯 ASGI 应用不需要任何框架：

```python
# 纯 ASGI 应用：不依赖任何框架
async def application(scope, receive, send):
    assert scope['type'] == 'http'
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'text/plain; charset=utf-8')],
    })
    await send({
        'type': 'http.response.body',
        'body': b'hello, asgi',
    })
```

把它和 7.1 节的同步模型（WSGI）放在一起对照，可以清楚看到四处关键差异：

| 对比项 | WSGI | ASGI |
|---|---|---|
| 应用形态 | 普通函数 | `async` 函数 |
| 请求信息 | `environ` 字典一次给全 | `scope` 描述连接 + `receive` 持续接收事件 |
| 响应方式 | `return` 一个可迭代对象 | `await send(...)` 分次发送 |
| 协议能力 | 仅 HTTP 短连接 | HTTP 短连接 + 长连接（WebSocket） |

第三行是重点：**ASGI 的响应是"分次发送"而不是"一次返回"**，所以它天然支持流式输出与双向通信。

### 7.3 事件循环：并发模型变了

这是本文最重要的一节。

FastAPI 运行在 ASGI 服务器（通常是 uvicorn）之上，服务器内部有一个**事件循环**。所有 `async def` 接口都在这个循环里执行：

```
事件循环（单线程）
  ├─ 请求 A 进入 async 接口 ── await 等待数据库 ──> 让出控制权
  ├─ 请求 B 进入 async 接口 ── await 等待外部接口 ──> 让出控制权
  └─ 数据库返回 ──> 继续执行请求 A ──> 返回响应
```

与 WSGI 的根本区别：

| | WSGI（Flask 同步） | ASGI（FastAPI 异步） |
|---|---|---|
| 执行单元 | 一个请求占一个线程 | 所有请求共享一个事件循环 |
| 遇到等待 | 线程被占用，只能干等 | `await` 主动让出，循环去处理别的请求 |
| 并发能力 | 受线程数限制 | 单线程可支撑大量并发 IO |
| 阻塞代码的代价 | 拖慢当前请求 | **卡住整个事件循环，所有请求一起变慢** |

请把最后一行读三遍。这就是为什么：

- 在 `async def` 接口里写 `time.sleep(1)`、同步数据库查询、同步 HTTP 请求，是**严重错误**，不是"性能稍差"；
- FastAPI 对此有一个补救设计：**用普通的 `def` 定义的接口，会被自动放进线程池执行**，因此不会阻塞事件循环。详见第 8 章。

### 7.4 适用边界

| 场景 | 是否适合 | 原因 |
|---|---|---|
| AI/大模型应用后端 | 适合 | 主流 SDK 与生态（LangChain、Dify 等）以 FastAPI 为标准 |
| 高并发、大量 IO 等待 | 适合 | 异步模型下等待不占线程 |
| 需要 WebSocket 的服务 | 适合 | 原生支持长连接 |
| 需要自动接口文档的团队协作 | 适合 | OpenAPI 文档由类型注解自动生成 |
| 以 CPU 密集计算为主的服务 | 需谨慎 | 计算仍会占用事件循环，须交给进程池 |
| 教学演示 HTTP 处理细节 | 不如 Flask 直观 | 异步机制引入了一层间接 |


---

## 8 异步与并发

这是全文最关键、也最容易出错的一章。

### 8.1 事件循环里绝不能阻塞

回顾 7.3 节：所有 `async def` 接口共享一个事件循环。所谓"阻塞"，指的是**一段代码在执行期间不让出控制权**。常见的阻塞操作：

| 操作 | 是否阻塞事件循环 |
|---|---|
| `time.sleep(1)` | 是 |
| `asyncio.sleep(1)` | 否（正确用法） |
| 同步数据库驱动（如 `pymysql`）查询 | 是 |
| 异步数据库驱动（如 `asyncpg`）查询 | 否 |
| `requests.get(...)` | 是 |
| `httpx.AsyncClient().get(...)` | 否 |
| 大量 CPU 计算（如 Pandas 处理大表） | 是 |
| 读写大文件 | 是 |

### 8.2 后果：一个请求卡住所有人

下面这个实验可以直接在自己机器上复现：

```python
import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


@app.get('/blocking')
async def blocking():
    time.sleep(1)            # 错误：阻塞事件循环 1 秒
    return {'ok': True, 'mode': 'blocking'}


@app.get('/async-sleep')
async def async_sleep():
    await asyncio.sleep(1)   # 正确：让出控制权 1 秒
    return {'ok': True, 'mode': 'async'}
```

同时向 `/blocking` 发起 5 个请求，总耗时约为 **5 秒**——因为事件循环被逐个卡住。把接口换成 `/async-sleep`，5 个并发请求总耗时约为 **1 秒**。

**结论：并发能力取决于"等待时是否让出控制权"，而不是线程数量。**

### 8.3 正确写法一：改用 `def`，交给线程池

FastAPI 有一个非常实用的设计：**用普通 `def` 定义的接口，会被自动放进线程池执行**，不会阻塞事件循环。

```python
import time

from fastapi import FastAPI

app = FastAPI()


@app.get('/sync-ok')
def sync_ok():
    # 用 def 定义，FastAPI 自动放进线程池，因此这里的阻塞是安全的
    time.sleep(1)
    return {'ok': True, 'mode': 'threadpool'}
```

这条规则带来一个非常实用的判断准则：

> **接口内部有阻塞操作（同步数据库、同步 HTTP、文件读写、CPU 计算）时，就用普通 `def`；
> 接口内部全程是异步操作（`await` 异步库）时，才用 `async def`。
> 绝对不要在 `async def` 里调用同步的阻塞函数。**

用 `def` 定义同步接口，是 FastAPI 项目中最常见也最容易被忽视的正确做法。

### 8.4 正确写法二：`async def` + 线程池

当接口本身需要异步能力（例如要 `await` WebSocket 推送），但其中又不得不调用阻塞代码时，需要把阻塞部分显式交给线程池：

```python
import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


def blocking_io() -> str:
    """同步的阻塞操作，例如 pymysql 查询"""
    time.sleep(1)
    return 'query-result'


@app.get('/mixed')
async def mixed():
    loop = asyncio.get_running_loop()
    # 把阻塞函数放进线程池，await 期间事件循环可以继续处理其他请求
    result = await loop.run_in_executor(None, blocking_io)

    # 之后可以继续使用异步能力（如 await 一个推送）
    return {'result': result}
```

`run_in_executor(None, fn, *args)` 的第一个参数传 `None` 表示使用默认线程池；`blocking_io` 及其参数会被在线程池中执行，返回值通过 `await` 拿到。

Python 3.9 起还有一个更简洁的等价写法：

```python
@app.get('/mixed-to-thread')
async def mixed_to_thread():
    result = await asyncio.to_thread(blocking_io)
    return {'result': result}
```

整个流程的形状是：

```
async def 接口
  ├─ await run_in_executor(None, 阻塞函数)   -> 事件循环在此期间处理其他请求
  ├─ await websocket.send_json(...)          -> 异步推送
  └─ return 结果
```

**这就是"同步与异步职责明确拆分"的含义：阻塞的部分交给线程池，事件循环只负责编排与推送。**

### 8.5 CPU 密集任务的正确做法

线程池对"等待型"阻塞（IO）有效，但对"计算型"阻塞无效——因为 Python 的 GIL 决定了同一时刻只有一个线程在执行字节码，线程池并不能让计算变快，还会挤占事件循环。

CPU 密集任务应交给**进程池**：

```python
from concurrent.futures import ProcessPoolExecutor

import asyncio
from fastapi import FastAPI

app = FastAPI()
process_pool = ProcessPoolExecutor(max_workers=4)


def heavy_compute(n: int) -> int:
    return sum(i * i for i in range(n))


@app.get('/compute')
async def compute(n: int = 100000):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(process_pool, heavy_compute, n)
    return {'result': result}
```

### 8.6 常见错误清单

| 错误写法 | 后果 | 正确做法 |
|---|---|---|
| `async def` 里 `time.sleep()` | 阻塞整个事件循环 | 用 `await asyncio.sleep()` |
| `async def` 里用同步数据库驱动 | 同上 | 改用 `def` 接口，或用异步驱动 |
| `async def` 里用 `requests` | 同上 | 用 `httpx.AsyncClient`，或改 `def` |
| 为了"显得异步"把所有接口写成 `async def` | 同步代码在其中反而更危险 | 同步接口写 `def`，让 FastAPI 丢线程池 |
| 在 `async def` 里做大量 CPU 计算 | 事件循环被长时间占用 | 用进程池 |


---

## 9 WebSocket

### 9.1 为什么需要 WebSocket

HTTP 是"客户端问、服务端答"的模式，服务端无法主动给客户端发消息。要让页面实时显示新消息，只能用轮询（每隔几秒请求一次），既浪费资源又有延迟。

WebSocket 在一条 TCP 连接上提供**全双工**通道：连接建立后，双方都可以随时发消息。FastAPI 原生支持。

### 9.2 最小示例

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.websocket('/ws/echo')
async def ws_echo(websocket: WebSocket):
    await websocket.accept()                 # 必须先接受连接
    try:
        while True:
            text = await websocket.receive_text()
            await websocket.send_text(f'echo: {text}')
    except WebSocketDisconnect:
        print('客户端断开')
```

用浏览器控制台就能测试：

```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/ws/echo');
ws.onmessage = (e) => console.log('收到:', e.data);
ws.onopen = () => ws.send('hello');
```

几个要点：

1. 装饰器是 `@app.websocket` 而不是 `@app.get`；
2. **必须先 `await websocket.accept()`**，否则连接会被拒绝；
3. 用 `try/except WebSocketDisconnect` 处理客户端断开——这是正常流程，不是异常；
4. 连接处理函数本身必须是 `async def`（WebSocket 无法同步处理）。

### 9.3 连接管理器：向多个客户端广播

实际业务中，服务端需要向**所有**在线客户端推送同一份数据（例如工作台的会话列表变更）。这需要一个连接注册表：

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    """管理在线连接，支持定向发送与广播"""

    def __init__(self):
        self._rooms: dict[str, set[WebSocket]] = {}

    async def connect(self, key: str, websocket: WebSocket):
        await websocket.accept()
        self._rooms.setdefault(key, set()).add(websocket)

    def disconnect(self, key: str, websocket: WebSocket):
        conns = self._rooms.get(key)
        if conns is None:
            return
        conns.discard(websocket)
        if not conns:
            del self._rooms[key]

    async def send_to(self, key: str, data: dict):
        """向某个房间的所有连接推送（定向）"""
        for ws in list(self._rooms.get(key, ())):
            try:
                await ws.send_json(data)
            except Exception:
                self.disconnect(key, ws)

    async def broadcast(self, data: dict):
        """向所有房间推送（广播）"""
        for key in list(self._rooms):
            await self.send_to(key, data)


manager = ConnectionManager()


@app.websocket('/ws/chat/{session_id}')
async def ws_chat(websocket: WebSocket, session_id: str):
    await manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('type') == 'ping':
                await websocket.send_json({'type': 'pong'})
            else:
                # 收到消息后，同时回复自己并广播给其他客户端
                await manager.send_to(session_id, {'type': 'echo', 'data': data})
    except WebSocketDisconnect:
        manager.disconnect(session_id, websocket)
```

两个工程要点：

1. **推送时逐个连接 `try/except`**。一条连接断开不能让整个广播失败，捕获异常后把该连接从注册表移除即可；
2. **列表要先复制再遍历**（`list(...)`）。因为遍历过程中可能修改字典，直接遍历会抛 `RuntimeError: dictionary changed size during iteration`。

### 9.4 心跳保活

长连接可能被中间设备（代理、网关）静默断开。约定一个心跳消息定期往返，可以及时发现断线：

```python
@app.websocket('/ws/heartbeat')
async def ws_heartbeat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('type') == 'ping':
                await websocket.send_json({'type': 'pong'})
    except WebSocketDisconnect:
        pass
```

客户端每 30 秒发一次 `{"type": "ping"}`，收到 `pong` 即认为连接正常。


---

## 10 应用工厂与 lifespan

### 10.1 为什么用应用工厂

`main.py` 里直接 `app = FastAPI()` 的写法在项目变大后会难以测试——测试需要独立的应用实例，而模块级单例无法重复创建。工厂模式把"组装应用"与"启动应用"解耦：

```python
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title='Demo API', version='1.0.0')

    # 在这里注册路由、中间件、异常处理器
    app.include_router(...)

    return app


app = create_app()      # 供 uvicorn 以 "main:app" 导入
```

### 10.2 lifespan：启动与关闭的钩子

需要在服务启动时初始化连接池、拉起后台任务，在关闭时释放资源，用 `lifespan` 声明：

```python
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI


async def background_loop():
    """后台周期任务：每 60 秒执行一次"""
    while True:
        await asyncio.sleep(60)
        # 这里做超时数据归档、缓存清理等工作
        print('后台任务执行一次')


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- 启动阶段 ----
    print('服务启动：初始化连接池')
    task = asyncio.create_task(background_loop())

    yield                     # 应用在此运行

    # ---- 关闭阶段 ----
    task.cancel()
    print('服务关闭：回收资源')


app = FastAPI(lifespan=lifespan)
```

要点：

1. `lifespan` 是一个**异步上下文管理器**，`yield` 之前的代码在启动时执行，之后的在关闭时执行；
2. 后台任务用 `asyncio.create_task()` 拉起，关闭时必须 `cancel()`，否则进程无法干净退出；
3. 不要使用 `@app.on_event("startup")` / `@app.on_event("shutdown")`——这套写法已被标记为过时，官方推荐统一使用 `lifespan`；
4. **`lifespan` 与 `on_event` 不能混用**：一旦提供 `lifespan` 参数，`startup`/`shutdown` 事件处理器将全部失效。

### 10.3 容错启动

一个实用的设计：数据库瞬时不可用时，服务仍应启动成功，等数据库恢复后自动可用。

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db_pool()          # 连接池初始化
    except Exception as e:
        # 只告警不退出：数据接口暂时不可用，恢复后自动重连
        print(f'数据库连接失败（数据接口将不可用）：{e}')

    task = asyncio.create_task(background_loop())
    yield
    task.cancel()
```

配合"连接池惰性建连"（每次执行 SQL 时才真正取连接），就能做到数据库恢复后无需重启服务。


---

## 11 中间件与 CORS

### 11.1 自定义中间件

中间件在**每个请求进入接口之前**与**响应返回客户端之前**执行，适合做耗时统计、请求 ID 注入、统一日志：

```python
import time
import uuid

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    request_id = uuid.uuid4().hex[:8]
    start = time.perf_counter()

    response = await call_next(request)      # 调用后续处理链

    cost = time.perf_counter() - start
    response.headers['X-Request-Id'] = request_id
    response.headers['X-Process-Time'] = f'{cost:.4f}'
    return response
```

需要注意：`call_next` 只能 `await` 一次；中间件里如果抛异常，后面的接口不会被执行。

### 11.2 CORS

浏览器出于同源策略，会拦截跨域请求。前端（如 `http://localhost:5173`）调用后端（`http://localhost:8000`）时，需要在后端声明允许的来源：

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],   # 生产环境务必写明确来源
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
```

**安全提示**：`allow_origins=['*']` 与 `allow_credentials=True` 不应同时使用。前者表示允许任意站点访问，在生产环境等于放弃同源保护。


---

## 12 项目结构分层实践

单个文件写不了几个接口就会失控。推荐按职责分层：

```
project/
├── main.py                 # 应用工厂 + lifespan + 异常映射
├── config/
│   └── config.json         # 配置（与代码分离）
├── schemas/
│   └── models.py           # Pydantic 请求/响应模型
├── dao/
│   ├── db_pool.py          # 连接池
│   └── user_dao.py         # 数据访问，只写 SQL
├── services/
│   └── user_service.py     # 业务逻辑编排
├── api/
│   ├── deps.py             # 公共依赖（统一响应、鉴权）
│   ├── user.py             # 用户路由（APIRouter）
│   └── ws.py               # WebSocket 路由
├── common/
│   ├── constants.py        # 常量与枚举
│   ├── exceptions.py       # 自定义异常
│   └── logger.py           # 日志
└── static/                 # 前端页面（如有）
```

路由用 `APIRouter` 拆分，与 Flask 的 Blueprint 作用相同：

```python
# api/user.py
from fastapi import APIRouter

router = APIRouter(prefix='/api/users', tags=['用户'])


@router.get('/{user_id}')
def get_user(user_id: int):
    return {'code': 200, 'data': {'id': user_id}}
```

```python
# main.py
from fastapi import FastAPI
from api.user import router as user_router

app = FastAPI()
app.include_router(user_router)
```

分层原则只有一条：**上层依赖下层，下层不感知上层**。

- `api` 只做参数解析与响应返回，不写业务判断；
- `services` 只写业务逻辑，不碰 HTTP 对象，也不写 SQL；
- `dao` 只写 SQL，不写业务规则；
- `schemas` 被各层共用，只描述数据结构。

这样分层的收益很实在：换掉数据层实现时，`services` 与 `api` 不用改；给 `services` 写单元测试时，不需要启动 Web 服务。


---

## 13 常见错误与排查

| 报错 / 现象 | 原因 | 解决 |
|---|---|---|
| `422 Unprocessable Entity` | 请求体或参数不符合模型约束 | 看响应体 `detail[].loc` 定位字段；参数字段缺失也会触发 |
| 接口返回 `{"detail": ...}` 与团队格式不一致 | FastAPI 默认错误格式 | 注册 `RequestValidationError` 与 `AppError` 异常处理器 |
| 接口报 `Field required` 但字段明明传了 | 参数被当成查询参数而非请求体 | 请求体必须用 Pydantic 模型声明，简单类型默认按查询参数解析 |
| `@app.on_event` 不生效 | 与 `lifespan` 混用导致被忽略 | 统一改用 `lifespan` |
| 改了代码不生效 | 未开热重载 | 用 `fastapi dev main.py` 或 `uvicorn main:app --reload` |
| 所有接口一起变慢，日志显示卡在某个接口 | `async def` 里出现了阻塞调用 | 该接口改为 `def`，或把阻塞部分放进 `run_in_executor` |
| WebSocket 连接立刻被关闭 | 没有调用 `websocket.accept()` | 在处理函数开头接受连接 |
| WebSocket 广播时抛 `dictionary changed size during iteration` | 遍历中修改了字典 | 遍历前先 `list(...)` 复制 |
| `RuntimeError: no running event loop` | 在同步函数里调用了 `asyncio.get_running_loop()` | 该函数应在 `async def` 中调用，或改用 `asyncio.run()` |
| 跨域请求被浏览器拦截 | 未配置 CORS | 添加 `CORSMiddleware` |
| 启动时数据库连不上，服务直接退出 | 初始化未做容错 | `lifespan` 中捕获异常并告警，配合连接池惰性建连 |

排查接口参数问题最有效的手段是打开 `/docs`，在 Swagger UI 里直接试调——页面上会显示每个参数的来源与约束，多数"参数传了却没收到"的问题一眼可见。


---

## 14 练习任务

### 练习 1（基础）

用 FastAPI 实现图书接口服务：

1. `GET /api/books` 支持 `keyword`（可选字符串）、`page`（默认 1，最小 1）、`size`（默认 10，范围 1 到 100）三个查询参数；
2. `GET /api/books/{book_id}`，`book_id` 必须大于等于 1，否则返回 422；
3. `POST /api/books` 请求体包含 `title`（1 到 100 字符，必填）、`author`（默认空串）、`price`（大于等于 0，默认 0）；
4. 用 `response_model` 保证响应只暴露 `id`、`title`、`author`、`price` 四个字段。

作答区：

```
（在此处写出你的代码）
```

### 练习 2（校验器与响应模型）

为练习 1 增加以下要求：

1. `title` 在校验时自动去除首尾空格，去空格后为空则报错；
2. `isbn` 字段接受带连字符的输入（如 `978-7-111-12345-6`），但在模型内部统一存成纯数字；
3. 新增 `UserIn` / `UserOut` 两个模型，`UserIn` 含 `name` 与 `password`，`UserOut` 只含 `name`，验证 `response_model` 确实过滤了 `password`。

作答区：

```
（在此处写出你的代码）
```

### 练习 3（依赖注入）

实现一个 `CurrentStaff` 类依赖：

1. 从请求头 `X-Staff-Id` 读取咨询师 id；
2. 请求头缺失时抛出 401，`detail` 为 `缺少 X-Staff-Id 请求头，请先登录`；
3. 再写一个 `pagination` 函数依赖，提供 `page`、`size`、`offset` 三个值；
4. 组合出一个 `GET /api/staff/sessions` 接口，同时使用这两个依赖。

作答区：

```
（在此处写出你的代码）
```

### 练习 4（异步与并发，重点）

下面的接口在并发压测时会导致整个服务变慢，请指出原因并给出两种修改方案。

```python
import time

from fastapi import FastAPI

app = FastAPI()


@app.get('/report')
async def report():
    time.sleep(2)          # 模拟同步数据库查询
    return {'ok': True}
```

作答区：

```
（在此处写出你的分析、两种修改方案，以及判断一个接口该用 def 还是 async def 的准则）
```

### 练习 5（WebSocket）

实现一个 WebSocket 聊天接口 `/ws/room/{room_id}`：

1. 支持多个客户端加入同一房间；
2. 任一客户端发送的消息，广播给该房间的所有客户端；
3. 客户端断开时从房间中移除；某个连接推送失败时不影响同一房间的其他连接；
4. 支持 `{"type": "ping"}` 心跳，回复 `{"type": "pong"}`。

作答区：

```
（在此处写出你的代码）
```


---

## 15 参考答案与评价要点

### 练习 1 参考答案

```python
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(title='Book API')

BOOKS = [
    {'id': 1, 'title': 'Python 编程基础', 'author': '张三', 'price': 59.0},
    {'id': 2, 'title': 'Web 开发入门', 'author': '李四', 'price': 69.0},
]


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100, description='书名')
    author: str = Field(default='', max_length=50, description='作者')
    price: float = Field(default=0.0, ge=0, description='价格')


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    price: float


@app.get('/api/books', response_model=list[BookOut])
def list_books(
    keyword: str = '',
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    rows = [b for b in BOOKS if keyword in b['title']] if keyword else BOOKS
    start = (page - 1) * size
    return rows[start:start + size]


@app.get('/api/books/{book_id}', response_model=BookOut)
def get_book(book_id: Annotated[int, Path(ge=1)]):
    for b in BOOKS:
        if b['id'] == book_id:
            return b
    raise HTTPException(status_code=404, detail='图书不存在')


@app.post('/api/books', response_model=BookOut, status_code=201)
def create_book(book: BookCreate):
    new_id = max([b['id'] for b in BOOKS], default=0) + 1
    row = {'id': new_id, 'title': book.title,
           'author': book.author, 'price': book.price}
    BOOKS.append(row)
    return row
```

**评价要点**

1. `book_id: Annotated[int, Path(ge=1)]` 是否使用了 `Path` 约束——漏掉时 `book_id=0` 会进入函数体；
2. **没有手写任何校验分支**：`title` 长度、`price` 范围都由 `Field` 完成，这是本节的核心考点；
3. `response_model` 是否声明，`list[BookOut]` 的写法是否正确；
4. `POST` 是否返回 201；
5. 是否误用 `async def`——本练习全是同步的内存操作，用 `def` 即可。

### 练习 2 参考答案

```python
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from fastapi import FastAPI, HTTPException

app = FastAPI()


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(default='', max_length=50)
    price: float = Field(default=0.0, ge=0)
    isbn: str = Field(default='', description='ISBN，可带连字符')

    @field_validator('title')
    @classmethod
    def strip_title(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError('title 不能为空白字符')
        return cleaned

    @field_validator('isbn')
    @classmethod
    def normalize_isbn(cls, value: str) -> str:
        cleaned = value.replace('-', '').strip()
        if cleaned and (len(cleaned) not in (10, 13) or not cleaned.isdigit()):
            raise ValueError('ISBN 必须是 10 位或 13 位数字')
        return cleaned


class UserIn(BaseModel):
    name: str
    password: str


class UserOut(BaseModel):
    name: str


@app.post('/api/users', response_model=UserOut)
def create_user(user: UserIn):
    # 故意把 password 一起返回，验证 response_model 会过滤掉它
    return {'name': user.name, 'password': user.password}
```

验证响应过滤（可直接放到测试里）：

```python
from fastapi.testclient import TestClient

client = TestClient(app)
resp = client.post('/api/users', json={'name': '张三', 'password': 'secret'})
assert resp.status_code == 200
assert resp.json() == {'name': '张三'}, resp.json()     # password 已被过滤
```

**评价要点**

1. `@field_validator` 是否配了 `@classmethod`（Pydantic v2 的要求，最容易漏）；
2. 校验器中抛的是 `ValueError` 而不是 `HTTPException`——校验器里不应感知 HTTP 语义；
3. 是否理解"校验器返回值会替换原值"，因此可以用它做数据清洗；
4. 是否验证了 `response_model` 的过滤行为，而不是只声明未验证。

### 练习 3 参考答案

```python
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query

app = FastAPI()


class CurrentStaff:
    """从请求头解析当前咨询师身份"""

    def __init__(self, x_staff_id: Annotated[int | None, Header()] = None):
        if x_staff_id is None:
            raise HTTPException(status_code=401,
                                detail='缺少 X-Staff-Id 请求头，请先登录')
        self.staff_id = x_staff_id

    @property
    def display(self) -> str:
        return f'staff-{self.staff_id}'


def pagination(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
) -> dict:
    return {'page': page, 'size': size, 'offset': (page - 1) * size}


@app.get('/api/staff/sessions')
def list_sessions(
    staff: Annotated[CurrentStaff, Depends(CurrentStaff)],
    pager: Annotated[dict, Depends(pagination)],
):
    return {'viewer': staff.display, 'pager': pager, 'sessions': []}
```

**评价要点**

1. 未登录时是否返回 401——在依赖里抛 `HTTPException`，接口函数不会被执行；
2. `pagination` 是否把 `offset` 一并算好返回，而不是让每个接口各算一遍；
3. 两个依赖是否都能正常注入（顺序不影响）；
4. 是否理解"同一请求内同一依赖只执行一次"的缓存行为。

### 练习 4 参考答案

**问题定位**：`report` 声明为 `async def`，因此它运行在事件循环里；而 `time.sleep(2)` 是阻塞调用，执行期间不会让出控制权。在这 2 秒内，事件循环无法处理任何其他请求——包括其他用户对完全无关接口的请求。所以是"一个接口拖垮整个服务"，而不是只拖慢自己。

**方案一：改为普通 `def`，交给线程池**

```python
@app.get('/report')
def report():
    time.sleep(2)
    return {'ok': True}
```

FastAPI 检测到接口是同步函数，会自动在线程池中执行，事件循环不被阻塞。

**方案二：保持 `async def`，把阻塞部分放进线程池**

```python
import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


def blocking_query():
    time.sleep(2)
    return True


@app.get('/report')
async def report():
    loop = asyncio.get_running_loop()
    ok = await loop.run_in_executor(None, blocking_query)
    return {'ok': ok}
```

**判断准则**

| 接口内部情况 | 选择 | 理由 |
|---|---|---|
| 有同步阻塞调用（同步数据库、`requests`、文件读写、CPU 计算） | 用 `def` | FastAPI 自动丢线程池，不会阻塞事件循环 |
| 全程是异步调用（`await` 异步库） | 用 `async def` | 才能真正发挥异步优势 |
| 既需要异步能力（如 `await` WebSocket 推送），又有阻塞调用 | 用 `async def` + `run_in_executor` | 阻塞部分进线程池，事件循环只做编排 |

**一句话准则：不要在 `async def` 里写同步的阻塞代码；有阻塞代码，就应该让它在 `def` 里，或显式交给线程池。**

**评价要点**

1. 能否指出"阻塞的是事件循环、影响的是所有请求"，而不是说"性能不好"；
2. 两种方案是否都给出，并说明各自适用场景；
3. 是否理解 `def` 自动进线程池这一 FastAPI 特性——很多人不知道它，反而把所有接口都写成 `async def`。

### 练习 5 参考答案

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class RoomManager:
    """按房间管理 WebSocket 连接"""

    def __init__(self):
        self._rooms: dict[str, set[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self._rooms.setdefault(room_id, set()).add(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        conns = self._rooms.get(room_id)
        if conns is None:
            return
        conns.discard(websocket)
        if not conns:
            del self._rooms[room_id]

    async def broadcast(self, room_id: str, data: dict):
        # 先复制成列表，避免遍历时修改字典
        for ws in list(self._rooms.get(room_id, ())):
            try:
                await ws.send_json(data)
            except Exception:
                # 单条连接失败不影响其他连接
                self.disconnect(room_id, ws)


manager = RoomManager()


@app.websocket('/ws/room/{room_id}')
async def ws_room(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('type') == 'ping':
                await websocket.send_json({'type': 'pong'})
                continue
            await manager.broadcast(room_id, {'type': 'message', 'data': data})
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
```

**评价要点**

1. 是否先 `await websocket.accept()`；
2. 广播前是否 `list(...)` 复制——不复制会在有连接断开时报 `dictionary changed size during iteration`；
3. 单条发送是否 `try/except` 并移除失效连接；
4. 断开时是否清理空房间，避免内存泄漏；
5. 心跳是否用 `continue` 与业务消息分开处理。


---

## 16 衔接：从框架到项目

至此你已经掌握了两套框架的基本用法。把它们放回一个真实项目时，还会遇到：

1. **配置与代码分离**：连接池参数、限流阈值、话术模板都应写在配置文件里，而不是散落在代码中；
2. **分层与依赖方向**：`api → service → dao`，上层依赖下层，下层不感知上层；
3. **可替换的 AI 引擎**：把"回答生成"抽象成一个接口，规则引擎与大模型实现都实现这个接口，业务代码只依赖接口——这是抽象基类（多态）在工程中的典型用法；
4. **同步与异步的边界**：项目中 `def` 与 `async def` 接口混用不是风格问题，而是每个接口按其内部是否阻塞来决定的。

---

## 附录 A 教师使用说明

> 本节供授课教师参考，不属于学员讲义正文，讲授时可整体略过。

### A.1 课时安排建议（共 3 课时）

| 课时 | 讲授内容 | 课堂演示建议 |
|---|---|---|
| 第 1 课时 | 第 1 章（认识 Web 与 FastAPI）、第 2 章（跑起第一个程序与 `/docs`）、第 3 章（路径与参数） | 先讲"输入网址后发生了什么"；跑起程序后打开 `/docs`，直接在页面上调接口，让学生看到"零文档代码"的效果 |
| 第 2 课时 | 第 4 章（Pydantic）、第 5 章（Depends）、第 6 章（错误处理） | 故意传错参数，展示 422 的 `loc` 定位能力；注册异常处理器后，展示错误格式如何统一 |
| 第 3 课时 | 第 7 章（ASGI 原理）、第 8 章（异步与并发，重点）、第 9 章（WebSocket） | 现场并发压测 `/blocking` 与 `/async-sleep`，用耗时对比证明事件循环阻塞的后果 |

第 10–13 章可作为项目实战前的预习材料。

### A.2 讲授侧重点

1. **第 1 章是"地基"，务必讲慢**。确认学生能复述"输入网址后发生了什么"、能区分前端与后端，再往下走；厨师煮汤的异步类比建议在这里就埋下伏笔。
2. **第 7、8 章是全文核心，务必留足时间**。建议现场做那个实验：同时发 5 个请求到 `/blocking`，让学生看着计时器从 1 秒变成 5 秒，再对比 `/async-sleep` 的 1 秒。这比讲原理有效得多。
3. **`def` 自动进线程池这一点必须强调**。很多学员学完 FastAPI 会陷入"所有接口都该是 `async def`"的误区，反而制造阻塞问题。
4. **Pydantic v1/v2 差异要提醒**。学员上网搜到的教程大量是 v1 写法，会直接报错，第 4.6 节的速查表建议让学生保存。
5. 本文是**自包含**的，不要求学生先学 Flask；若学生已了解 Flask，可在讲解同步/异步时顺带对比，但不作为理解前提。

### A.3 常见学员疑问

| 疑问 | 回答要点 |
|---|---|
| 既然 `def` 会自动进线程池，那 `async def` 还有什么意义？ | 只有真正的异步 IO 才能带来并发收益。`def` 靠线程池，线程数量有限且切换有开销；`async def` 在单线程上就能支撑大量并发等待。 |
| 为什么不干脆全部用 `async def` + `run_in_executor`？ | 可以，但代码更啰嗦。既然 FastAPI 已经为 `def` 自动做了这件事，同步接口直接用 `def` 更简洁。 |
| `Depends` 和 Flask 的装饰器有什么区别？ | 装饰器是"包裹函数"，依赖注入是"声明参数"。后者更显式，且依赖可以被嵌套、缓存和单独测试。 |
| 422 能不能改成 400？ | 可以，注册 `RequestValidationError` 异常处理器即可，见第 6.3 节。 |
| WebSocket 需要额外装库吗？ | 不需要。但用 uvicorn 时建议安装 `uvicorn[standard]`，其中包含 WebSocket 协议实现。 |
| `lifespan` 和 `@app.on_event` 能一起用吗？ | 不能。一旦提供 `lifespan`，`on_event` 的处理器会全部失效。 |

### A.4 与项目的接口

本文结束后，学员应能把以下概念对应到"心聆 MindEcho"项目的代码位置上：

| 本文概念 | 项目中的落点 |
|---|---|
| `APIRouter` 分层 | `aiservice/api/` 下的 5 个路由模块 |
| Pydantic 校验与响应模型 | `aiservice/schema/models.py` |
| `Depends` 鉴权 | `aiservice/api/deps.py` 的 `get_staff` |
| 自定义异常与异常处理器 | `aiservice/common/exceptions.py` + `main.py` 的三级异常映射 |
| `lifespan` 生命周期与后台任务 | `aiservice/main.py` |
| `def` 与 `async def` 的边界 | `api/chat.py`（同步 `def`）与 `api/ws.py`（异步） |
| `run_in_executor` 拆分阻塞与异步 | `service/chat_service.py` 的 `handle_chat` |
| WebSocket 连接管理 | `service/ws_manager.py` 与 `staff_ws_manager.py` |
| 同步与异步职责分离 | `service/staff_service.py` 的"入库 + 推送"两步拆分 |
