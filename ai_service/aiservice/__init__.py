'''
心聆 MindEcho 在线心理支持平台 (AI 心理咨询师系统)
==================================================
02_advance(进阶)阶段 AI 方向综合项目。

分层结构(上层依赖下层, 下层不感知上层):
    api      -> FastAPI 路由层(chat/staff/ws/pages) + main 应用工厂
    service  -> 业务层(AI引擎/会话编排/咨询师/限流/WS连接管理/润色引擎)
    dao      -> 数据访问层(DBUtils 连接池 + 4 个 DAO)
    schema   -> Pydantic 请求/响应模型
    common   -> 基础层(常量/异常/配置/日志)

AI 核心设计:
- service/bot_engine.py: BotEngine 可插拔抽象(本阶段 RuleEngine, 后续换真实大模型)
- service/reply_polisher.py: 咨询师助手"AI 检索润色"抽象(内置规则版 + 真实大模型版)

免责声明: 本系统为教学演示项目, 不构成医疗/心理诊断。
'''
