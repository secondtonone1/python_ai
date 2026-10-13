# Flask 技术文档

> 前置课程讲义 · Web 框架入门
>
> 适用版本：Flask 3.x（本文全部示例在 Flask 3.0.3 + Python 3.12 上运行验证通过）
>
> 前置知识：会基础 Python（函数、面向对象、装饰器、上下文管理器 `with`）。**不要求你事先了解任何 Web 知识**——我们从"在浏览器输入一个网址"讲起。

---

## 1 从一个网址说起：认识 Web 与 Flask

在写第一行代码之前，我们先花点时间弄清楚几个最基本的问题：我们每天打开的网页到底是什么？在浏览器里输入一个网址后发生了什么？我们这门课要写的程序，在其中扮演什么角色？把这些想明白，后面的所有概念都会顺理成章。

### 1.1 你每天都在使用 Web

用浏览器看新闻、查资料、购物、用网页版邮箱，乃至很多手机 App 里点开的页面——它们都有一个共同点：

- 你在一个**客户端**（绝大多数时候是浏览器）上操作；
- 背后有一台（实际是很多台）远方的**服务器**在为你服务。

你在浏览器里看到的文字、图片、按钮、视频，不是凭空出现在屏幕上的，而是**服务器通过网络"送"过来的**。我们这门课要学的，就是怎么用 Python 写出"送出这些内容"的服务器程序。

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

请记住这种对话的两个特点：**一问一答、答完即结束**。浏览器不主动发问，服务器就不会主动说话——这一点在以后讲 WebSocket（让服务器能主动推送）时还会提到。

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

### 1.5 Flask 是什么

**Flask 是一个用 Python 编写的、轻量级的 Web 框架**，用来快速搭建网站和 Web 接口（也就是后端）。它有几个鲜明的特点：

- **小而精（微内核）**：核心只提供"路由 + 请求/响应处理"这两件最基本的事，不替你做太多决定；
- **好上手**：一个最小程序只要几行代码，非常适合用来理解 Web 到底是怎么运转的；
- **可扩展**：需要数据库、表单校验、登录等能力时，再按需安装对应的扩展，像搭积木一样一点点加上去；
- **生态成熟、使用者众多**：大量公司的内部工具、中小型网站和教学项目都在用，遇到问题很容易搜到答案。

为了帮你建立定位，我们把 Web 框架粗略分成两种风格：

- 一种是"**大而全、精装修拎包入住**"的，典型代表是 Django——它把数据库、后台管理、表单、认证等全部给你配好，约定也很多；
- 另一种是"**小而灵活**"的，代表就是 Flask——核心简洁，需要什么自己装。

**教学先讲 Flask 是有原因的**：正因为它"小"，你才能看清一座 Web 应用是怎么一砖一瓦盖起来的，不被一大堆现成功能淹没。等你理解了最本质的东西，再去学更"大"的框架或更"快"的框架（如 FastAPI），都会轻松很多。

**Flask 适合做什么**：学习 Web 原理、中小型网站、公司内部工具、以数据库增删改查（CRUD）为主的服务、快速验证想法的原型。

**Flask 不太擅长什么**：海量的实时长连接（比如聊天服务器）、超高并发的场景——这些正是 FastAPI 等现代框架的舞台，在后续课程中你会接触到。

### 1.6 本文的学习路线

下面是我们接下来的行进路线，你可以把它当成一张地图，随时知道自己走到了哪：

| 阶段 | 章节 | 在干什么 |
|---|---|---|
| ① 先跑起来 | 第 2 章 | 装好 Flask，写出第一个能在浏览器访问的程序，先获得成就感 |
| ② 学会基本操作 | 第 3、4 章 | 把不同网址对应到不同函数（路由）；读取浏览器发来的数据、返回结果（请求与响应） |
| ③ 打通原理 | 第 5、6 章 | 会写接口后，回头看"请求究竟是怎么到达你函数的"（WSGI），以及 `request` 为什么能直接用（上下文） |
| ④ 进阶能力 | 第 7–13 章 | 模板、蓝图（拆分大项目）、错误处理与日志、数据库、配置管理、部署上线 |
| ⑤ 动手巩固 | 第 14、15 章 | 练习题与参考答案 |

最重要的学习建议只有一条：**边看边敲**。每一个示例都请亲手在自己电脑上运行，然后试着改一改——把返回的文字换成自己的名字、加一条新的路径，观察发生了什么。Web 开发是"做"会的，不是"读"会的。

### 1.7 学习目标

带着路线图，下面是学完本文后你应当达到的目标（现在不必完全看懂，学完再回来对照）：

1. 说清浏览器与服务器之间"请求—响应"的过程，以及 Web 框架到底帮我们做了哪些重复工作；
2. 独立写出带路由、路径参数、查询参数和 JSON 响应的 Flask 接口；
3. 在写过接口的基础上，说清 WSGI 是什么、Flask 在其中处于什么位置，以及它"一个请求占用一个执行单元"的同步特点；
4. 解释为什么视图函数不用接收 `request` 参数却能直接使用它，并说明上下文的作用范围；
5. 用蓝图（Blueprint）把一个多模块应用拆开；
6. 用统一的方式处理业务异常，并写出会按大小自动轮转的日志；
7. 用连接池访问 MySQL，并解释参数化查询为什么能防止 SQL 注入。

准备好了吗？我们从安装 Flask、跑起第一个程序开始。


---

## 2 环境准备与最小应用

### 2.1 安装

```bash
pip install flask
```

确认版本：

```bash
python -c "import importlib.metadata as m; print(m.version('flask'))"
```

> 说明：Flask 3.1 起 `flask.__version__` 属性已被移除，请改用上面的 `importlib.metadata` 方式读取版本号。

### 2.2 最小应用

新建 `app.py`：

```python
from flask import Flask

app = Flask(__name__)


@app.get('/')
def index():
    # 直接返回 dict（Flask 1.1+ 会自动转成 JSON 响应）
    return {'message': 'hello flask'}


@app.get('/health')
def health():
    return {'status': 'up'}
```

`Flask(__name__)` 传入模块名，框架据此定位模板目录与静态文件目录（默认相对于该模块所在目录）。

### 2.3 启动方式

方式一，命令行（推荐）：

```bash
flask --app app run --debug
```

- `--app app` 指定应用所在的模块（模块中需存在名为 `app` 或 `application` 的实例，或用 `--app app:变量名` 指定）；
- `--debug` 同时开启**交互式调试器**与**自动重载**，改完代码保存即生效。

方式二，从 Python 代码启动：

```python
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
```

两种方式等价，但 `--debug` 写在命令行更灵活。`debug=True` 时页面报错会显示带代码执行的调试器，**它只能在开发环境使用**，线上开启等于把服务器交出去。

> 注意：`@app.before_first_request` 这个装饰器在 Flask 3.0 已被彻底移除。需要在启动时执行的初始化逻辑，请改为在创建应用时直接执行，或放入应用工厂函数。


---

## 3 路由系统

### 3.1 路由与视图函数

装饰器把 URL 规则绑定到函数：

```python
@app.route('/books', methods=['GET', 'POST'])
def books():
    return {'ok': True}
```

Flask 2.0 起为常用方法提供了快捷装饰器，与上面写法等价：

```python
@app.get('/books')
def list_books():
    return {'books': []}


@app.post('/books')
def create_book():
    return {'created': True}, 201
```

**视图函数的返回值**支持三种形式，这是新手最容易困惑的地方：

| 返回值 | 含义 |
|---|---|
| `'text'` 或 `{'k': 'v'}` | 响应体，状态码默认 200（`dict` 自动转 JSON） |
| `('text', 201)` | 二元组：响应体 + 状态码 |
| `('text', 201, {'X-Trace': 'abc'})` | 三元组：响应体 + 状态码 + 响应头字典 |

### 3.2 变量规则与转换器

```python
@app.get('/users/<int:user_id>')
def get_user(user_id):
    # user_id 已经是 int 类型，转换失败会直接返回 404，不会进入本函数
    return {'user_id': user_id, 'type': str(type(user_id))}


@app.get('/files/<path:file_path>')
def get_file(file_path):
    # path 转换器允许斜杠，适合处理 a/b/c.txt 这类路径
    return {'path': file_path}
```

| 转换器 | 匹配内容 | 说明 |
|---|---|---|
| `string`（默认） | 不含斜杠的任意文本 | 不写转换器即为此类型 |
| `int` | 非负整数 | 转换失败返回 404 |
| `float` | 浮点数 | |
| `uuid` | UUID 字符串 | 常用于资源 ID |
| `path` | 含斜杠的路径 | 会吞掉后续斜杠 |

### 3.3 查询参数

查询参数（URL 中 `?` 之后的部分）通过 `request.args` 读取：

```python
from flask import request


@app.get('/search')
def search():
    keyword = request.args.get('keyword', '')
    page = request.args.get('page', 1, type=int)      # 指定类型，转换失败用默认值
    tags = request.args.getlist('tag')                 # 同名参数出现多次时用它
    return {'keyword': keyword, 'page': page, 'tags': tags}
```

注意 `request.args.get()` 与 `type=int` 的行为：`type` 转换失败时**返回默认值而不报错**，所以它适合做有默认值的可选参数；必填参数应显式校验：

```python
@app.get('/search')
def search():
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        return {'code': 400, 'message': 'keyword 不能为空'}, 400
    return {'code': 200, 'data': {'keyword': keyword}}
```

### 3.4 url_for：不要硬编码 URL

```python
from flask import url_for


@app.get('/users/<int:user_id>')
def get_user(user_id):
    # 生成 /users/42，而不是手写 '/users/' + str(user_id)
    return {'url': url_for('get_user', user_id=42)}
```

`url_for` 的第一个参数是**端点名**，默认等于视图函数名。它的价值：改动路由规则时只需改装饰器一处，所有由 `url_for` 生成的链接自动同步；它还负责处理特殊字符转义。


---

## 4 请求与响应

### 4.1 请求对象 `request`

`request` 封装了当前请求的全部信息：

| 属性 / 方法 | 用途 |
|---|---|
| `request.method` | 请求方法 |
| `request.path` | 路径（不含查询串） |
| `request.args` | 查询参数（`?a=1`） |
| `request.form` | 表单数据（`application/x-www-form-urlencoded`） |
| `request.json` / `get_json(silent=True)` | JSON 请求体 |
| `request.files` | 上传的文件 |
| `request.headers` | 请求头 |
| `request.remote_addr` | 客户端 IP |

读取 JSON 请求体时，**必须防御非法 JSON**：

```python
from flask import request


@app.post('/echo')
def echo():
    # silent=True 表示解析失败返回 None，而不是抛异常
    data = request.get_json(silent=True)
    if data is None:
        return {'code': 400, 'message': '请求体必须是合法 JSON'}, 400
    return {'code': 200, 'data': data}
```

直接使用 `request.json` 在请求体不是 JSON 时会抛出 415/400 异常；用 `get_json(silent=True)` 自行判断，能给出更可控的错误响应。

### 4.2 响应对象

需要精细控制响应（如设置 Cookie、自定义响应头）时，使用 `jsonify` 或 `make_response`：

```python
from flask import jsonify, make_response


@app.get('/detail')
def detail():
    resp = make_response(jsonify({'code': 200, 'data': {'id': 1}}))
    resp.status_code = 200
    resp.headers['X-App'] = 'demo'
    resp.set_cookie('last_visit', '2026-09-25')
    return resp
```

| 工具 | 使用时机 |
|---|---|
| 返回 `dict` / `str` | 最简单的场景 |
| `jsonify(...)` | 需要构造 JSON 但不需要改响应本身 |
| `make_response(...)` | 需要设置状态码、响应头、Cookie |

### 4.3 Cookie 与 session

```python
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = 'dev-only-change-me'      # session 的签名密钥，必须设置


@app.post('/login')
def login():
    session['user_id'] = 1
    return {'code': 200}


@app.get('/me')
def me():
    return {'user_id': session.get('user_id')}
```

两个常见误解需要澄清：

1. **Flask 默认的 session 存在客户端 Cookie 里，且只做签名、不加密**。用户可以读到里面的内容，只是无法伪造。因此绝不能在 session 里存密码、手机号等信息。
2. 没设置 `app.secret_key` 就写 session，会直接报 `RuntimeError: The session is unavailable because no secret key was set`。


---

## 5 Flask 是怎么跑起来的：理解 WSGI

到目前为止，你已经能写出好几个可以在浏览器访问的接口了。那么你有没有好奇过：浏览器发来的请求，究竟是怎么穿过网络、最终到达你写的那个函数的？框架在这中间到底替我们做了什么？

这一章我们就退到框架背后看个究竟。这套机制有一个正式的名字，叫 **WSGI**——理解它之后，你不仅能回答上面的问题，也为以后看懂 FastAPI 的不同工作方式打好基础。

### 5.1 框架解决的是什么问题

假设不用任何框架，你要提供一个 `GET /hello` 接口。你需要：从 TCP 字节流里解析出请求行、请求头、请求体，判断请求方法，决定该调用哪个函数，再把结果拼成符合 HTTP 规范的响应报文。这些工作与业务逻辑毫无关系，却必须做对。

WSGI 应用只有十几行，但它已经能跑起来：

```python
# 纯 WSGI 应用：不依赖任何框架
def application(environ, start_response):
    path = environ['PATH_INFO']
    if path == '/hello':
        status = '200 OK'
        body = b'hello, wsgi'
    else:
        status = '404 Not Found'
        body = b'not found'

    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    with make_server('127.0.0.1', 5000, application) as server:
        print('http://127.0.0.1:5000/hello')
        server.serve_forever()
```

运行后访问 `http://127.0.0.1:5000/hello` 会得到 `hello, wsgi`。但这段代码有三个硬伤：

1. 所有路径判断挤在一个 `if/elif` 里，路径一多就无法维护；
2. 查询参数、请求体、Cookie 全要手写解析；
3. 返回值必须手动拼装成字节串。

**Flask 的价值，就是把这三点封装掉**：把路径映射到函数、把请求解析成对象、把返回值序列化成响应。

### 5.2 WSGI 规范

WSGI（Web Server Gateway Interface，见 PEP 3333）规定了"Web 服务器"与"Python 应用"之间的调用约定。应用是一个可调用对象，接收两个参数：

| 参数 / 返回值 | 含义 |
|---|---|
| `environ` | 字典，包含请求的全部信息（方法、路径、头、体、客户端地址等） |
| `start_response` | 由服务器传入的回调，应用用它声明状态码与响应头 |
| 返回值 | 可迭代对象，逐块产出响应体（`bytes` 序列） |

`flask.Flask` 的实例本身就是一个 WSGI 应用。这一点可以直接验证：

```python
from flask import Flask

app = Flask(__name__)
print(callable(app))        # True —— 应用实例本身可调用，符合 WSGI 约定
print(app.wsgi_app)         # <bound method Flask.wsgi_app ...>
```

服务器（如 gunicorn、waitress）负责监听端口、解析 HTTP、调用这个可调用对象；Flask 负责路由分发与请求响应处理。**两者通过 WSGI 规范解耦**——这正是你能把 Flask 换成别的框架而不必改服务器配置的原因。

### 5.3 WSGI 的同步模型

这是本文最重要的一节。

在 WSGI 模型下，服务器为每一个请求调用一次应用可调用对象，**直到它返回，这个请求才算处理完**。处理这个请求的执行单元（线程或进程）在这段时间里被完全占用：

```
请求 A 到达 ──> [ 处理请求 A：查询数据库（耗时 200ms） ] ──> 返回
请求 B 到达 ──> [ 等待执行单元空闲 ] ──> [ 处理请求 B ] ──> 返回
```

由此推出两条结论，请务必记住：

1. **在视图函数里做慢操作（查库、调外部接口、读写文件），会拖慢这一个请求**，但不影响其他请求——只要还有空闲的执行单元。
2. 并发能力取决于执行单元的数量。`app.run()` 的 Werkzeug 开发服务器默认开启多线程（`threaded=True`），所以开发时感觉"并发没问题"；但这只是开发服务器的行为。

第 2 点的对比对象就是 FastAPI 的异步模型：那里所有请求共享**同一个事件循环**，任何一段阻塞代码都会卡住所有人。**本节是理解 FastAPI 并发模型的基准线**，请先记住 WSGI 是"一个请求占一个执行单元"。

### 5.4 Flask 的适用边界

| 场景 | 是否适合 | 原因 |
|---|---|---|
| 中小型业务服务、内部工具 | 适合 | 生态成熟、上手快、招人容易 |
| 教学与原型 | 适合 | 概念少，能直观看到 HTTP 的处理过程 |
| 以数据库查询为主的常规 CRUD | 适合 | 多线程 + 连接池足够 |
| 大量长连接（聊天、实时推送） | 不适合 | WSGI 无原生长连接支持，需额外引入 flask-socketio 等 |
| 高并发、大量 IO 等待 | 不适合 | 同步模型下并发靠线程，线程开销远大于协程 |
| AI/大模型应用后端 | 通常不适合 | 主流 SDK 与生态（LangChain 等）以 FastAPI 为默认 |


---

## 6 请求上下文与应用上下文

这一节解释一个"看起来像魔法"的现象，也是 Flask 最容易被误解的设计。

### 6.1 问题：`request` 从哪里来

回看 4.1 的代码：视图函数没有接收 `request` 参数，函数体内却能直接用 `request`。它是从哪来的？

如果 `request` 是模块级全局变量，多线程同时处理两个请求时必然串数据。Flask 的答案不是全局变量，而是**上下文**。

### 6.2 上下文栈与 `LocalProxy`

`flask.request` 实际上是一个 `LocalProxy` 对象——代理到"当前上下文中的真实请求对象"。流程如下：

```
请求到达
  └─> Flask 把该请求的信息压入上下文栈（request context）
      └─> 调用视图函数
          └─> 函数内访问 flask.request
              └─> LocalProxy 在当前上下文里找到对应请求对象并返回
          └─> 函数返回，上下文出栈
```

因此，每个线程（或每个协程任务）看到的是**自己的**请求对象，互不干扰。这也解释了那个经典报错：

```python
from flask import request

# 在视图函数之外访问 request，会报错：
# RuntimeError: Working outside of request context.
```

因为此时上下文栈是空的，代理找不到目标。调试时可以用**手动上下文**复现视图环境：

```python
from flask import Flask, request

app = Flask(__name__)

# test_request_context 构造一个临时请求上下文
with app.test_request_context('/search?keyword=flask'):
    print(request.path)                        # /search
    print(request.args.get('keyword'))         # flask
```

### 6.3 `current_app` 与 `g`

| 对象 | 作用 | 生命周期 |
|---|---|---|
| `request` | 当前请求的代理 | 一次请求 |
| `session` | 当前会话数据的代理 | 一次请求（数据跨请求持久化在 Cookie） |
| `current_app` | 当前应用实例的代理 | 应用与请求上下文期间均可用 |
| `g` | 一次请求内的临时存储 | 一次请求 |

`g` 的典型用法是存放"一次请求内多处要用、又不适合作为参数层层传递"的对象，例如数据库连接。

```python
from flask import g, current_app


@app.before_request
def open_conn():
    g.conn = get_connection()          # 请求开始前放好


@app.teardown_request
def close_conn(exc):
    conn = getattr(g, 'conn', None)    # 请求结束后清理，即使出错也会执行
    if conn is not None:
        conn.close()


@app.get('/info')
def info():
    return {'app_name': current_app.name}
```

`current_app` 在蓝图里尤其常用：蓝图类不需要知道具体是哪个应用实例，通过 `current_app` 取当前应用即可（见第 8 章）。


---

## 7 模板渲染（Jinja2）

前后端分离时，后端只需要返回 JSON，可以跳过本章。若需要服务端渲染页面，Flask 使用 Jinja2：

```
project/
├── app.py
└── templates/
    ├── base.html
    └── index.html
```

`base.html` 定义骨架：

```html
<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>{% block title %}首页{% endblock %}</title></head>
<body>
  <main>{% block content %}{% endblock %}</main>
</body>
</html>
```

`index.html` 继承它：

```html
{% extends "base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
  <ul>
    {% for item in items %}
      <li>{{ item.name }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```

视图函数用 `render_template` 传变量：

```python
from flask import render_template


@app.get('/page')
def page():
    return render_template('index.html', title='书籍列表',
                           items=[{'name': 'Python 基础'}, {'name': 'Web 开发'}])
```

**安全要点**：Jinja2 默认对 `{{ }}` 中的变量做 HTML 转义，这是防 XSS 的第一道防线。只有在你确认内容可信时，才使用 `{{ value | safe }}` 关闭转义——不要为了显示 HTML 而随意使用它。


---

## 8 蓝图：把应用拆成模块

### 8.1 为什么需要蓝图

单个 `app.py` 写满所有路由后无法维护。蓝图（Blueprint）是一组路由的集合，可以定义在独立模块中，再统一注册到应用上。

### 8.2 定义与注册

`user.py`：

```python
from flask import Blueprint, request

# 第一个参数是蓝图名称，第二参数是所在模块（用于定位模板等资源）
user_bp = Blueprint('user', __name__, url_prefix='/api/users')


@user_bp.get('/<int:user_id>')
def detail(user_id):
    return {'code': 200, 'data': {'id': user_id}}


@user_bp.get('/search')
def search():
    return {'code': 200, 'data': {'keyword': request.args.get('keyword', '')}}
```

`app.py` 中注册：

```python
from flask import Flask
from user import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)
```

注册后，`detail` 的实际路径是 `/api/users/<int:user_id>`——`url_prefix` 与蓝图内规则拼接而成。

### 8.3 蓝图内的 `url_for`

蓝图的端点名格式为 `蓝图名.函数名`：

```python
from flask import url_for

with app.test_request_context():
    print(url_for('user.detail', user_id=7))    # /api/users/7
```

### 8.4 推荐的目录结构

```
project/
├── app.py                 # 应用工厂 + 蓝图注册
├── config.py              # 配置
├── api/
│   ├── __init__.py
│   ├── user.py            # user 蓝图
│   └── book.py            # book 蓝图
├── dao/
│   └── user_dao.py        # 数据访问
├── service/
│   └── user_service.py    # 业务逻辑
└── common/
    ├── exceptions.py      # 自定义异常
    └── logger.py          # 日志
```

这套"路由 / 业务 / 数据"分层的做法与后面 FastAPI 项目完全一致——**蓝图的角色，相当于 FastAPI 的 `APIRouter`**。


---

## 9 错误处理与日志

### 9.1 `abort` 与错误处理器

```python
from flask import abort, Flask, jsonify

app = Flask(__name__)


@app.get('/users/<int:user_id>')
def get_user(user_id):
    if user_id > 100:
        abort(404)                 # 中断请求，交给 404 处理器
    return {'code': 200, 'data': {'id': user_id}}


@app.errorhandler(404)
def not_found(err):
    return jsonify({'code': 404, 'message': '资源不存在'}), 404


@app.errorhandler(405)
def method_not_allowed(err):
    return jsonify({'code': 405, 'message': '请求方法不允许'}), 405
```

### 9.2 自定义异常 + 统一处理器

企业项目通常定义自己的异常基类，让业务错误携带错误码，再由统一处理器转成 JSON：

```python
# common/exceptions.py
class AppError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class ParamError(AppError):
    def __init__(self, message='参数错误'):
        super().__init__(400, message)


class NotFoundError(AppError):
    def __init__(self, message='资源不存在'):
        super().__init__(404, message)
```

```python
# app.py
from common.exceptions import AppError, ParamError


@app.errorhandler(AppError)
def handle_app_error(err):
    return jsonify({'code': err.code, 'message': err.message}), err.code


@app.errorhandler(Exception)
def handle_unexpected(err):
    app.logger.exception('未处理异常')          # 完整堆栈进日志
    return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.get('/order/<int:order_id>')
def get_order(order_id):
    if order_id <= 0:
        raise ParamError('order_id 必须为正整数')
    raise NotFoundError(f'订单 {order_id} 不存在')
```

**关键实践：堆栈只进日志，对外只返回通用提示**。把数据库报错、文件路径暴露给客户端，等于给攻击者提供信息。

### 9.3 日志配置

Python 标准库的 `RotatingFileHandler` 可以在文件超过指定大小时自动轮转，避免日志无限膨胀：

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(app):
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    handler = RotatingFileHandler(
        log_dir / 'server.log',
        maxBytes=10 * 1024 * 1024,   # 单文件上限 10MB
        backupCount=5,               # 最多保留 5 个历史文件
        encoding='utf-8',
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-7s | %(name)s:%(lineno)d | %(message)s'))

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
```


---

## 10 数据库访问

### 10.1 为什么用连接池

每次请求都新建一条 MySQL 连接，需要付出 TCP 握手 + 认证的开销；请求一多，数据库连接数会被迅速耗尽。连接池预先建立若干条连接并重复使用。

```bash
pip install pymysql dbutils
```

```python
# dao/db_pool.py
from contextlib import contextmanager

import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor


class DbPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, '_ready', False):
            return
        self._pool = PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=2,
            blocking=True,
            host='127.0.0.1', port=3306,
            user='root', password='your-password',
            database='demo_db', charset='utf8mb4',
            cursorclass=DictCursor,      # 查询结果以字典返回，便于业务层使用
        )
        self._ready = True

    @contextmanager
    def cursor(self):
        """借连接 -> 执行 SQL -> 提交/回滚 -> 归还连接"""
        conn = self._pool.connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()          # 归还到池中，不是断掉物理连接


db = DbPool()
```

### 10.2 参数化查询：防 SQL 注入

```python
# 正确：占位符 %s，参数由驱动负责转义
def get_user_by_name(name: str):
    sql = 'SELECT id, name FROM t_user WHERE name = %s'
    with db.cursor() as cursor:
        cursor.execute(sql, (name,))
        return cursor.fetchone()


# 错误示范：字符串拼接，用户输入 ' or '1'='1 就能绕过条件
def get_user_by_name_unsafe(name: str):
    sql = f"SELECT id, name FROM t_user WHERE name = '{name}'"
    with db.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchone()
```

**规则：SQL 里只允许出现占位符，任何来自外部的值都必须通过 `execute` 的第二个参数传入。** 表名、列名无法参数化，如果确实需要动态拼接，必须用白名单校验。

### 10.3 单个连接与连接池的差异

`pymysql.connect()` 返回的连接不是线程安全的，多线程共享一个连接会出错。如果一定要用单连接，需显式加锁。连接池的每个连接在使用期间被独占借出，用完后归还，因此天然适配多线程。


---

## 11 配置管理

不要把配置写死在代码里。Flask 提供多种加载方式：

```python
# config.py
class BaseConfig:
    JSON_AS_ASCII = False
    DB_POOL_MAX = 10


class DevConfig(BaseConfig):
    DEBUG = True
    DB_HOST = '127.0.0.1'


class ProdConfig(BaseConfig):
    DEBUG = False
    DB_HOST = '10.0.0.5'
```

```python
# app.py
import os
from config import DevConfig, ProdConfig

app = Flask(__name__)
app.config.from_object(DevConfig if os.environ.get('FLASK_ENV') != 'prod' else ProdConfig)

# 也可以直接映射一个字典
app.config.from_mapping(SECRET_KEY='dev-only', DB_PORT=3306)

print(app.config['DB_HOST'])
```

配置的使用原则：

1. **区分环境**：开发、测试、生产用不同配置类；
2. **敏感信息走环境变量**：数据库密码、`SECRET_KEY`、第三方密钥不应写进代码仓库；
3. `SECRET_KEY` 每次启动随机生成会导致已签发的 session 全部失效，因此不要用 `os.urandom()` 直接赋值。


---

## 12 部署与运行

### 12.1 开发服务器不能用于生产

`flask run` 启动的是 Werkzeug 开发服务器，它的设计目标是方便调试，不满足生产环境的性能与安全要求。生产环境使用 WSGI 服务器：

```bash
pip install gunicorn                 # Linux / macOS
gunicorn -w 4 -b 0.0.0.0:8000 "app:app"
```

```bash
pip install waitress              # Windows
waitress-serve --listen=0.0.0.0:8000 app:app
```

### 12.2 多进程带来的状态问题

`-w 4` 表示启动 4 个进程，每个进程有独立的内存空间。由此产生三个必须注意的问题：

1. **内存中的状态不共享**：在进程 A 里写进字典的值，进程 B 读不到。计数、缓存、限流这类功能不能依赖进程内变量；
2. **会话必须外置**：应在 Redis 等外部存储中管理登录态，而不是依赖进程内字典；
3. **定时任务会重复执行**：每个进程都会跑一遍，需要引入分布式锁或独立的任务进程。

### 12.3 生产部署要点

| 事项 | 做法 |
|---|---|
| `debug` | 必须为 `False` |
| `SECRET_KEY` | 从环境变量读取，长度足够且固定 |
| HTTPS | 由 Nginx 等反向代理终止 TLS |
| 日志 | 输出到文件或标准输出，交由外部系统采集 |
| 健康检查 | 提供 `/health` 接口供负载均衡探活 |
| 输入长度限制 | 在反向代理层限制请求体大小，防止大包攻击 |


---

## 13 常见错误与排查

| 报错 / 现象 | 原因 | 解决 |
|---|---|---|
| `RuntimeError: Working outside of request context` | 在视图函数之外访问了 `request` | 在视图函数内使用；测试时用 `app.test_request_context()` |
| `RuntimeError: Working outside of application context` | 使用了需要应用上下文的对象（如 `current_app`） | 在视图内使用；或用 `with app.app_context():` |
| `RuntimeError: The session is unavailable because no secret key was set` | 未配置 `SECRET_KEY` 就使用了 `session` | 设置 `app.secret_key` |
| `405 Method Not Allowed` | 路由未声明该方法 | 在 `methods` 中补上，或改用 `@app.post` 等快捷装饰器 |
| 访问 404，路由看似正确 | `url_prefix` 与蓝图内规则拼接后路径不符 | 用 `flask routes` 命令打印全部已注册路由 |
| 返回的中文显示为 `\u4e2d\u6587` | JSON 序列化启用了 ASCII 转义 | 设置 `app.json.ensure_ascii = False` |
| 改代码不生效 | 未开启自动重载 | 启动时加 `--debug` |
| 多线程下数据串了 | 误把请求相关数据存到了模块级全局变量 | 改用 `g` 或 `request` 上下文对象 |

排查路由问题的实用命令：

```bash
flask --app app routes
```

它会列出应用中所有已注册的 URL 规则、允许的方法与端点名，是定位 404/405 最快的手段。


---

## 14 练习任务

### 练习 1（基础）

用 Flask 实现一个图书接口服务，满足：

1. `GET /api/books` 返回图书列表，支持 `keyword` 查询参数做标题模糊筛选，`page`（默认 1）、`size`（默认 10）分页；响应统一为 `{"code": 200, "message": "ok", "data": {...}}`；
2. `GET /api/books/<int:book_id>` 返回单本图书，不存在时返回 `{"code": 404, ...}` 且 HTTP 状态码为 404；
3. `POST /api/books` 接收 JSON 请求体（`title`、`author`、`price`），`title` 为空时返回 400。

要求：用一个内存列表作为数据源，全部逻辑放在蓝图 `book_bp` 中，`url_prefix` 为 `/api/books`。

作答区：

```
（在此处写出你的代码）
```

### 练习 2（上下文）

解释下面这段代码为什么会报错，并给出两种修改方式。

```python
from flask import Flask, request

app = Flask(__name__)


def read_keyword():
    return request.args.get('keyword', '')


@app.get('/search')
def search():
    return {'keyword': read_keyword()}
```

作答区：

```
（在此处写出你的分析与两种修改方案）
```

### 练习 3（错误处理与日志）

把练习 1 的接口改造为：自定义 `AppError` 异常体系，`ParamError` 对应 400、`NotFoundError` 对应 404，用一个统一处理器返回 JSON；同时让未预期异常返回 500 且把完整堆栈写进 `logs/server.log`。

作答区：

```
（在此处写出你的代码）
```

### 练习 4（数据库）

为练习 1 的图书服务加一个 MySQL 版本：用 `DBUtils.PooledDB` 建连接池，实现"按标题模糊查询"和"按 id 查询"两个方法。要求全部使用参数化查询，并说明为什么 `LIKE` 查询的 `%` 要拼在参数里而不是 SQL 字符串里。

作答区：

```
（在此处写出你的代码与说明）
```


---

## 15 参考答案与评价要点

### 练习 1 参考答案

```python
# api/book.py
from flask import Blueprint, request

book_bp = Blueprint('book', __name__, url_prefix='/api/books')

BOOKS = [
    {'id': 1, 'title': 'Python 编程基础', 'author': '张三', 'price': 59.0},
    {'id': 2, 'title': 'Web 开发入门', 'author': '李四', 'price': 69.0},
]


def ok(data=None):
    return {'code': 200, 'message': 'ok', 'data': data}


@book_bp.get('')
def list_books():
    keyword = request.args.get('keyword', '').strip()
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    if page < 1 or size < 1:
        return {'code': 400, 'message': 'page/size 必须为正整数'}, 400

    rows = [b for b in BOOKS if keyword in b['title']] if keyword else BOOKS
    start = (page - 1) * size
    return ok({'total': len(rows), 'items': rows[start:start + size]})


@book_bp.get('/<int:book_id>')
def get_book(book_id):
    for b in BOOKS:
        if b['id'] == book_id:
            return ok(b)
    return {'code': 404, 'message': '图书不存在'}, 404


@book_bp.post('')
def create_book():
    data = request.get_json(silent=True)
    if data is None:
        return {'code': 400, 'message': '请求体必须是合法 JSON'}, 400
    title = str(data.get('title', '')).strip()
    if not title:
        return {'code': 400, 'message': 'title 不能为空'}, 400

    new_id = max([b['id'] for b in BOOKS], default=0) + 1
    book = {'id': new_id, 'title': title,
            'author': str(data.get('author', '')),
            'price': float(data.get('price', 0))}
    BOOKS.append(book)
    return ok(book), 201
```

```python
# app.py
from flask import Flask
from api.book import book_bp

app = Flask(__name__)
app.json.ensure_ascii = False          # 中文不转义
app.register_blueprint(book_bp)
```

**评价要点**

1. 路由前缀是否正确（蓝图 `url_prefix` + 蓝图内 `''` 与 `'/<int:book_id>'`）；
2. 是否区分了"业务错误"与"HTTP 状态码"：返回体里的 `code` 与 HTTP 状态码应保持一致；
3. `page`/`size` 是否做了边界校验——`size=0` 会导致除零或空结果，`page=-1` 会产生负数下标；
4. 是否使用了 `get_json(silent=True)` 而不是 `request.json`；
5. `POST` 成功是否返回 201 而不是 200。

### 练习 2 参考答案

**报错原因**：`request` 是 `LocalProxy`，它代理的是"当前请求上下文中的请求对象"。`read_keyword()` 虽然被视图函数调用，但它**执行时**上下文栈里有请求上下文，所以这个具体写法其实不会报错——真正的报错场景是**在视图函数之外**（例如模块导入时、线程中、定时任务里）访问 `request`，此时上下文栈为空，代理找不到目标，抛出 `RuntimeError: Working outside of request context`。

本题的考点是：**判断一段代码是否会触发上下文错误，看的是"执行时的调用栈里有没有视图函数"，而不是"代码写在哪个文件"**。

两种修改方式（用于真正的视图外场景）：

```python
# 方式一：把当前请求依赖的值作为参数传入
def read_keyword(keyword_arg: str) -> str:
    return keyword_arg.strip()


@app.get('/search')
def search():
    return {'keyword': read_keyword(request.args.get('keyword', ''))}
```

```python
# 方式二：需要复现请求环境时，手动构造上下文（常用于测试与脚本）
from flask import request

with app.test_request_context('/search?keyword=flask'):
    print(request.args.get('keyword'))     # flask
```

**评价要点**：能说清"上下文在函数调用期间存在"；能给出"传参"这一实用的解耦方式。

### 练习 3 参考答案

```python
# common/exceptions.py
class AppError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(message)


class ParamError(AppError):
    def __init__(self, message='参数错误'):
        super().__init__(400, message)


class NotFoundError(AppError):
    def __init__(self, message='资源不存在'):
        super().__init__(404, message)
```

```python
# app.py（在原基础上追加）
from flask import jsonify
from common import setup_logging
from common.exceptions import AppError


@app.errorhandler(AppError)
def handle_app_error(err):
    app.logger.info(f'业务异常 [{err.code}] {err.message}')
    return jsonify({'code': err.code, 'message': err.message}), err.code


@app.errorhandler(Exception)
def handle_unexpected(err):
    if isinstance(err, HTTPException):          # 保留 404/405 等框架异常语义
        return jsonify({'code': err.code, 'message': err.description}), err.code
    app.logger.exception('未处理异常')
    return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


setup_logging(app)
```

**评价要点**

1. `@app.errorhandler(Exception)` 会捕获所有异常，**必须先放行 `HTTPException`**，否则 404 会变成 500；
2. 是否用 `app.logger.exception()` 而不是 `app.logger.error()`——只有 `exception` 会带上堆栈；
3. 对外响应是否隐藏了内部细节；
4. 异常码与 HTTP 状态码是否一致。

### 练习 4 参考答案

```python
# dao/book_dao.py
from dao.db_pool import db


class BookDao:
    def search_by_title(self, keyword: str, limit: int = 50):
        sql = ('SELECT id, title, author, price FROM t_book '
               'WHERE title LIKE %s ORDER BY id LIMIT %s')
        with db.cursor() as cursor:
            cursor.execute(sql, (f'%{keyword}%', limit))
            return list(cursor.fetchall())

    def get_by_id(self, book_id: int):
        sql = 'SELECT id, title, author, price FROM t_book WHERE id = %s'
        with db.cursor() as cursor:
            cursor.execute(sql, (book_id,))
            return cursor.fetchone()
```

**为什么 `%` 要拼在参数里**：参数化查询的工作方式是——SQL 语句先被数据库解析并编译成执行计划，参数值以独立通道传入，永远不会被当作 SQL 语法解析。因此 `f'%{keyword}%'` 作为一个整体字符串传入参数通道，其中即便包含 `'` 或 `--`，也只是普通字符。如果把 `%` 拼进 SQL 字符串（如 `"WHERE title LIKE '%" + keyword + "%'"`），用户输入的引号就会闭合字符串、注入新语法，参数化就形同虚设。

**评价要点**

1. 是否用 `%s` 占位符而非 f-string 拼接；
2. 是否理解"参数化不是把值转义，而是让值根本不进入 SQL 语法层"；
3. 分页 `LIMIT` 也用参数传入，而不是拼接。


---

## 16 衔接：从 Flask 走向 FastAPI

本文末尾留下三个问题，它们是下一篇《FastAPI 技术文档》的起点：

1. **WSGI 的同步模型在什么情况下会成为瓶颈**？当一个请求里大部分时间都在等待 IO（数据库、外部接口）时，线程被占着却什么也没干。
2. **"在视图函数里做慢操作只影响自己"这个结论，换个运行时还成立吗**？在事件循环模型下就不成立了。
3. **数据校验写在哪一层**？本文的做法是在视图函数里手写 `if not title: return 400`。当字段变多时，这段代码会迅速膨胀——FastAPI 用 Pydantic 模型把校验声明化。


---

## 附录 A 教师使用说明

> 本节供授课教师参考，不属于学员讲义正文，讲授时可整体略过。

### A.1 课时安排建议（共 3 课时）

| 课时 | 讲授内容 | 课堂演示建议 |
|---|---|---|
| 第 1 课时 | 第 1 章（认识 Web 与 Flask）、第 2 章（跑起第一个程序）、第 3 章（路由） | 先在幻灯片上走一遍"输入网址后发生了什么"；再带学生把最小程序跑起来，用浏览器访问看到结果 |
| 第 2 课时 | 第 4 章（请求与响应）、第 5 章（WSGI 原理）、第 6 章（上下文） | 先运行 5.1 的纯 WSGI 应用，再对照 Flask 应用，让学生直观看到框架省掉了什么；现场触发"视图外访问 request"的报错并修复 |
| 第 3 课时 | 第 8 章（蓝图）、第 9 章（错误与日志）、第 10 章（数据库） | 演示 `flask --app app routes` 打印路由表；SQL 注入环节现场输入 `' or '1'='1` 看到全部数据 |

第 7 章（模板）、第 11 章（配置）、第 12 章（部署）、第 13 章（排查）可作为自学内容。

### A.2 讲授侧重点

1. **第 1 章是"地基"，务必讲慢**。很多学生是第一次理解前端、后端、请求与响应，建议多用餐厅类比，确认他们能自己复述"在浏览器输入网址后发生了什么"，再往下走。
2. **第 5.3 节（同步模型）必须讲透**。它是理解后续 FastAPI 异步模型与"阻塞代码要丢线程池"的基准线。可用"排队买票"类比：WSGI 是"一个窗口一个人，办完才轮到下一个"，多线程是"多开几个窗口"，事件循环是"一个窗口在多个柜台间快速轮转"。
3. **第 6 章要讲机制、不要只讲现象**。学员常把 `request` 当成全局变量，这个误解会在多线程调试时造成严重困惑。
4. **第 10 章的 SQL 注入建议现场演示攻击**。把 `get_user_by_name_unsafe` 跑起来，输入 `' or '1'='1` 看到全部数据被查出，比讲十分钟原理更有效。
5. **守住"先跑起来、再讲原理"的顺序**：不要在学生跑通第一个程序之前深入 WSGI 细节，那会让入门者失去方向。

### A.3 常见学员疑问

| 疑问 | 回答要点 |
|---|---|
| 为什么视图函数不用写 `request` 参数？ | 见第 6 章。它是上下文代理，不是全局变量。 |
| 为什么不直接用一个全局 `request = {}`？ | 多线程会串数据。可以用一个 10 行的小实验验证：两个线程分别往全局字典写不同值，读到的会互相覆盖。 |
| 蓝图和模块有什么区别？ | 模块是 Python 的代码组织单位，蓝图是"一组路由 + 前缀 + 独立钩子"的注册单位。二者配合使用：一个蓝图通常放在一个模块里。 |
| 开发服务器为什么不能上生产？ | 单进程、无并发优化、调试器可执行任意代码。用 gunicorn/waitress。 |
| 返回 `dict` 和 `jsonify` 有什么区别？ | 最终都会变成 JSON 响应；`jsonify` 用于需要进一步加工响应的场景。 |

### A.4 与后续课程的接口

本文结束后，学员应带着以下三个未解问题进入《FastAPI 技术文档》：同步模型的瓶颈在哪里、事件循环下阻塞的代价是什么、数据校验能否声明化。下一篇会逐条给出答案，并最终落到"心聆 MindEcho"项目的代码结构上。
