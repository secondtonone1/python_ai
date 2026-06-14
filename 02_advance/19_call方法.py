'''
演示call方法
'''

class Add(object):
    def __call__(self, a, b):
        return a + b

if __name__ == '__main__':
    add = Add()
    # 将对象像函数一样使用，可以触发__call__方法
    print(add(3,5))