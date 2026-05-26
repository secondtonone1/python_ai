"""
该模块用于充当 聊天机器人的后端模块, 即: 接收前端(Streamlit)传过来的用户的问题,
交给大语言模型(Qwen, DeepSeek-r1等), 获取其相应结果, 并返回(给前端)
"""

# 1. 导包
import ollama

# 2.定义函数, 给大语言模型发送请求, 并获取其处理结果(聊天机器人的回答)
def get_response(prompt):
    # 2.1 发起请求, 获取响应信息
    response = ollama.chat(model='deepseek-r1:1.5b', messages=[{'role':'user', 'content': prompt}])
    # 2.2 返回模型处理后的结果(即: 聊天机器人的回答)
    return response['message']['content']


# 3. 因为前端传过来的问题, 是 列表 + 字典的形式, 即: 已经符合Ollama API的格式了, 我们无需做处理, 直接用.
def get_response_list(prompt):
    # 2.1 发起请求, 获取响应信息
    response = ollama.chat(model='deepseek-r1:1.5b', messages=prompt[-20:])
    # response = ollama.chat(model='deepseek-r1:1.5b', messages=prompt[-20:])

    # 2.2 返回模型处理后的结果(即: 聊天机器人的回答)
    return response['message']['content']



# 4. 测试自定义的 工具函数.
if __name__ == '__main__':
    prompt = '给我一份数据结构和算法学习大纲'
    response = get_response(prompt)
    print(response)
