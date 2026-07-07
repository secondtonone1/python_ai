
# 自定义一个带参数的装饰器，模仿functools.wraps这个函数
def func_wrapper(func):
    # func是函数接受的参数，原函数
    def decorator(fn):
        # fn相当于另一个开发者实现的装饰器中的inner函数
        # 不是下面的inner函数
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)
        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        return inner
    return decorator


def timer(func):
    @func_wrapper(func)
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