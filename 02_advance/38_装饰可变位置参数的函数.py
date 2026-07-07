
def decorator1(func):
    # 内层函数接受可变位置参数
    def inner(*args):
        print('努力计算中...')
        print(f'args: {args}')
        # args本质上是一个元组，
        # *args就是将元组中的数据拆包，拆成1个1个的位置参数
        result = func(*args)
        print('计算成功')
        return result
    return inner

@decorator1
def sum(a,b):
    return a+b

print(sum(1,2))

@decorator1
def sum2(a,b, c,d):
    return a+b+c+d

print(sum2(1,2,3,4))
# 调用失败，inner接受的是可变位置参数
# sum(a = 1, b = 2)

