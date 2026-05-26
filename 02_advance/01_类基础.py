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

