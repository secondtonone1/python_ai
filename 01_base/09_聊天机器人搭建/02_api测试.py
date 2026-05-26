import ollama

# 2.定义函数, 给大语言模型发送请求, 并获取其处理结果(聊天机器人的回答)
def get_response(prompt):
    # 2.1 发起请求, 获取响应信息
    response = ollama.chat(model='deepseek-r1:1.5b', messages=[{'role':'user', 'content': prompt}])
    # 2.2 返回模型处理后的结果(即: 聊天机器人的回答)
    return response['message']['content']

if __name__ == '__main__':
    print(get_response('给我一份AI学习攻略'))