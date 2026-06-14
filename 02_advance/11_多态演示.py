'''
演示多态用法
'''

'''
用一个父类对象引用子类对象，通过父类对象调用方法，能够触发子类对象的方法
这种机制就是多态

多态必要条件:
1. 必须要有继承关系
2. 子类重写父类方法
3. 父类对象引用子类对象
'''

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f'我叫{self.name}, 通过动物咆哮')


class Dog(Animal):
    def speak(self):
        print(f'我叫{self.name}，叫声汪汪汪')

class Cat(Animal):
    def speak(self):
        print(f'我叫{self.name}，叫喵喵喵')

class Duck(Animal):
    def speak(self):
        print(f'我叫{self.name}，叫声嘎嘎嘎')

def animal_speak(animal:Animal):
    animal.speak()

if __name__ == '__main__':
    animal_speak(Animal('动物',8))
    animal_speak(Dog('小狗',7))
    animal_speak(Cat('小猫',4))
    animal_speak(Duck('鸭子',3))







