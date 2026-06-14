'''
演示方法重写
'''

class Animal(object):
    def __init__(self, name):
        self.name = name

    def speak(self):
        print('动物咆哮')

    def introduce(self):
        print(f'我是一只动物,我叫{self.name}')

class Dog(Animal):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    # 子类重新实现了父类的introduce方法，
    # 将来子类对象调用introduce，会触发子类的introduce方法
    def introduce(self):
        print(f'我是一只小狗，我叫{self.name}')

    def speak(self):
        print('小狗汪汪汪叫...')

dg = Dog('旺财',2)
# 子类对象调用自己的introduce
dg.introduce()
dg.speak()

# 子类对象具体调用哪个类的方法，取决于mro的查找顺序
print(Dog.__mro__)
