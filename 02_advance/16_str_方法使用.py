'''
演示new方法
'''
class Person:
    def __init__(self,name):
        self.name=name
    # 打印对象的时候会输出__str__返回的字符串
    def __str__(self):
        return f'我的名字是: {self.name}'

    # 用于调试的字符串输出
    def __repr__(self):
        return f'in __repr__ 我的名字是: {self.name}'

if __name__ == '__main__':
    '''
    __str__和__repr__都能在打印的时候输出指定的字符串
    如果实现了__str__优先调用__str__
    否则没有实现__str__再去查找__repr__
    '''
    p = Person('Zack')
    # 默认调用__str__
    print(f'p is {p}')
    # 显示调用repr
    print(repr(p))
    # 显示调用str
    print(str(p))
