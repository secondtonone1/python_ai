'''
SmartService AI 智能客服系统
============================
02_advance(进阶)阶段 AI 方向综合项目。

分层结构(上层依赖下层, 下层不感知上层):
    api      -> FastAPI 路由层(chat/staff/ws/pages) + main 应用工厂
    service  -> 业务层(规则引擎/会话编排/人工客服/限流/WS连接管理)
    dao      -> 数据访问层(DBUtils 连接池 + 4 个 DAO)
    schema   -> Pydantic 请求/响应模型
    common   -> 基础层(常量/异常/配置/日志)

AI 核心设计: service/bot_engine.py 中的 BotEngine 是可插拔抽象,
本阶段用 RuleEngine(知识库规则引擎), 后续阶段替换为真实大模型实现。
'''
