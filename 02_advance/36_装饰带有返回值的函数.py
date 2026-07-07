def print_info(func):
    def inner():
        print(f'友好提示，正在努力计算中...')
        res = func()
        print(f'计算成功...')
        # 返回原函数调用结果
        return res
    return inner



@print_info
def get_sum():
    return 20 + 38


print(get_sum())