'''
讲解init方法
'''

class Student:
    # 当使用Student类创建对象的时候，会调用下面的方法
    def __init__(self,name, age,score):
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
        # 为对象添加score属性
        self.score = score

    # 定义对象的方法自我介绍，不接受实参
    def introduce(self):
        # 将来对象会自动传递给self, 比如s1.introduce, self就是s1
        print(f'您好,我是{self.name}, 我今年{self.age}岁了')
    # 展示学分
    def show_score(self):
        print(f'{self.name}的成绩是{self.score}')
    # 更新学分
    def update_score(self,new_score):
        self.score = new_score
        print(f'{self.name}的成绩已经更新为{self.score}分')
'''
创建一个学生对象, 会自动调用__init__,
1. __init__需要三个参数，第一个self实际是指向了对象的地址，这个对象在调用__init__之前
通过__new__方法就已经创建好，提前在堆空间创建好的， 解释器会自动将这个对象的地址赋值给self
不需要开发者传参
2. name, age需要通过Student('zack',18)传递，将实参传递给name,age两个形参
'''
# 用s1存储Student生成的对象
s1 = Student('zack',18,95)
# 通过对象.属性的方式访问属性
print(s1.name)
print(s1.age)
# 调用introduce方法, s1会自动传递给self
s1.introduce()
# 这个是打印类的方法的
#print(Student.__dict__)
# 展示学分
s1.show_score()
# 更新学分
s1.update_score(100)
s1.show_score()
