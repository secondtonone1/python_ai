def print_info(func):
    def inner(x,y):
        print(f'正在努力计算中...')
        func(x,y)
    return inner


# get_sum = print_info(get_sum)
@print_info
def get_sum(a,b):
    z = a + b
    print(f'两数之和为: {z}')

get_sum(1,2)