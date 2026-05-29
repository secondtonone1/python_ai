'''
变量名 = 变量值
变量值:
1 数值(小数或者整数)
小数在计算机编程中叫做浮点数,类型为float(浮点型)
整数在计算机编程中就叫做整数，类型为int(整形)
2 字符串(由'或者"括起来的内容叫做字符串)
3 布尔值(True，False) 类型为bool(布尔类型)
'''
# name为变量名，存储字符串zack
name = 'zack'
# age为变量名 ，存储整数数据38
age = 38
# weight为变量名, 存储浮点数76.5
weight = 76.5
# print可以输出多个内容，中间用逗号分割
print(name, age, weight)

'''
变量名命名规则
1. 不能以数字开头
2. 名字只能由字母，数字，下划线构成
3. 严格区分大小写
4. 不要和关键字冲突
'''
# 名字只能由字母，数字，下划线构成
# name? = 'zack'
# 不能以数字开头
# 3_hello = 'zack'
# 不要和关键字冲突
# if age = 18

'''
判断变量类型:
1. type(变量名),返回变量对应的具体类型
2. isinstance(变量名,类型),判断变量名是否和类型匹配，如果匹配返回True,否则返回False
'''
age = 38
print(type(age))
print(isinstance(age,int))
weight = 76.5
print(type(weight))
print(isinstance(weight,int))
name = 'zack'
print(type(name))