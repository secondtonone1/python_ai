"""
该模块用于充当 聊天机器人的前端模块, 即: 接收用户录入的问题, 调用 chat_utils模块的 get_response()函数, 获取模型处理结果.
并通过 streamlit 在前端页面展示即可.
"""

# 1. 导包
import streamlit as st
from chat_utils import get_response_list
from db_utils import ChatDatabase


# 2. 初始化数据库连接
@st.cache_resource
def init_database():
    """初始化数据库连接（使用缓存避免重复连接）"""
    return ChatDatabase()


# 3. 标题
st.title('恋恋风辰zack的小助手')

# 4. 初始化数据库
try:
    db = init_database()
    # 验证连接是否有效，无效则重连
    if not db.is_connected():
        st.warning("⚠️ 数据库连接已断开，正在重新连接...")
        if not db.reconnect():
            st.error("❌ 数据库连接失败，请检查数据库配置")
            st.stop()
except Exception as e:
    st.error(f"❌ 数据库初始化失败: {e}")
    st.stop()

# 5. 初始化会话状态
if 'messages' not in st.session_state:
    # 从数据库加载历史记录
    loaded_messages = db.load_all_messages(limit=100)

    if loaded_messages and len(loaded_messages) > 0:
        st.session_state.messages = loaded_messages
        st.success(f"✅ 已从数据库加载 {len(loaded_messages)} 条历史记录")
    else:
        # 如果没有历史记录，创建欢迎语
        welcome_msg = {'role': 'assistant', 'content': '你好, 我是恋恋风辰zack的助手, 有什么可以帮助您的吗?👋'}
        st.session_state.messages = [welcome_msg]
        # 保存欢迎语到数据库
        if not db.save_message(welcome_msg['role'], welcome_msg['content']):
            st.warning("⚠️ 欢迎语保存失败，但不影响使用")

# 6. 添加侧边栏功能
with st.sidebar:
    st.header("📊 聊天统计")
    message_count = db.get_message_count()
    st.metric("总消息数", message_count)

    st.divider()

    # 清空记录按钮
    if st.button("🗑️ 清空所有记录", type="secondary"):
        if db.clear_all_messages():
            welcome_msg = {'role': 'assistant', 'content': '你好, 我是恋恋风辰zack的助手, 有什么可以帮助您的吗?👋'}
            st.session_state.messages = [welcome_msg]
            db.save_message(welcome_msg['role'], welcome_msg['content'])
            st.success("✅ 已清空所有记录")
            st.rerun()
        else:
            st.error("❌ 清空记录失败")

# 7. 遍历并显示所有消息记录
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# 8. 接收用户录入的问题
prompt = st.chat_input('请录入您的问题: ')

# 9. 处理用户输入
if prompt:
    # 添加用户消息
    user_message = {'role': 'user', 'content': prompt}
    st.session_state.messages.append(user_message)
    st.chat_message('user').markdown(prompt)

    # 保存用户消息到数据库
    if not db.save_message(user_message['role'], user_message['content']):
        st.warning("⚠️ 消息保存失败，但继续处理")

    # 获取AI回复
    with st.spinner('AI小助理正在思考中...'):
        try:
            response = get_response_list(st.session_state.messages)
        except Exception as e:
            st.error(f"❌ AI 处理失败: {e}")
            response = "抱歉，我暂时无法处理您的请求，请稍后重试。"

    # 添加AI回复
    assistant_message = {'role': 'assistant', 'content': response}
    st.session_state.messages.append(assistant_message)
    st.chat_message('assistant').markdown(response)

    # 保存AI回复到数据库
    if not db.save_message(assistant_message['role'], assistant_message['content']):
        st.warning("⚠️ 回复保存失败，但已显示在界面上")