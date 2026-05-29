'''
演示类的继承
'''
# 父类
class Person(object):
    def eat(self):
        print('吃东西')
    def sleep(self):
        print('睡觉')

# 子类, 拥有了父类的属性和方法
class Student(Person):
    pass

# 教师类
class Teacher(Person):
    pass

s1 = Student()
# 拥有了父类的属性和方法
s1.eat()
s1.sleep()

t1 = Teacher()
t1.eat()
t1.sleep()

# 首先去Student中查找，如果Student中没有去Person查找，如果Person也没有去Object查找
# 如果最后都没有找到该方法，则报错
# s1.play_game()
# 打印Student对象的方法查找顺序
# (<class '__main__.Student'>, <class '__main__.Person'>, <class 'object'>)
print(Student.__mro__)

# 动物类
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 私有方法, 咆哮
    def __roar(self):
        print('野性的呼唤，原始觉醒')

# 猫类
class Cat(Animal):
    pass

class Dog(Animal):
    # Dog类的__init__方法会覆盖掉父类同名的__init__方法
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.type = 'dog'

class Bird(Animal):
    # 将共性属性的初始化放入Animal，调用Animal的__init__方法
    # 将Bird特性的属性的初始化放入Bird
    def __init__(self, name, age, type):
        # 调用父类的__init__方法
        super().__init__(name, age)
        # 特性属性的初始化
        self.type = type

# 调用的是Animal的__init__方法
cat = Cat('小猫',5)
# 创建Dog实例
dog = Dog('小狗',6)
print(dog.type)
# 创建鸟类实例
bird =  Bird('小鸟',200,'金雕')
print(bird.type)
print(bird.age)
print(bird.name)
print('😔'*50)
# 在Bird的__dict__看不到从父类继承的方法
print(Bird.__dict__)
# 在Animal中看到私有方法__roar改名了_Animal__roar
print(Animal.__dict__)
# 可以理解为_Animal__roar被Bird类继承了
# 根据__mro__顺序去查找，先查找Bird类，没有_Animal__roar
# 继续去上一级Animal查找，找到_Animal__roar
bird._Animal__roar()

class BaseA:
    def show(self):
        print('BaseA show')

class BaseB:
    def show(self):
        print('BaseB show')

class C(BaseA, BaseB):
    pass

c = C()
print('😔'*50)
c.show()

# 查看C的__mro__顺序
# (<class '__main__.C'>, <class '__main__.BaseA'>, <class '__main__.BaseB'>, <class 'object'>)
print(C.__mro__)
