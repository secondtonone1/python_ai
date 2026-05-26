'''
这是一个聊天的工具类，用来调用ollama大模型
'''
# 1.导包
import ollama
# 2. 定义函数，给大模型发送请求，并获取处理结果
def get_response(prompt):
    # 2.1发送请求获取响应
    response = ollama.chat(model='deepseek-r1:1.5b',messages=[
        {'role': 'user',
         'content': prompt,}
    ])
    # 2.2 获取模型处理的结果(文本信息)
    return response['message']['content']

def get_response_list(prompt_list):
    '''
    根据历史提示词记录列表，选出最近的20条，作为消息发送给大模型，从而形成记忆功能。
    :param prompt_list:提示词列表, [{'role': 'user','content':'AI怎么学'},
    {'role':'asssistant', 'content': '去kaggle学习'},
    {'role':'user','content':'还有什么方法'}
    ...]
    :return: 大模型的回答文本
    '''
    # 获取列表中最近的20条记录，作为参考发送给大模型
    response = ollama.chat(model='deepseek-r1:1.5b',messages=prompt_list[-20:])
    # 2.2 获取模型处理的结果(文本信息)
    return response['message']['content']

if __name__ == '__main__':
    #print(get_response('您好，学习AI有哪些方式?'))
    message_list = [{'role':'user','content':'您好，学习AI有哪些方式?'},
                    {'role':'assistant','content':'''
                        <think>

</think>

学习AI可以通过多种方式实现：

### 1. **人工智能课程**
   - 参加高校或培训机构的AI相关课程。
   - 国内外知名大学的在线课程（如Coursera、Udacity等）。

### 2. **自学与实践**
   - 学习AI的基础知识，如机器学习、深度学习。
   - 利用编程语言（如Python、R）、工具（如TensorFlow、PyTorch）进行实践。

### 3. **实战项目**
   - 参加 hackathons或竞赛，提升实际应用能力。

### 4. **开源项目开发**
   - 负责AI项目，如Deep Learning框架的实现。

### 5. **加入社区**
   - 移民社区、学术研究小组等平台参与讨论和交流。

### 6. **技术培训**
   - 参加行业或专业培训，提升技能。

### 7. **企业实习**
   - 在科技公司或创业团队中实践AI应用。

### 8. **参加比赛**
   - 参加数据科学、机器学习等竞赛，提升实战能力。

### 9. **阅读文献**
   - 学习相关论文和书籍，深入理解AI技术。

### 10. **参与开源项目**
   - 协助开发或管理AI相关的开源项目。

通过以上方式，可以有效掌握和应用人工智能知识。
                    '''},
                    {
                        'role':'user',
                        'content':'还有什么推荐吗?'
                    }
                    ]
    print(get_response_list(message_list))
