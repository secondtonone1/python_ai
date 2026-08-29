# SmartService AI 智能客服系统

> 02_advance（进阶）阶段综合项目，方向：**AI 大模型应用开发**。
> 用"一个完整的 AI 智能客服系统"串联起面向对象、线程、协程、MySQL 等已学知识点，
> 并引入 **FastAPI + WebSocket**（AI 领域最主流的服务框架），
> 核心的"机器人引擎"设计成可插拔抽象：本阶段用**规则引擎**，后续阶段无缝替换为真实大模型（LangChain/LangGraph）。

---

## 一、项目定位

**业务场景**：培训机构部署一套在线客服系统。访客在网页上与 AI 机器人对话咨询
（课程、开班时间、学费、报名方式……），机器人基于知识库规则回答；
答不上来的问题自动转人工，客服人员在工作台实时接管会话。

| 角色 | 界面 | 功能 |
|---|---|---|
| 访客 | `http://localhost:8000/` 聊天页 | 创建会话、与 AI 流式对话、满意度评价 |
| AI 机器人 | 服务端规则引擎 | 知识库关键词匹配、追问澄清、未命中转人工 |
| 客服人员 | `http://localhost:8000/staff` 工作台 | 登录、会话列表、人工接管、回复、知识库管理、统计报表 |

**课程路线的定位**：这是 AI 应用开发的第一站 —— 学会用 Web 服务承载 AI 能力、
把"模型"抽象成可替换组件。后续 dify（低代码）、机器学习深度学习、LangChain/LangGraph
阶段都会在此基础上演进（详见 `docs/02_系统设计文档.md` 第 9 章演进路线）。

## 二、系统架构

```
+-------------------------------- 前端层 ---------------------------------+
|  index.html 访客聊天页              staff.html 客服工作台                |
|  (原生JS + WebSocket流式渲染)       (登录/接管/回复/知识库/统计)           |
+----------|-----------------------------------------|--------------------+
           | REST (HTTP)                REST (HTTP)   |
           | + WebSocket 流式对话                      |
+----------v-----------------------------------------v--------------------+
|                        FastAPI 应用 (asyncio 内核)                      |
|  api/chat.py   访客接口       api/staff.py  客服接口                     |
|  api/ws.py     WebSocket     api/pages.py  页面路由                     |
+------------------------------------|------------------------------------+
|                     service 业务层                                      |
|  chat_service(编排) / staff_service(人工)                               |
|  bot_engine(可插拔AI引擎) / rate_limiter(限流) / ws_manager(连接管理)     |
+------------------------------------|------------------------------------+
|                      dao 数据访问层 (DBUtils 连接池)                     |
|  session_dao / message_dao / knowledge_dao / staff_dao                  |
+------------------------------------|------------------------------------+
|  common 基础层: 常量/异常/配置/日志  |  schema: Pydantic 请求响应模型     |
+------------------------------------|------------------------------------+
|                        MySQL (ai_service_db)                            |
|       t_session / t_message / t_knowledge / t_staff                     |
+-------------------------------------------------------------------------+
```

## 三、目录结构

```
ai_service/
├── README.md                  # 项目总览(本文件)
├── requirements.txt           # fastapi / uvicorn / pymysql / DBUtils
├── config/config.json         # 全局配置(端口/数据库/日志/机器人/限流)
├── scripts/init_db.sql        # 建库建表 + 演示知识库 + 客服账号
├── docs/                      # 01需求 02设计 03API 04知识点串联
├── aiservice/                 # 主程序包
│   ├── main.py                # FastAPI 应用工厂 + 生命周期 + 异常映射
│   ├── common/                # 基础层: 常量/异常/配置/日志
│   ├── schema/                # Pydantic 请求/响应模型
│   ├── dao/                   # 数据层: 连接池 + 4个DAO
│   ├── service/               # 业务层: 规则引擎/编排/限流/WS管理
│   ├── api/                   # 接口层: chat/staff/ws/pages 路由
│   └── static/                # 前端页面(原生HTML+JS)
├── run.py                     # 启动入口  python run.py
└── tests/                     # 单元测试
```

## 四、快速开始

> 所有命令在 `ai_service` 目录下执行。

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

执行 `scripts/init_db.sql`（创建 `ai_service_db` 库、4 张表、8 条演示知识库数据、
客服账号 `admin / 123456`）。数据库连接在 `config/config.json` 的 `database` 小节。

### 3. 启动服务

```bash
python run.py
# 开发模式(改代码自动重启): python run.py --reload
```

### 4. 体验

| 入口 | 地址 | 说明 |
|---|---|---|
| 访客聊天页 | http://localhost:8000/ | 试试问：`你们的课程有哪些？` `学费多少钱` `什么时候开班` |
| 客服工作台 | http://localhost:8000/staff | admin / 123456 登录 |
| 接口文档 | http://localhost:8000/docs | FastAPI 自动生成的 Swagger 文档 |

**演示路径**：
1. 聊天页问"上课时间"→ 机器人从知识库命中，**逐字流式输出**答案，可评价满意度
2. 问一个知识库没有的问题（如"我想请假怎么办"）→ 机器人提示转人工
3. 客服工作台看到"等待中"会话 → 点击接管 → 回复消息 → 聊天页**实时收到**客服消息
4. 工作台"统计"页查看：会话量 / 机器人命中率 / 满意度
5. 连续快速发消息超过限流阈值 → 收到 429 提示（限流保护演示）

## 五、企业级特性对照表

| 企业级标准 | 本项目落点 |
|---|---|
| 分层架构 | common/schema → dao → service → api，上层依赖下层 |
| 配置与代码分离 | `config/config.json` + Config 单例（bot 话术/阈值/限流参数均可配） |
| 统一异常体系 | MonitorError + 错误码 → FastAPI 异常处理器统一转 JSON 响应 |
| 连接池 | DBUtils PooledDB + 上下文管理器（自动提交/回滚/归还） |
| SQL 安全 | 全量参数化查询，杜绝 SQL 注入 |
| 密码安全 | 客服密码 SHA256 加盐哈希存储，不存明文 |
| 接口限流 | 内存滑动窗口限流器（会话/聊天两类接口，防刷） |
| 流式输出 | WebSocket 逐字推送（模拟大模型 token 流，AI 应用标配体验） |
| 异步推送 | 客服回复实时推送到访客浏览器（无轮询） |
| 后台任务 | asyncio 周期任务自动归档超时会话 |
| 接口文档 | FastAPI 自动生成 Swagger（/docs）+ 手写 API 文档 |
| 单元测试 | 规则引擎 / 限流器 / 配置 / 接口冒烟 |

## 六、知识点对照（简表）

| 课程 | 知识点 | 项目落点 |
|---|---|---|
| 01-15 | 面向对象 | 分层架构、BotEngine 抽象 + RuleEngine 实现（多态） |
| 16 | 单例模式 | Config / DbPool / WsManager |
| 21 | 上下文管理器 | DbPool.cursor() 自动提交/回滚/归还 |
| 33-45 | 装饰器 | FastAPI 路由装饰器 @app.get、@app.websocket |
| 55-72 | 线程/锁 | uvicorn 线程池跑同步端点、RateLimiter 线程锁、DBUtils 线程安全 |
| 73-83 | 协程/asyncio | FastAPI 即 asyncio 框架：async 端点、WebSocket、后台归档任务、run_in_executor 跑阻塞 DB |
| 84-89 | TCP/网络编程 | WebSocket 长连接（HTTP 升级而来）；TCP 粘包/半包概念对照 WebSocket 帧 |
| 90 | pymysql | DAO 层：连接池 + 参数化 + DictCursor + 事务 |

完整对照见 `docs/04_知识点串联手册.md`。

## 七、常见问题

| 问题 | 解决 |
|---|---|
| `ModuleNotFoundError: No module named 'aiservice'` | 必须在 `ai_service` 目录下运行 |
| 启动报"数据库连接失败" | 检查 `config/config.json`；确认已执行 `scripts/init_db.sql` |
| 网页打不开 | 确认 uvicorn 监听端口与配置一致（默认 8000） |
| WebSocket 断开 | 服务端重启会断开，刷新页面即可重建会话 |
| 登录客服工作台失败 | 账号 admin / 123456（首次需执行 init_db.sql） |
