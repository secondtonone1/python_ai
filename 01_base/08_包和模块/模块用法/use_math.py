'''
演示模块导入方法
'''
'''
# 导入模块
import my_math
# 使用my_math包的my_add
print(my_math.my_add(1,2))
'''

'''
# 导入my_math包，起别名
import my_math as mt
print(mt.my_add(1,2))
'''

# 导出my_math中所有的函数和变量
from my_math import *
# 导出my_math中的my_add函数
from my_math import my_add
print(my_add(1,2))


