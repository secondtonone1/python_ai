'''
演示单例模式
'''

'''
单例模式，就是无论同一个类创建多少对象，都是同一个对象
网络编程，TcpServer, DBManager
'''

class Singleton(object):
    # 类属性
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

a = Singleton()
b = Singleton()
print(a is b)
print(f'id(a) is {id(a)}')
print(f'id(b) is {id(b)}')