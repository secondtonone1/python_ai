'''
演示闭包基本操作
'''
'''
闭包条件
1. 函数嵌套
2. 内部函数使用外部函数的变量
3. 外部函数返回内部函数
'''
# 定义外部函数
def outer_func(num1):
    # 定义内部函数
    def inner_func(num2):
        # 使用外部函数的变量num1
        num = num1 + num2
        print(f'现在的num值:{num}')
    # 返回内部函数
    return inner_func

# 函数名就是函数地址
# 调用外部函数返回内部函数的地址
# fn相当于inner_func, 常驻内存的
fn = outer_func(10)
# 调用闭包函数，等价于inner_func(1)
fn(1)
