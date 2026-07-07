def print_info(func):
    def inner(x,y):
        print('努力计算中...')
        # 接受原函数的返回值
        res = func(x,y)
        print('计算成功...')
        return res
    return inner

@print_info
def get_sum(x,y):
    return x+ y

print(get_sum(1,2))