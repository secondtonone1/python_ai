'''
演示运算符
'''
a = 10
b = 3
# 加法运算
print(f'{a}+{b} = {a+b}')
# 乘法运算
print(f'{a}*{b} = {a*b}')
# 减法运算
print(f'{a}-{b} = {a-b}')
# 除法运算
print(f'{a}/{b} = {a/b}')
# 整除运算
print(f'{a}//{b} = {a//b}')
# 取余运算
print(f'{a}%{b} = {a%b}')
# 求幂运算
print(f'{a}**{b} = {a**b}')
# 复合运算赋值
a **= b
print(a)
a = 10
# 比较运算
print(f'a >= b = {a >= b}')
print(f'a <= b = {a <= b}')
print(f'a > b = {a > b}')
print(f'a < b = {a < b}')
print(f'a == b = {a == b}')
print(f'a != b = {a != b}')
# 逻辑运算
'''
and 逻辑与  x and y , 只有当x和y都为True的时候，x and y结果才为True
and短路效应: 当x为False，整个结果为False, 不再计算y
or 逻辑或 x or y , 当x或者y有一个为True，那么整个结果就为True
or短路效应: 当x为True，整个结果为True，y不参与运算
not x , 逻辑非，对x的结果取反, x为True， not x为False, x为False, not x为True
'''
print(a > b and a < b)
print(a > b or a < b)
print(not a > b)