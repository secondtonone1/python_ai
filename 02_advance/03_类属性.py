'''
演示类属性
'''

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
# 应用，利用类属性统计创建的实例个数
class Person:
    # 统计创建了多少实例
    count = 0
    def __init__(self, name, age):
        self.name = name
        self.age = age
        # 对类属性进行修改，自增
        Person.count += 1

zs = Person('zs',25)
lisi = Person('lisi',25)
print(f'总共创建了{Person.count}个实例')