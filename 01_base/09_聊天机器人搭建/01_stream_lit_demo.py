import streamlit as st
# 页面配置
st.set_page_config(
    page_title='Streamlit 聊天机器人教学版',
    page_icon = '🤖',
    layout = 'wide'
)

# 页面标题
st.title('🤖 Streamlit AI 聊天机器人演示')
st.markdown('### 核心功能：各类用户输入控件 + 标准聊天界面')
st.divider()
# 侧边栏
with st.sidebar:
    st.title('⚙️ 机器人设置')
    bot_name = st.text_input("机器人名称",value='智能助手')
    model_mode = st.selectbox(
        "选择对话模型风格",
        ["通用闲聊", "专业技术问答", "文案创作", "心理咨询"]
    )
    reply_len = st.radio('回复长度',['简短','中等','详细'])
    enable_func =  st.multiselect(
        '开启附加功能',
        ["联网搜索", "代码解释", "翻译", "总结"]
    )
    temperature =  st.slider(
        "AI 创意程度",
        min_value=0.0,
        max_value=1.0,
        value = 0.7,
        step = 0.1
    )
    auto_clean = st.checkbox('发送后自动清空输入', value = False)

# 主页面, 用户信息输入区域
st.header('👤 用户信息输入区')
col1, col2 = st.columns(2)
with col1:
    user_nick = st.text_input('您的昵称',placeholder="请输入您的昵称...")
    user_age = st.number_input('您的年龄', min_value=0, max_value=120, value=25)
with col2:
    user_gender = st.selectbox('性别',['男','女','保密'])
    user_mood = st.slider('当前的心情指数',0,10,5)

st.divider()

# 核心模块：聊天窗口
st.header("💬 AI 聊天对话窗口")
# 如果输入框,text_input, number_input, chat_input里面的内容有变化，则代码从上到下重新执行
# 导致变量被清空, 不能用普通变量存储消息记录
# chat_list = []
# print('initial: ', chat_list)
# 可以使用session_state记录消息，不会随着每次页面更新导致代码失效
if 'messages' not in st.session_state:
    st.session_state['messages']= []
else:
    for data in st.session_state['messages']:
        with st.chat_message(data['role']):
            st.markdown(data['content'])

user_input = st.chat_input('请在这里输入您想问的问题...')
if user_input:
    # chat_list.append({'role':'user','content':user_input})
    # print('after_append',chat_list)
    # print(user_input)
    # 使用st中提供的消息缓存机制seesion_state存储记录
    st.session_state['messages'].append({'role':'user','content':user_input})
    # print(st.session_state['messages'])
    with st.chat_message('user'):
        st.markdown(user_input)

    # 模拟AI回复（可替换为大模型API调用）
    ai_reply = f"""
    你好 {user_nick if user_nick else "朋友"}！👋
    你当前的心情指数：{user_mood}分（满分10分）
    你发送的内容：{user_input}
    ---
    🤖 机器人配置：
    - 机器人名称：{bot_name}
    - 对话模式：{model_mode}
    - 回复长度：{reply_len}
    - AI创意度：{temperature}
    - 开启功能：{", ".join(enable_func) if enable_func else "无"}
    ---
    提示：此为模拟回复，替换大模型API后可实现真实AI对话！
    """
    st.session_state['messages'].append({'role':'assistant','content':ai_reply})
    with st.chat_message('assistant'):
        st.markdown(ai_reply)
    # 如果自动清空聊天记录，则调用st.reruan，相当于刷新浏览器
    if auto_clean:
        st.rerun()
# 点击了清空聊天记录的按钮
if st.button("🔄 清空全部聊天记录"):
    st.session_state['messages'] =[]
    st.rerun()