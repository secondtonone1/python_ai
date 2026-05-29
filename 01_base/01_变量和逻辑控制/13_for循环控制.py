'''
演示for循环逻辑控制
'''
'''
for基本语法
for 临时变量 in 序列:
    循环体逻辑1
    循环体逻辑2
说明：
序列包括，字符串，字典，列表，元组，集合，序列本质上就是可以被遍历的对象，
序列本质上是一个可以被迭代的对象
后期我们可以自己定义可以被遍历的对象，包括迭代器和生成器
'''
'''
需求：通过for循环遍历字符串i love python
'''
str = 'i love python'
for char in str:
    # char是一个临时变量，用str中依次取出每一个字符赋值给char
    print(char)
print('for 循环结束了')

'''
要想打印不换行的内容，可以对print传参
'''
print('a',end='')
print('b')
print('c')

str = 'i love python'
for char in str:
    print(char,end='')
# 默认输出换行
print()
print('for循环结束了')