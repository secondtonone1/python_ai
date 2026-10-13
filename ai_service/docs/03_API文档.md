# SmartService AI 智能客服系统 - API 文档

| 项目 | 内容 |
|---|---|
| 文档版本 | v1.0 |
| 在线文档 | 启动服务后访问 http://localhost:8000/docs (Swagger, 可在线调试) |

## 1. 通用约定

- **统一响应格式**：所有接口返回 `{"code": 200, "message": "ok", "data": ...}`
- **错误码**：200 成功 / 400 参数错误 / 401 未认证 / 403 无权限 / 404 不存在 / 429 限流 / 500 服务器错误
- **客服鉴权**：登录成功后，请求头携带 `X-Staff-Id: <客服id>`（演示级方案，生产应使用 JWT）
- **限流**：聊天消息 20 条/分钟/会话；创建会话 10 次/分钟/IP；超限返回 429 + `Retry-After` 响应头

## 2. 访客接口

### POST /api/session — 创建会话

```json
// 请求
{"visitor_name": "张三"}

// 响应 data
{"id": 1, "visitor_name": "张三", "status": "bot",
 "created_at": "2026-08-18T10:00:00", "updated_at": "2026-08-18T10:00:00"}
```

### GET /api/session/{session_id}/history — 会话历史

```json
// 响应 data: 消息数组
[{"id": 1, "session_id": 1, "role": "user", "content": "学费多少钱",
  "source": null, "rating": null, "created_at": "2026-08-18T10:00:05"}]
```

### POST /api/message/{message_id}/rate — 满意度评价

```json
// 请求: 1=满意 -1=不满意
{"rating": 1}

// 响应 data
{"message_id": 5, "rating": 1}
```

## 3. WebSocket 接口

### WS /ws/chat/{session_id} — 流式对话通道

| 方向 | 消息 | 说明 |
|---|---|---|
| C→S | `{"type":"chat","content":"..."}` | 发送聊天消息 |
| C→S | `{"type":"ping"}` | 心跳保活（前端每 30s 发送） |
| S→C | `{"type":"pong"}` | 心跳响应 |
| S→C | `{"type":"chunk","delta":"学"}` | **流式分片**，机器人逐字输出 |
| S→C | `{"type":"message_end","message":{...}}` | 一条机器人消息输出完毕 |
| S→C | `{"type":"session_status","status":"waiting_human"}` | 会话状态变化（转人工/已接入） |
| S→C | `{"type":"staff_reply","message":{...}}` | **人工客服回复实时推送** |
| S→C | `{"type":"error","code":429,"message":"..."}` | 错误（如限流） |

**流式对话时序**：

```
访客                    服务端
  |--{"type":"chat"}------>|
  |                        | 限流 -> 入库 -> 规则引擎
  |<--{"type":"chunk",...}--| 分片1
  |<--{"type":"chunk",...}--| 分片2 (每50ms一个)
  |        ......          |
  |<--{"type":"message_end"}-| 整条消息完毕(带消息id, 供评价)
  |<--{"type":"session_status","status":"waiting_human"}-| (未命中时)
```

### WS /ws/staff?staff_id=1 — 客服工作台推送通道（替代轮询）

客服登录后建立本连接，服务端把所有会话事件**实时推送**过来——会话列表与消息
不再需要 3s/5s 的 HTTP 轮询（仅登录/打开会话/断线重连时做一次全量拉取兜底）。

| 方向 | 消息 | 说明 |
|---|---|---|
| C→S | `{"type":"ping"}` | 心跳保活（工作台每 30s 发送） |
| S→C | `{"type":"staff_session","session":{id,visitor_name,status,updated_at}}` | **会话信息变更**：新转人工/被接管/被关闭/有新活动，前端按当前列表增删改 |
| S→C | `{"type":"staff_message","message":{...}}` | **新消息**：访客消息/机器人回答/客服回复，选中该会话时实时上屏 |
| S→C | `{"type":"pong"}` | 心跳响应 |

触发点：访客发消息/机器人回答（chat_service 入库后）、客服接管/回复/关闭（staff
接口执行后）都会向所有在线工作台广播。工作台侧是"广播 + 前端过滤"模型。

## 4. 客服接口（需 X-Staff-Id 请求头）

### POST /api/staff/login — 登录

```json
// 请求 (演示账号: admin / 123456)
{"username": "admin", "password": "123456"}

// 响应 data
{"id": 1, "username": "admin", "display_name": "值班客服"}
```

### GET /api/staff/sessions?status=waiting_human — 会话列表

status 可选: `bot` / `waiting_human` / `human` / `closed`

```json
// 响应 data
[{"id": 3, "visitor_name": "访客", "status": "waiting_human",
  "created_at": "...", "updated_at": "..."}]
```

> 平时会话列表由 WebSocket（`/ws/staff`）推送增量维护；本接口只在
> **登录首次加载 / 断线重连对账 / 切换状态页**时全量拉取。

### POST /api/staff/sessions/{id}/takeover — 人工接管

接管成功后会实时广播：向全部工作台推 `staff_session`（该会话移出"等待人工"
列表）、向该会话的访客推 `session_status: human`（访客页面即时显示"人工客服
已接入"）。

### GET /api/staff/sessions/{id}/messages?after_id=0 — 增量消息（兜底）

工作台平时通过 WebSocket（`/ws/staff`）实时接收新消息；本接口仅在
**打开会话拉历史、断线重连补齐推送间隙**时调用一次。`after_id` 传最后一条
消息的 id，只返回新消息。

### POST /api/staff/sessions/{id}/reply — 回复访客

```json
// 请求
{"content": "您好，正在为您查询班期..."}

// 访客浏览器通过 WebSocket 实时收到 {"type":"staff_reply", ...}
// 全部在线工作台实时收到 {"type":"staff_message", ...} 与 {"type":"staff_session", ...}
```

### POST /api/staff/sessions/{id}/close — 关闭会话

关闭成功后会实时广播：向全部工作台推 `staff_session`（该会话移出列表）、
向该会话的访客推 `session_status: closed`。

### POST /api/staff/sessions/{id}/polish — AI 检索润色（咨询师助手）

需会话处于 `human`（已接入）。两种模式（`data.mode` 区分）：

- **生成模式**（body 为空 `{}`）：取来访者**最近一条消息** → 检索知识库 →
  以咨询师口吻起草回复（`mode: generate`）；
- **润色模式**（body 传 `content`，即咨询师已写草稿）：结合来访者消息与知识库
  **润色/改写这段草稿**，保持原意（`mode: polish`）。

未配置大模型 Key 时自动降级为内置检索润色（此时润色模式保留原文并说明），始终有结果。

```json
// 请求示例: 润色自己已写的草稿
{"content": "别太担心，一切都会好的。"}

// 响应 data (润色模式)
{"draft": "我听到你现在有些担心……我很愿意陪你一起想办法。", "engine": "llm",
 "mode": "polish", "note": "已润色您的草稿; 命中知识库: ...",
 "knowledge_id": 15, "question": "最近总是很焦虑"}
```

> `engine`: `llm` = 真实大模型（需在 `config/config.json` 的 `polisher.llm` 配 API Key）；
> `rule` = 内置检索润色（零依赖兜底）。`draft` 返回后可编辑再发送。

### GET /api/staff/stats — 运营统计

```json
// 响应 data
{"session_total": 12, "session_by_status": {"bot": 3, "waiting_human": 2, ...},
 "message_today": 156, "bot_answer_total": 80, "bot_hit_rate": 0.83,
 "rating_count": 25, "avg_rating": 0.92}
```

### 知识库管理

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /api/staff/knowledge | 全部知识条目 |
| POST | /api/staff/knowledge | 新增 `{category, question, keywords, answer}` |
| PUT | /api/staff/knowledge/{id} | 更新（只更新传入的字段，None 忽略） |
| DELETE | /api/staff/knowledge/{id} | 删除 |

```json
// 新增请求示例
{"category": "咨询预约", "question": "咨询怎么收费、一次多久",
 "keywords": "收费,费用,多少钱,时长", "answer": "当前为教学演示，咨询不收取费用。单次咨询通常为 50 分钟。"}
```

## 5. 页面路由

| 路径 | 内容 |
|---|---|
| GET / | 来访者聊天页 |
| GET /staff | 咨询师工作台 |
| GET /docs | Swagger 接口文档（在线调试） |
| GET /api/health | 健康检查 |

## 6. curl 演示清单（课堂使用）

```bash
# 1. 健康检查
curl http://localhost:8000/api/health

# 2. 创建会话
curl -X POST http://localhost:8000/api/session -H "Content-Type: application/json" -d '{"visitor_name":"小明"}'

# 3. 查询历史
curl http://localhost:8000/api/session/1/history

# 4. 评价(满意)
curl -X POST http://localhost:8000/api/message/2/rate -H "Content-Type: application/json" -d '{"rating":1}'

# 5. 咨询师登录 -> 拿到 id
curl -X POST http://localhost:8000/api/staff/login -H "Content-Type: application/json" -d '{"username":"admin","password":"123456"}'

# 6. 待接入的会话列表 (1 为咨询师id)
curl http://localhost:8000/api/staff/sessions?status=waiting_human -H "X-Staff-Id: 1"

# 7. 接入会话 (接入后状态变 human)
curl -X POST http://localhost:8000/api/staff/sessions/1/takeover -H "X-Staff-Id: 1"

# 8. AI 检索润色 (返回可编辑草稿; 未配 Key 时用内置检索润色)
curl -X POST http://localhost:8000/api/staff/sessions/1/polish -H "X-Staff-Id: 1"

# 9. 回复来访者 (来访者页面实时收到)
curl -X POST http://localhost:8000/api/staff/sessions/1/reply -H "X-Staff-Id: 1" -H "Content-Type: application/json" -d '{"content":"我听到你的困扰了，我们可以一起慢慢梳理。"}'

# 10. 运营统计
curl http://localhost:8000/api/staff/stats -H "X-Staff-Id: 1"

# 11. 新增知识
curl -X POST http://localhost:8000/api/staff/knowledge -H "X-Staff-Id: 1" -H "Content-Type: application/json" -d '{"category":"咨询预约","question":"咨询怎么收费、一次多久","keywords":"收费,费用,多少钱,时长","answer":"当前为教学演示，咨询不收取费用。"}'

# 12. 未认证访问客服接口 -> 401
curl http://localhost:8000/api/staff/sessions
```
