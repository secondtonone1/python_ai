'''
service 业务层: 承载所有业务规则
- bot_engine: AI 客服引擎抽象 + 规则引擎实现 (可插拔, 后续替换真实大模型)
- chat_service: 访客侧编排 (会话/消息/流式输出/追问状态)
- staff_service: 人工客服 (登录/接管/回复/统计/知识库管理)
- rate_limiter: 滑动窗口限流器
- ws_manager: WebSocket 连接管理器 (实时推送)
'''
