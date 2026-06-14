'''
演示迭代器实现
'''

class Counter:
    def __init__(self,max_num):
        self.max_num = max_num
        self.current = 0

    # 返回迭代器对象
    def __iter__(self):
        '''
        返回可迭代对象
        :return:
        '''
        return self

    # 返回一个值
    def __next__(self):
        '''
        next函数接受的是一个可迭代对象
        :return:
        '''
        if self.current < self.max_num:
            self.current += 1
            return self.current
        # 抛出停止异常
        raise StopIteration

if __name__ == '__main__':
    counter = Counter(2)
    # 可以通过next从迭代器中获取数据
    print(next(counter))
    print(next(counter))
    try:
        print(next(counter))
    except StopIteration:
        print('迭代停止...')
    print('😔'*20)
    # 可以使用for循环
    counter2 = Counter(3)
    for num in counter2:
        print(num)

