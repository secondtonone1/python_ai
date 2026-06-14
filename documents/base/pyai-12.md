---
title: 面向对象编程
date: 2026-05-26 11:36:11
tags: [python,AI]
categories: [python,AI]

---

## 学习目标

1. 理解什么是面向对象编程。
2. 区分类、对象、属性、方法的概念。
3. 能够使用 Python 定义类并创建对象。
4. 理解 `self` 的作用。
5. 掌握构造方法 `__init__` 的使用。
6. 理解封装、继承、多态三大核心思想。
7. 能够用面向对象思想解决简单实际问题。

---

## 为什么需要面向对象

### 面向过程

面向过程的核心思想是：**自顶向下，逐步细化**。

特点：

- 把问题拆成一个个步骤
- 每个步骤用函数实现
- 按顺序执行

示例（报名流程）：

开始 → 提交信息 → 缴费 → 分班 → 结束

问题：

- 数据与行为分离
- 难以维护复杂系统

---

###  面向对象

核心思想：

> 不再关注“做什么步骤”，而是关注“谁来做这些事情”

例如报名系统可以抽象为4个对象：

- 学生
- 教师
- 大学
- 班级

每个对象：

- 有属性（数据）
- 有方法（行为）

---

### 核心对比

| 维度     | 面向过程 | 面向对象 |
| -------- | -------- | -------- |
| 思维方式 | 步骤导向 | 对象导向 |
| 复杂系统 | 难维护   | 易扩展   |
| 代码复用 | 较低     | 更高     |

---

## 什么是类和对象

### 对象

对象是现实世界中具体存在的一个事物。

例如：

- 一个具体的学生：张三
- 一辆具体的汽车：我的白色汽车
- 一只具体的猫：小花
- 一个具体的订单：订单编号 1001

在程序中，对象通常包含两部分：

| 组成 | 含义             | 示例                 |
| ---- | ---------------- | -------------------- |
| 属性 | 对象的数据、特征 | 姓名、年龄、颜色     |
| 方法 | 对象的行为、功能 | 学习、跑步、打印信息 |

### 类

类是对象的模板或设计图。

例如：

- “学生类”是所有学生的模板
- “汽车类”是所有汽车的模板
- “猫类”是所有猫的模板

类和对象的关系可以这样理解：

| 类     | 对象                       |
| ------ | -------------------------- |
| 图纸   | 根据图纸造出来的房子       |
| 模板   | 根据模板创建出来的具体内容 |
| 学生类 | 张三、李四、王五           |
| 汽车类 | 宝马、奔驰、比亚迪         |

一句话总结：

> 类是抽象的，对象是具体的。

---

## 定义类和创建对象

### 定义一个最简单的类

```python
class Student:
    pass
```

说明：

- `class` 是定义类的关键字。
- `Student` 是类名，通常使用大驼峰命名法。
- `pass` 表示暂时不写内容。

###  创建对象

```python
stu1 = Student()
stu2 = Student()

print(stu1)
print(stu2)
```

`stu1` 和 `stu2` 都是通过 `Student` 类创建出来的对象。

它们属于同一个类，但它们是两个不同的对象。

![image-20260526145555982](https://cdn.llfc.club/image-20260526145555982.png)

## 给对象添加属性

对象的属性可以理解为对象的数据。

```python
'''
演示类的基础操作
'''

'''
定义一个类类型
class 类名():
    pass
创建对象
变量 = 类名()
'''
# 学生类
class Student():
    pass

# 创建一个对象赋值给s1
s1 = Student()
# 创建一个对象赋值给s2
s2 = Student()
print(f's1 : {s1}')
print(f's2 : {s2}')

# 为s1添加name属性，属性值为'zack'
s1.name = 'zack'
# 为s1添加age属性,属性值为18
s1.age = 18
print(f's1.age : {s1.age}')
print(f's1.name : {s1.name}')
# s2因为没有添加属性，所以不能通过属性访问
# print(f's2.age : {s2.age}')
```

输出：

```text
张三
18
```

这种方式可以添加属性，但不推荐在正式项目中大量使用，因为每个对象的属性可能不统一。

例如：

```python
stu1.name = "张三"
stu2.score = 95
```

这样会导致对象结构混乱。

更推荐使用构造方法 `__init__` 来统一初始化属性。

---

## 构造方法 

### 什么是构造方法

构造方法是在创建对象时自动执行的方法。

在 Python 中，构造方法的名字固定为：

```python
__init__
```

示例：

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

stu1 = Student("张三", 18)
stu2 = Student("李四", 19)

print(stu1.name, stu1.age)
print(stu2.name, stu2.age)
```

输出：

```text
张三 18
李四 19
```

### self` 是什么

`self` 表示当前对象本身。

当执行：

```python
stu1 = Student("张三", 18)
```

可以理解为：

```python
self 指向 stu1
self.name = "张三"
self.age = 18
```

当执行：

```python
stu2 = Student("李四", 19)
```

可以理解为：

```python
self 指向 stu2
self.name = "李四"
self.age = 19
```

所以 `self` 的作用是：

> 区分当前操作的是哪一个对象。

![image-20260526153451012](https://cdn.llfc.club/image-20260526153451012.png)



### 常见错误

错误写法：

```python
class Student:
    def __init__(name, age):
        name = name
        age = age
```

问题：

1. 少写了 `self`。
2. 没有把数据保存到对象中。
3. `name = name` 只是局部变量赋值，没有意义。

正确写法：

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

---

## 对象方法

方法就是定义在类中的函数，用来描述对象的行为。

```python
'''
讲解init方法
'''

class Student:
    # 当使用Student类创建对象的时候，会调用下面的方法
    def __init__(self,name, age):
        '''
        构造方法
        :param name: 学生的名字
        :param age: 学生的年龄
        :param self: 对象的地址，或者self指向了对象
        '''
        # 为对象添加name属性
        self.name = name
        # 为对象添加age属性
        self.age = age
    # 定义对象的方法自我介绍，不接受实参
    def introduce(self):
        # 将来对象会自动传递给self, 比如s1.introduce, self就是s1
        print(f'您好,我是{self.name}, 我今年{self.age}岁了')
'''
创建一个学生对象, 会自动调用__init__,
1. __init__需要三个参数，第一个self实际是指向了对象的地址，这个对象在调用__init__之前
通过__new__方法就已经创建好，提前在堆空间创建好的， 解释器会自动将这个对象的地址赋值给self
不需要开发者传参
2. name, age需要通过Student('zack',18)传递，将实参传递给name,age两个形参
'''
# 用s1存储Student生成的对象
s1 = Student('zack',18)
# 通过对象.属性的方式访问属性
print(s1.name)
print(s1.age)
# 调用introduce方法, s1会自动传递给self
s1.introduce()
```

输出：

```text
大家好，我叫张三，今年18岁
```

说明：

- `introduce` 是对象方法。
- 对象方法的第一个参数通常也是 `self`。
- 调用方法时，不需要手动传入 `self`。

也就是说：

```python
stu1.introduce()
```

Python 会自动把 `stu1` 传给 `self`。

![image-20260526154826227](https://cdn.llfc.club/image-20260526154826227.png)

---

## 完整示例：学生类

```python
class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def introduce(self):
        print(f"大家好，我叫{self.name}，今年{self.age}岁")

    def show_score(self):
        print(f"{self.name}的成绩是{self.score}分")

    def update_score(self, new_score):
        self.score = new_score
        print(f"{self.name}的成绩已更新为{self.score}分")

stu1 = Student("张三", 18, 95)
stu1.introduce()
stu1.show_score()
stu1.update_score(98)
stu1.show_score()
```

输出：

```text
大家好，我叫张三，今年18岁
张三的成绩是95分
张三的成绩已更新为98分
张三的成绩是98分
```

---

## 类属性和实例属性

### 实例属性

实例属性属于具体对象，每个对象可以拥有不同的值。

```python
class Student:
    def __init__(self, name):
        self.name = name

stu1 = Student("张三")
stu2 = Student("李四")

print(stu1.name)
print(stu2.name)
```

这里的 `name` 就是实例属性。

### 类属性

类属性属于类本身，所有对象可以共享。

```python
class Student:
    # 类属性
    # 学校
    school = '第一中学'
    # 班费
    class_money = 200
    # 定义对象属性
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 创建对象
stu1 = Student('张三', 23)
# 通过对象访问类属性
print(stu1.school)
# 也可通过类名访问类属性
print(Student.school)
# 创建对象李四
stu2 = Student('李四', 24)
print(stu2.school)
# 通过类名修改类属性
Student.school = '第二中学'
print('😀'*50)
print(stu1.school)
print(stu2.school)
# 隐藏bug，看似是通过对象修改类属性，其实是添加对象属性
# 其实是给stu1添加对象属性school
# 因为赋值操作具有二义性，被理解为为stu1添加了一个对象属性school
stu1.school = '第三中学'
print('😀'*50)
print(stu2.school)
print(Student.school)
# 如果通过对象直接使用类属性，做修改不会产生二义性
# 学生stu1花费班费20, 但是赋值会创建新的对象的属性
# 相当于 stu1.class_money = stu1.class_money - 20
# 上述表达式，=右侧的stu1.class_money是类属性，左侧的stu1.class_money是对象属性
stu1.class_money -= 20
print('😀'*50)
print(f'班费{Student.class_money}')
print(f'stu1班费{stu1.class_money}')
# stu2没有对象属性class_money,用的是类属性
print(f'stu2班费{stu2.class_money}')
print('😀'*50)
```

输出：

```text
第一中学
第一中学
第一中学
😀😀😀😀😀😀😀😀😀
第二中学
第二中学
😀😀😀😀😀😀😀😀😀
第二中学
第二中学
😀😀😀😀😀😀😀😀😀
班费200
stu1班费180
stu2班费200
```

### 类属性和实例属性的区别

| 类型     | 所属对象 | 是否共享 | 示例             |
| -------- | -------- | -------- | ---------------- |
| 实例属性 | 具体对象 | 不共享   | `self.name`      |
| 类属性   | 类本身   | 共享     | `Student.school` |

###  示例：统计学生人数

```python
class Student:
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1

stu1 = Student("张三")
stu2 = Student("李四")
stu3 = Student("王五")

print(Student.count)
```

输出：

```text
3
```

---

## 封装

###  什么是封装

封装是指把数据和操作数据的方法放在一起，并对外隐藏不希望直接访问的细节。

简单理解：

> 不让外部随便修改对象内部的数据，而是通过方法来控制访问。

例如，学生成绩不应该被随意设置为负数。

### 未封装的问题

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

stu = Student("张三", 90)
stu.score = -100
print(stu.score)
```

输出：

```text
-100
```

这显然不合理。

### 使用私有属性

在 Python 中，属性名前面加两个下划线，表示私有属性。

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.__score = score

    def get_score(self):
        return self.__score

    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            print("成绩必须在0到100之间")

stu = Student("张三", 90)
print(stu.get_score())

stu.set_score(95)
print(stu.get_score())

stu.set_score(-100)
print(stu.get_score())
```

输出：

```text
90
95
成绩必须在0到100之间
95
```

### 封装的好处

1. 保护数据安全。
2. 控制数据修改规则。
3. 降低外部代码对内部实现的依赖。
4. 让类的使用更加清晰。

---

## 继承

### 本质理解（结合哲学）

继承本质是：**共性 + 个性**

例如：

生物 → 动物 → 哺乳动物 → 人类

- 上层：共性
- 下层：个性

---

###  继承核心作用

1. 代码复用
2. 表达层级关系
3. 提升扩展能力

---

### 基本语法

```python
class 父类:
    pass

class 子类(父类):
    pass
```

---

### 经典案例（强化）

```python
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

```

`__init__`流程说明

``` python
# 动物类
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 猫类
class Cat(Animal):
    pass

# 调用的是Animal的__init__方法
cat = Cat('小猫',5)
```



---

![image-20260529094012124](https://cdn.llfc.club/image-20260529094012124.png)



**方法覆盖**

``` python
# 动物类
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 猫类
class Cat(Animal):
    pass

class Dog(Animal):
    # Dog类的__init__方法会覆盖掉父类同名的__init__方法
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.type = 'dog'

# 调用的是Animal的__init__方法
cat = Cat('小猫',5)
# 创建Dog实例
dog = Dog('小狗',6)
print(dog.type)
```

**通过子类调用父类方法**

``` python
# 动物类
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Bird(Animal):
    # 将共性属性的初始化放入Animal，调用Animal的__init__方法
    # 将Bird特性的属性的初始化放入Bird
    def __init__(self, name, age, type):
        # 调用父类的__init__方法
        super().__init__(name, age)
        # 特性属性的初始化
        self.type = type

# 创建鸟类实例
bird =  Bird('小鸟',200,'金雕')
print(bird.type)
print(bird.age)
print(bird.name)
```



###  私有成员说明（进阶重点）

父类私有方法：

```python
def __private_func(self):
    pass
```

特点：

- 子类不能直接访问
- 本质被改名：_类名__方法名

``` python
# 动物类
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 私有方法, 咆哮
    def __roar(self):
        print('野性的呼唤，原始觉醒')


class Bird(Animal):
    # 将共性属性的初始化放入Animal，调用Animal的__init__方法
    # 将Bird特性的属性的初始化放入Bird
    def __init__(self, name, age, type):
        # 调用父类的__init__方法
        super().__init__(name, age)
        # 特性属性的初始化
        self.type = type


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
```

---

###  多继承

Python 支持多继承：

``` python
class A:
    def show(self):
        print("A")

class B:
    def show(self):
        print("B")

class C(A, B):
    pass

c = C()
c.show()
```

输出：

```
A
```

为什么不是 B？

因为 Python 会按照 **MRO（Method Resolution Order，方法解析顺序）** 查找方法。

查看 MRO：

```
print(C.__mro__)
```

输出类似：

```
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>)
```

所以查找顺序是：

```
C → A → B → object
```

**小结**

- 多继承时，方法查找不是随便找的
- Python 按照 MRO 顺序查找方法
- `类名.__mro__` 可以查看查找顺序
- 初学者应先掌握单继承，再理解多继承和 MRO

---

## 方法重写

### 什么是方法重写

如果子类对父类的方法不满意，可以在子类中重新定义同名方法。

这叫方法重写。

```python
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

```

输出：

```bash
我是一只小狗，我叫旺财
小狗汪汪汪叫...
(<class '__main__.Dog'>, <class '__main__.Animal'>, <class 'object'>)

```

###  为什么需要方法重写

不同子类虽然拥有相同的方法名，但具体表现可能不同。

例如：

- 狗会叫，但叫声是“汪汪”。
- 猫会叫，但叫声是“喵喵”。
- 鸭子会叫，但叫声是“嘎嘎”。

这为多态打下了基础。

---

## 调用父类方法

有时子类并不是完全替换父类方法，而是在父类原有功能基础上增加新功能。

这时可以使用 `super()`。

正确完整代码：

```python
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
        super().__init__(name)
        self.color = color
    def introduce(self):
        super().introduce()
        print(f'我的颜色是{self.color}')

dog = Dog('旺财','蓝色')
dog.introduce()

```

输出：

```text
我是一只动物,我叫旺财
我的颜色是蓝色
```

说明：

- `super().__init__(name)` 调用了父类的构造方法。
- `super().introduce()` 调用了父类的 `introduce` 方法。

![image-20260604223932481](https://cdn.llfc.club/image-20260604223932481.png)

**另外一种调用方式**

``` python
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

```

## 多继承风险

>
>
>```python
>'''
>需求:
>1. 定义一个汽车Car基类，构造方法__init__接受汽车的名字和颜色
>
>2. 定义GasolineCar类，继承自Car, 实现__init__方法，接受参数名字，颜色
>    以及充能方式
>    实现run方法，输出耗油运行
>    实现energy方法，输出默认使用燃油
>    
>3. 定义ElectricCar类, 实现__init__方法，接受参数名字，颜色
>    以及充能方式
>    继承自Car，实现run方法，输出耗电运行
>    实现energy方法，输出默认使用电能
>    
>4. 定义HybridCar类，同时继承自ElectricCar,GasolineCar，
>实现run方法，油电混动运行
>
>5.  实例化一个HybridCar对象，调用energy以及run方法，看看输出
>
>'''
>```

**代码**

``` python
'''
演示多继承隐患
'''

'''
需求:
1. 定义一个汽车Car基类，构造方法__init__接受汽车的名字和颜色

2. 定义GasolineCar类，继承自Car, 实现__init__方法，接受参数名字，颜色
    以及充能方式
    实现run方法，输出耗油运行
    实现energy方法，输出默认使用燃油

3. 定义ElectricCar类, 实现__init__方法，接受参数名字，颜色
    以及充能方式
    继承自Car，实现run方法，输出耗电运行
    实现energy方法，输出默认使用电能

4. 定义HybridCar类，同时继承自ElectricCar,GasolineCar，
实现run方法，油电混动运行

5.  实例化一个HybridCar对象，调用energy以及run方法，看看输出

'''
# 1. 定义一个汽车Car基类，构造方法__init__接受汽车的名字和颜色
class Car(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color

# 2. 定义GasolineCar类，继承自Car, 实现__init__方法，接受参数名字，颜色
#     以及充能方式
class GasolineCar(Car):
    def __init__(self, name, color,energy_type):
        super().__init__(name, color)
        self.energy_type = energy_type

    def run(self):
        print('耗油运行')

    def energy(self):
        print('默认使用燃油')

# 3. 定义ElectricCar类, 实现__init__方法，接受参数名字，颜色
#     以及充能方式

class ElectricCar(Car):
    def __init__(self, name, color, energy_type):
        super().__init__(name, color)
        self.energy_type = energy_type

    def run(self):
        print('耗电运行')

    def energy(self):
        print('默认使用电能')

# 4. 定义HybridCar类，同时继承自ElectricCar,GasolineCar
class HybridCar(ElectricCar, GasolineCar):
    def __init__(self, name, color, energy_type):
        self.name = name
        self.color = color
        self.energy_type = energy_type

    def run(self):
        print('油电混动运行')


if __name__ == '__main__':
    # gc = GasolineCar('宝马','白色','燃油')
    # gc.run()
    # gc.energy()
    #
    # ec = ElectricCar('比亚迪','黑色','电能')
    # ec.run()
    # ec.energy()
    print(HybridCar.__mro__)
    hy_car = HybridCar('比亚迪','黑色','油电混动')
    hy_car.run()
    hy_car.energy()
```

>
>
>如果HybridCar没有实现`__init__`方法, 将会导致通过mro顺序调用上一级的`__init__`方法
>
>而上一级是ElectricCar类，ElectricCar类的`__init__`方法内部又调用了`super()`所以会通过mro找到上一级
>
>这个上一级其实是GasolineCar, 进而造成`__init__`调用参数不匹配而失败
>
>规避的方式第一种即使实现HybridCar的`__init__方法`
>
>第二种方式就是通过父类名.方法名方式显示调用

**第二种方式**

``` python
'''
演示多继承隐患
'''

'''
需求:
1. 定义一个汽车Car基类，构造方法__init__接受汽车的名字和颜色

2. 定义GasolineCar类，继承自Car, 实现__init__方法，接受参数名字，颜色
    以及充能方式
    实现run方法，输出耗油运行
    实现energy方法，输出默认使用燃油

3. 定义ElectricCar类, 实现__init__方法，接受参数名字，颜色
    以及充能方式
    继承自Car，实现run方法，输出耗电运行
    实现energy方法，输出默认使用电能

4. 定义HybridCar类，同时继承自ElectricCar,GasolineCar，
实现run方法，油电混动运行

5.  实例化一个HybridCar对象，调用energy以及run方法，看看输出

'''
# 1. 定义一个汽车Car基类，构造方法__init__接受汽车的名字和颜色
class Car(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color

# 2. 定义GasolineCar类，继承自Car, 实现__init__方法，接受参数名字，颜色
#     以及充能方式
class GasolineCar(Car):
    def __init__(self, name, color,energy_type):
        Car.__init__(self, name, color)
        self.energy_type = energy_type

    def run(self):
        print('耗油运行')

    def energy(self):
        print('默认使用燃油')

# 3. 定义ElectricCar类, 实现__init__方法，接受参数名字，颜色
#     以及充能方式

class ElectricCar(Car):
    def __init__(self, name, color, energy_type):
        Car.__init__(self, name, color)
        self.energy_type = energy_type

    def run(self):
        print('耗电运行')

    def energy(self):
        print('默认使用电能')

# 4. 定义HybridCar类，同时继承自ElectricCar,GasolineCar
class HybridCar(ElectricCar, GasolineCar):

    def run(self):
        print('油电混动运行')


if __name__ == '__main__':
    # gc = GasolineCar('宝马','白色','燃油')
    # gc.run()
    # gc.energy()
    #
    # ec = ElectricCar('比亚迪','黑色','电能')
    # ec.run()
    # ec.energy()
    print(HybridCar.__mro__)
    hy_car = HybridCar('比亚迪','黑色','油电混动')
    hy_car.run()
    hy_car.energy()
```

>
>
>**结论**
>
>当使用多继承时，子类调用父类的方法，一定要用父类名.方法名(参数1,参数2...)

## 多态

### 什么是多态

多态是指不同对象调用相同方法时，表现出不同的行为。

核心特点：

> 相同的方法名，不同的实现效果。

```python
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

```

输出：

```text
我叫动物, 通过动物咆哮
我叫小狗，叫声汪汪汪
我叫小猫，叫喵喵喵
我叫鸭子，叫声嘎嘎嘎
```

### 多态的优势

多态可以让代码更加灵活。可以将抽象类的定义和具体类的实现分离，实现开发的解耦合

同时使用平台，不用随着逻辑的变化而修改，将来只要扩充子类类型即可。

符合高内聚和低耦合的思想。

例如：

```python
def make_sound(animal):
    animal.speak()

make_sound(Dog())
make_sound(Cat())
make_sound(Duck())
```

这个函数不关心传入的是狗、猫还是鸭子，只关心对象有没有 `speak` 方法。

**like方式继承**

like方式就是像的意思，不要求类一定和某一个类实现继承关系，只要这个类具备相似的方法即可。

``` python
'''
演示like继承
'''

class Bird:
    def fly(self):
        print("i can fly")
# is 方式继承，Angle一定是Bird
class Angle(Bird):
    def fly(self):
        print('鹰会飞')
# like 方式继承， Go语言特性interface
class Plane:
    def fly(self):
        print('飞机也会飞')

def func_test_bird(bird:Bird):
    bird.fly()

if __name__ == '__main__':
    angle = Angle()
    func_test_bird(angle)
    plane = Plane()
    func_test_bird(plane)
```

**王者荣耀换肤案例**

``` python
'''
王者荣耀换肤案例
'''
from pyarrow._flight import BasicAuth


# 皮肤基类
class BaseSkin:
    def show(self):
        pass

class XHOriginSkin(BaseSkin):
    def show(self):
        print('没错，我就是呼唤胜利的男神')

class WXJFSkin(BaseSkin):
    def show(self):
        print('我就差一点了,快来砍我')

class BaseHero:
    def __init__(self,name,gender):
        self.name = name
        self.gender = gender
        # 皮肤列表
        self.skins = []

class XHHero(BaseHero):
    def __init__(self,name,gender):
        super().__init__(name,gender)
        # 初始化人物原皮
        skin:BaseSkin = XHOriginSkin()
        self.skins.append(skin)
        # 上一次展示的皮肤
        self.last_skin_index = 0

    # 展示人物
    def show(self):
        self.skins[self.last_skin_index].show()

    # 购买皮肤
    def buy_skin(self, skin:BaseSkin):
        self.skins.append(skin)

    def change_skin(self,index):
        if index >= len(self.skins):
            return
        self.skins[index].show()
        self.last_skin_index = index

if __name__ == '__main__':
    xh_hero = XHHero('夏侯惇','男')
    xh_hero.show()
    # 购买皮肤
    xh_hero.buy_skin(WXJFSkin())
    # 换肤
    xh_hero.change_skin(1)
    # 展示英雄
    xh_hero.show()

```





## 特殊方法

Python 中有一些以双下划线开头和结尾的方法，称为特殊方法，也叫魔术方法。

###  `__str__`

当使用 `print()` 打印对象时，会自动调用对象的 `__str__` 方法。

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"学生姓名：{self.name}，年龄：{self.age}"

stu = Student("张三", 18)
print(stu)
```

输出：

```text
学生姓名：张三，年龄：18
```

如果不定义 `__str__`，直接打印对象通常会看到对象的内存地址信息，不利于阅读。

###  `__repr__`

`__repr__` 更偏向开发者调试使用，通常返回一个更明确的对象描述。

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Student(name={self.name!r}, age={self.age!r})"

stu = Student("张三", 18)
print(repr(stu))
```

输出：

```text
Student(name='张三', age=18)
```

---

## 类方法和静态方法

### 实例方法

最常见的方法是实例方法，第一个参数是 `self`。

```python
class Student:
    def introduce(self):
        print("我是学生")
```

实例方法通常需要访问对象本身的数据。

### 类方法

类方法使用 `@classmethod` 装饰器，第一个参数通常是 `cls`，表示当前类。

```python
class Student:
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1

    @classmethod
    def show_count(cls):
        print(f"当前学生人数：{cls.count}")

Student("张三")
Student("李四")
Student.show_count()
```

输出：

```text
当前学生人数：2
```

### 静态方法

静态方法使用 `@staticmethod` 装饰器。

它不需要访问对象，也不需要访问类。

```python
class MathTool:
    @staticmethod
    def add(a, b):
        return a + b

print(MathTool.add(3, 5))
```

输出：

```text
8
```

### 三种方法对比

| 方法类型 | 第一个参数 | 是否访问实例属性 | 是否访问类属性 |
| -------- | ---------- | ---------------- | -------------- |
| 实例方法 | `self`     | 可以             | 可以           |
| 类方法   | `cls`      | 不直接访问       | 可以           |
| 静态方法 | 无固定参数 | 不访问           | 不访问         |

---

## 面向对象综合案例：银行账户

### 需求分析

设计一个银行账户类 `BankAccount`，要求：

1. 每个账户有账户名和余额。
2. 可以存款。
3. 可以取款。
4. 余额不能小于 0。
5. 可以查看账户信息。

### 代码实现

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"成功存入{amount}元")
        else:
            print("存款金额必须大于0")

    def withdraw(self, amount):
        if amount <= 0:
            print("取款金额必须大于0")
        elif amount > self.__balance:
            print("余额不足")
        else:
            self.__balance -= amount
            print(f"成功取出{amount}元")

    def get_balance(self):
        return self.__balance

    def show_info(self):
        print(f"账户名：{self.owner}，余额：{self.__balance}元")

account = BankAccount("张三", 1000)
account.show_info()
account.deposit(500)
account.withdraw(300)
account.withdraw(2000)
account.show_info()
```

输出：

```text
账户名：张三，余额：1000元
成功存入500元
成功取出300元
余额不足
账户名：张三，余额：1200元
```

###  案例讲解重点

这个案例同时体现了：

1. 类和对象。
2. 构造方法。
3. 实例属性。
4. 私有属性。
5. 封装思想。
6. 方法对数据的控制。

---

## 课堂案例：图书管理

###  需求

设计一个图书类 `Book`，包含：

- 书名
- 作者
- 价格
- 展示图书信息的方法
- 修改价格的方法

### 代码示例

```python
class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.__price = price

    def show_info(self):
        print(f"书名：{self.title}，作者：{self.author}，价格：{self.__price}元")

    def set_price(self, price):
        if price > 0:
            self.__price = price
        else:
            print("价格必须大于0")

    def get_price(self):
        return self.__price

book = Book("Python入门", "王老师", 59.9)
book.show_info()
book.set_price(69.9)
book.show_info()
book.set_price(-10)
```

---

## 课后作业

### 作业 1：商品类

定义一个 `Product` 类，要求：

1. 有商品名称、价格、库存。
2. 价格和库存不能为负数。
3. 有展示商品信息的方法。
4. 有购买商品的方法。
5. 购买时库存减少。
6. 如果库存不足，提示“库存不足”。

### 作业 2：学生管理小系统

定义一个 `Student` 类，包含：

- 姓名
- 年龄
- 成绩

再定义一个 `StudentManager` 类，包含：

- 添加学生
- 删除学生
- 查找学生
- 展示所有学生

### 作业 3：动物园案例

定义父类 `Animal`，包含：

- 名字
- 年龄
- `eat()` 方法
- `speak()` 方法

定义子类：

- `Dog`
- `Cat`
- `Bird`

要求每个子类重写 `speak()` 方法。

