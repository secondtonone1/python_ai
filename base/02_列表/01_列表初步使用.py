'''
列表初步使用
'''
'''
演示列表的定义
'''
fruits = ['orange','apple','mango']
print(fruits)
print(type(fruits))

# 列表可以存储不同类型的数据
my_list = ['apple',123,True]
print(my_list)
print(type(my_list))

# 获取列表中的某一个元素
print(fruits[0])
print(fruits[1])
print(fruits[2])
print(fruits[-1])

# 如何遍历列表
print('-----------------------------------')
# for循环
for name in fruits:
    print(name)
print('-----------------------------------')
# while循环
index = 0
while index < len(fruits):
    print(fruits[index])
    index += 1


