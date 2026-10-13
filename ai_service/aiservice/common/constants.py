'''
常量定义模块
============
企业级项目中, 所有"魔法数字"与枚举值集中定义:
1. 修改时只需要改一处, 不会遗漏
2. 见名知义, 代码可读性更好
'''


class SessionStatus:
    """会话状态 (状态机见 docs/02_系统设计文档.md 第 6 章)"""
    BOT = 'bot'                    # 机器人接待中
    WAITING_HUMAN = 'waiting_human'  # 机器人未命中, 等待人工
    HUMAN = 'human'                # 人工客服接管中
    CLOSED = 'closed'              # 已关闭
    ARCHIVED = 'archived'          # 超时归档


class MessageRole:
    """消息角色"""
    USER = 'user'      # 访客
    BOT = 'bot'        # AI 机器人
    STAFF = 'staff'    # 人工客服


class MessageSource:
    """机器人回答来源 (统计命中率用)"""
    KNOWLEDGE = 'knowledge'  # 知识库命中
    PENDING = 'pending'      # 追问澄清(让用户选序号)
    FALLBACK = 'fallback'    # 未命中, 转人工话术
    HUMAN = 'human'          # 人工客服回复


class WsType:
    """WebSocket 消息类型 (客户端 <-> 服务端)"""
    # 客户端 -> 服务端
    CHAT = 'chat'          # 发送聊天消息 {content}
    PING = 'ping'          # 心跳保活
    # 服务端 -> 客户端 (访客侧)
    CHUNK = 'chunk'              # 流式输出的一个分片 {delta}
    MESSAGE_END = 'message_end'  # 一条消息输出完毕 {message}
    SESSION_STATUS = 'session_status'  # 会话状态变化 {status}
    STAFF_REPLY = 'staff_reply'  # 人工客服回复(实时推送) {message}
    ERROR = 'error'              # 错误 {code, message}
    PONG = 'pong'
    # 服务端 -> 客户端 (客服工作台侧, 替代轮询)
    STAFF_SESSION = 'staff_session'    # 会话信息变更 {session}
    STAFF_MESSAGE = 'staff_message'    # 新消息入库 {message}


class ErrorCode:
    """业务错误码 (与 HTTP 状态码对应, 见 api 层异常映射)"""
    SUCCESS = 200
    PARAM_ERROR = 400        # 参数错误
    UNAUTHORIZED = 401       # 未认证/认证失败
    NO_PERMISSION = 403      # 无权限
    NOT_FOUND = 404          # 资源不存在
    RATE_LIMITED = 429       # 请求过于频繁
    SERVER_ERROR = 500       # 服务器内部错误


class Rating:
    """满意度取值"""
    SATISFIED = 1       # 满意
    UNSATISFIED = -1    # 不满意
    # NULL = 未评价
