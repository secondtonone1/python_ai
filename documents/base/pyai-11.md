---
title: 实现聊天机器人
date: 2026-05-19 17:03:22
tags: tags: [python,AI]
categories: [python,AI]
---

## 前情回顾

前面我们实现了聊天机器人的基本界面。

这里我们稍作修改，进行简化

``` python
"""
该模块用于充当 聊天机器人的前端模块, 即: 接收用户录入的问题, 调用 chat_utils模块的 get_response()函数, 获取模型处理结果.
并通过 streamlit 在前端页面展示即可.
"""

# 1. 导包
import streamlit as st

# 3. 标题
st.title('🤖恋恋风辰zack的小助手')
st.header("💬 AI 聊天对话窗口")

# 4. 初始化会话状态
if 'messages' not in st.session_state:
    # 如果没有历史记录，创建欢迎语
    welcome_msg = {'role': 'assistant', 'content': '你好, 我是恋恋风辰zack的助手, 有什么可以帮助您的吗?👋'}
    st.session_state.messages = [welcome_msg]

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
    st.session_state.messages.append(user_message)
    st.chat_message('user').markdown(prompt)


```

界面效果如下

![image-20260519171848959](https://cdn.llfc.club/image-20260519171848959.png)

## python请求ollama

之前我们是通过apifox或者浏览器发送http请求的

这里介绍使用ollama的包发送请求

具体参考文档地址

https://github.com/ollama/ollama-python

### 安装ollama库

``` bash
pip install ollama
```

### 非流式访问

``` python
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='gemma3', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)
```

### 流式访问

``` python
from ollama import chat

stream = chat(
    model='gemma3',
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)
```

当然可以通过代码访问云端api, 这里不再赘述

### 测试案例

我们可以实现一个代码访问本地ollama的deepseek-r1:1.5b模型

``` python
# 1. 导包
import ollama

# 2.定义函数, 给大语言模型发送请求, 并获取其处理结果(聊天机器人的回答)
def get_response(prompt):
    # 2.1 发起请求, 获取响应信息
    response = ollama.chat(model='deepseek-r1:1.5b', messages=[{'role':'user', 'content': prompt}])
    # 2.2 返回模型处理后的结果(即: 聊天机器人的回答)
    return response['message']['content']
```

调用

``` python
print(get_response('给我一份AI学习资料'))
```

打印输出如下

``` markdown
D:\ProgramData\anaconda3\python.exe D:\workspace\github\python_ai\01_base\09_聊天机器人搭建\02_api测试.py 
<think>
嗯，用户让我给他一份关于AI学习的攻略。首先，我得弄清楚他到底需要什么。可能他是刚开始接触AI，或者想深入学习这个领域。也有可能是希望系统地规划自己的学习路径。

那我要考虑哪些部分呢？通常，学习攻略会有基础的学习方法、适合的课程类型、以及长期目标这几个方面。用户可能希望从多个角度入手，帮助他有效学习AI。

基础学习方法方面，我应该建议一些经典算法和框架，比如深度学习中的CNN、RNN这些。然后推荐一些入门书籍或文章，这样他可以有一个起点。此外，实践是关键，所以编程练习和实战项目很重要。另外，持续学习和更新知识也是必须的，毕竟AI领域变化挺快的。

适合的学习课程类型方面，系统课程可能更全面，但需要一定的时间投入。在线课程则相对灵活，容易安排学习计划。混合型课程可以结合两种方法，这样用户可以根据自己的情况选择最适合自己节奏的课程。

长期目标和持续学习部分也很重要。目标设定要明确，不能太急或太慢。定期评估进步，并进行调整，这能让学习过程更有条理。同时，保持对新技术的关注，及时了解最新的发展动态。

最后，工具推荐是必不可少的。Python、TensorFlow这些编程语言和框架已经很普及了，现在可以结合这些工具来实践。如果需要更深入的学习，可能还要考虑相关领域的书籍或者研究论文。

总的来说，这份攻略应该涵盖基础学习、适合的课程类型、长期目标以及工具推荐等方面，帮助用户系统地学习AI，并在实践中提升自己的能力。
</think>

当然！以下是一份关于AI学习的攻略，涵盖了基础知识、学习方法和实践建议：

---

### **AI学习攻略**

#### **1. 基础学习**
   - **了解核心概念**：从机器学习的基本原理开始，逐步深入到深度学习、神经网络等人工智能的核心领域。
   - **经典算法与框架**：
     - **深度学习**：学习Convolutional Neural Networks (CNN)、Recurrent Neural Networks (RNN)、LSTM (长短期记忆网络)、Transformer等模型。
     - **计算机视觉**：掌握OpenCV、PyTorch等工具，学习图像处理、目标检测、语音识别等任务。
     - **自然语言处理（NLP）**：学习NLP的基本概念和框架，如Word2Vec、BERT等模型。
   - **编程与实践**：
     - 学习Python（特别是深度学习相关的库如PyTorch和TensorFlow）。
     - 实践项目：从简单的分类任务到复杂的人工智能项目，逐步提升自己的编程能力和解决问题的能力。

#### **2. 适合的课程类型**
   - **系统课程**：通过在线平台或教材购买系统化的AI基础课程，通常包含理论知识和实践训练。
   - **混合型课程**：
     - **深度学习课程**：结合神经网络理论与代码实践，适合对技术感兴趣的学生。
     - **应用课程**：专注于特定领域（如计算机视觉、NLP、语音识别等）的AI应用。
     - **在线资源**：通过Coursera、Udemy等平台获取免费或低_cost的教程和视频课程。
   - **实践型课程**：
     - 适合需要 hands-on 实践的学生，通常会包括编程项目和团队合作。

#### **3. 长期目标**
   - **短期目标**：完成基础课程，了解核心概念并开始简单的AI应用。
   - **中期目标**：学习高级模型（如GPT、Transformer）以及相关的NLP技术。
   - **长期目标**：
     - 进入研究机构或公司从事AI相关的工作。
     - 等待更多资源后进行进一步的扩展和深入。

#### **4. 持续学习**
   - AI领域不断更新，新模型、新技术层出不穷。定期回顾和反思自己的学习效果，及时调整学习计划。
   - 关注行业动态：学习最新的AI工具和技术趋势，确保学习内容与市场需求同步。

#### **5. 工具推荐**
   - **编程语言**：
     - Python（基本）、PyTorch、TensorFlow、Keras、Rustc pytorch框架。
   - **框架与库**：
     - PyTorch：适合深入理解神经网络的框架。
     - TensorFlow：广泛用于AI项目和研究。
     - NumPy：高效的数据处理工具。
     - OpenCV：处理图像相关的任务。
   - **机器学习基础**：
     - Scikit-learn、Pandas、Matplotlib等库，用于数据分析和可视化。

---

### **总结**
AI学习是一个系统而持续的过程。从基础的学习开始，逐步深入到高级技术，并通过实践来提升自己的能力。希望这份攻略能帮助你快速掌握AI的基础知识，开启一段有意义的AI学习之旅！

Process finished with exit code 0

```

**列表请求**

有时候我们为了让AI具备记忆，需要发送历史会话记录列表给大模型

``` python
# 3. 因为前端传过来的问题, 是 列表 + 字典的形式, 即: 已经符合Ollama API的格式了, 我们无需做处理, 直接用.
def get_response_list(prompt):
    # 2.1 发起请求, 获取响应信息
    response = ollama.chat(model='deepseek-r1:1.5b', messages=prompt[-20:])
    # 2.2 返回模型处理后的结果(即: 聊天机器人的回答)
    return response['message']['content']
```

比如我们组织

``` python
prompt = [
    {
        'role':'user', 
        'content': '学习AI有什么途径？'
    },
    {
       'role':'assistant', 
        'content': 'AI相关资料的网站,机器学习图书，论坛等'  
    },
    {
         'role':'user', 
        'content': '还有哪些呢？'
    }
]
```

大模型回答

``` json
'message' : {
    'content':'还可以去github上搜索相关项目',
    'role': 'assistant'
}
```

## 综合整理

``` python
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
    # 调用大模型获取答案
    response_text = chat_utils.get_response_list(st.session_state.messages)
    ai_message = {'role': 'assistant', 'content': response_text}
    # 加入历史记录
    st.session_state['messages'].append(ai_message)
    st.chat_message('assistant').markdown(response_text)


```







