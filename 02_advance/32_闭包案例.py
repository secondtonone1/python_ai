'''
思路：
1. 可以通过外部函数func返回内部函数
2. 内部函数调用的这个参数累加到闭包的自由变量中，内部函数返回累加后的结果
'''

def func():
    result = 0
    def inner(num2):
        nonlocal result
        result += num2
        return result
    return inner

if __name__ == '__main__':
    g = func()
    print(g(1))
    print(g(2))
    print(g(3))