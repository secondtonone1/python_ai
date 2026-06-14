'''
子类调用父类的方法
'''

'''
子类调用父类的方法
方法1
super().方法名(参数1,参数2,参数3...)
方式2
父类名.方法名(self,参数1,参数2,参数3...)
'''
class Animal:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print(f'我是一只动物,我叫{self.name}')

class Dog(Animal):
    def __init__(self, name,color):
        Animal.__init__(self, name)
        self.color = color
    def introduce(self):
        Animal.introduce(self)
        print(f'我的颜色是{self.color}')

dog = Dog('旺财','蓝色')
dog.introduce()
