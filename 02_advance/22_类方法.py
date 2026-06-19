'''
演示类方法
'''

class Student:
    # 类属性
    count = 0
    def __init__(self, name):
        self.name = name
        # 对类属性+1，统计计数
        Student.count += 1

    @classmethod
    def showcount(cls):
        #print(f'创建了{Student.count}个学生')
        print(f'创建了{cls.count}个学生')

s1 = Student('zack')
s2 = Student('ray')
# 类方法被所有对象共享，可以通过类名或者对象名方式访问
s1.showcount()
s2.showcount()
Student.showcount()