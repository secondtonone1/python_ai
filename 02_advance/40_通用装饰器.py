'''
这是通用装饰器
'''

def decorator(func):
    def inner(*args, **kwargs):
        print(f'努力计算中...')
        print(f'args = {args}')
        print(f'kwargs = {kwargs}')
        # 元组，字典拆包
        # args相当于元组，*args相当于将元组拆解成可变位置参数
        # kwargs相当于字典，**kwargs相当于将字典拆解为可变关键字参数
        return func(*args, **kwargs)
    return inner

@decorator
def sum(*args,**kwargs):
    '''
    需求，对元组中的所有数据求和，对字典中的value求和
    :param args: args是可变位置参数打包后的元组
    :param kwargs: kwargs是可变关键字参数打包后的字典
    :return:
    '''
    sum = 0
    # 遍历元组求和
    for arg in args:
        sum += arg

    # 遍历字典的value求和
    for value in kwargs.values():
        sum += value
    return sum

print(sum(1,2,3, a = 4, b=5, c = 6))
# 打印sum函数的名字
print(f'sum.__name__ = {sum.__name__}')
# 打印函数的文档
print(f'sum.__doc__ = {sum.__doc__}')
