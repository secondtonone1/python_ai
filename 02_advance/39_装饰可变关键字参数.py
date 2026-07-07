
def decorator(func):
    # 内层函数接受可变关键字参数
    def inner(**kwargs):
        print('努力计算中...')
        # kwargs本质上是一个字典
        # **kwargs就是将字典中的数据拆包，拆成1个1个的key=value的形式
        print(f'kwargs = {kwargs}')
        result = func(**kwargs)
        print('计算成功')
        return result
    return inner

@decorator
def sum(a,b):
    return a+b
# 因为inner无法接受可变位置参数
# print(sum(1,2))

# inner可以接受可变关键字参数
print(sum(a = 1, b = 2))


