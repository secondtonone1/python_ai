'''
演示range操作
'''

'''
range本质上返回一个可被迭代的对象(可以通过for循环遍历)
简单的理解为range会生成一个整数的序列
基本语法
range(stop)---> 默认从0开始，到stop结束，不包括stop，步长为1,range(0,stop,1)-->[0,1,2,3....stop)
range(start,stop,step) ----> 从start开始，到stop结束，不包括stop，步长为step
step可以为负数，表示从大到小，step也可以是大于1的数字
'''

'''
需求使用for循环与range操作，使用for循环遍历4次，输出4个hello world
思路：
1. 可以考虑生成一个数字序列[0,1,2,3]--->range(0,4,1)--->range(4)
2. 使用for循环遍历   for 临时变量 in range(4):
3. 循环体内打印hello world即可
'''
for i in range(4):
    print('hello world')

'''
使用for循环，计算从1到50之间所有奇数的和
思路:
1. 生成一个1到50的序列, range(1,51,1)--->range(1,51)
2. 通过for循环从序列range(1,51)中依次取出数据放入临时变量
3. 对临时变量进行判断，如果为奇数，才进行累加求和，
求和可以放入外部定义的一个变量
'''
# 定义奇数的和
odd_sum = 0
for i in range(1,51):
    #print(i)
    # 判断为奇数
    if i % 2 != 0:
        odd_sum += i
print(f'1到50的奇数的和为{odd_sum}')

print('#'*50)
# 演示step为-1，表示从大到小
# 因为step是负数，所以数据序列必须从大到小，因为下面的range开始比结束大
# 所以不满足逻辑要求，生成空序列，python不会报错
for i in range(1,51, -1):
    print(i)
print('#'*50)
for i in range(51,0, -1):
    print(i)
print('#'*50)

# step可以为大于1的数
for i in range(0,10,2):
    print(i)
print('#'*50)