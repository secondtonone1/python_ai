'''
演示new方法
'''
class Person:
    # cls是类名,name是形参接受实参
    # __new__的形参取决于接受的实参的个数
    def __new__(cls,name):
        print(f'__new__:创建对象')
        # 一层一层向上找，直到找到object的__new__方法
        # object的__new__方法是创建对象的
        obj = super().__new__(cls)
        return obj
    # self 存储的是对象，这个对象从__new__返回的
    def __init__(self,name):
        print(f'__init__: 初始化对象')
        self.name=name

class A:
    def __new__(cls):
        print('创建失败')
        return None
    def __init__(self):
        print('初始化')

if __name__ == '__main__':
    '''
    下面的创建对象的流程，相当于
    obj = Person.__new__(Person, 'Tom')
    obj = Person.__init__(obj,'Tom')
    '''
    p = Person('Tom')
    print(p.name)
    '''
    因为A类的new方法返回的是None, 所以不会调用init方法
    '''
    a = A()
