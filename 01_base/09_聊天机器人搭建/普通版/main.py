"""
该模块用于充当 聊天机器人的前端模块, 即: 接收用户录入的问题, 调用 chat_utils模块的 get_response()函数, 获取模型处理结果.
并通过 streamlit 在前端页面展示即可.
"""

# 1. 导包
import streamlit as st
import chat_utils

# 3. 标题
st.title('🤖恋恋风辰zack的小助手')
st.divider()
st.header("💬 AI 聊天对话窗口")

# 4. 初始化会话状态
if 'messages' not in st.session_state:
    # 如果没有历史记录，创建欢迎语
    welcome_msg = {'role': 'assistant', 'content': '你好, 我是恋恋风辰zack的助手, 有什么可以帮助您的吗?👋'}
    st.session_state['messages'] = [welcome_msg]

# 5. 遍历并显示所有消息记录
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# 6. 接收用户录入的问题
prompt = st.chat_input('请录入您的问题: ')

# 9. 处理用户输入
if prompt:
    # 添加用户消息
    user_message = {'role': 'user', 'content': prompt}
    # 加入历史记录
    st.session_state['messages'].append(user_message)
    # 将文本显示在窗口中
    st.chat_message('user').markdown(prompt)
    with st.spinner('AI小助理正在思考中...'):
        # 调用大模型获取答案
        response_text = chat_utils.get_response_list(st.session_state.messages)
        ai_message = {'role': 'assistant', 'content': response_text}
        # 加入历史记录
        st.session_state['messages'].append(ai_message)
        st.chat_message('assistant').markdown(response_text)

