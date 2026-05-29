'''
演示元组拆包过程
'''

tuple1 = ('炸鸡',True,25.5)
# 拆包
name, is_flag, price = tuple1
print(f"{name},{is_flag},{price}")

# 自动拆包
a, b = (10,20)
print(f"{a},{b}")

# 两个变量交换
c1 = '游戏手柄'
c2 = 'Switch'
# temp 存储c1之前的数值
temp = c1
# c1存储c2的值
c1 = c2
# c2存储temp,也就是c1之前的值
c2 = temp
print(f"{c1},{c2}")

# 快速交换
# c2,c1 = c1,c2 也是可以交换的
c2 , c1 = (c1,c2)
print(f"{c1},{c2}")