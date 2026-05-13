'''
演示函数传参
'''

'''
函数内部定义的参数是形参
函数调用时传递的参数是实参
'''
def play_game(name):
    '''
    打游戏的函数
    :param name: 用户名, 形参
    :return: str,返回值
    '''
    return name + '正在打游戏'

# 函数调用
print(play_game('小丽'))