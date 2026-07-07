'''
演示闭包进阶知识
'''

def outer():
    num = 100
    age = 20
    def inner():
        print(num)
        print(age)
    return inner

fn = outer()
# 查看自由变量的名称
print(fn.__code__.co_freevars)
# 查看闭包中保存的变量对象
print(fn.__closure__)