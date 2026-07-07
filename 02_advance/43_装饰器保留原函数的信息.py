import functools

def timer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@timer
def calc():
    '''数值计算函数'''
    pass

# 打印函数名字
print(calc.__name__)
print(calc.__doc__)