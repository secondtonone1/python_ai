'''
演示函数嵌套
'''

def func_a():
    return 1

# func_b内部调用func_a,将调用的结果返回给外边
def func_b():
    return func_a()

print(func_b())

'''
递归: 一个函数自己调用自己，就是递归
必要条件： 要有结束条件
'''
def func_c(num:int):
    '''
    通过递归实现求阶乘操作
    :param num:参数
    :return: int
    '''
    if num <= 1:
        return 1
    return num * func_c(num-1)


print(func_c(3))

'''
分治思想，分而治之，简称分治
将一个大问题，拆解为相似的小问题，逐个击破
'''
'''
需求：有一个小青蛙，每次可以跳1个台阶，或者跳2个台阶，总共10个台阶，问有多少种走法
思路：
1. 当仅有一个台阶，那么就是1中走法，fn(1) = 1
2. 当有两个台阶，那么有两种走法,f(2) = 2
3. 当有三个台阶， 那么有这些走法 f(3) = f(2) + f(1)
4. 如果有四级台阶， 那么走法为f(4) = f(3) + f(2)
5. 如果有n级台阶，那么走法为f(n) = f(n-1) + f(n-2)
'''
def fn_steps(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    return fn_steps(n-1) + fn_steps(n-2)

print(fn_steps(10))

'''
汉诺塔
移动n个盘子，从A--->C盘
思路：
将前n-1个盘子从A柱借助C柱移动到B柱
将第n个盘子从A柱移动到C柱
将前n-1个盘子从B柱借助A柱移动到C柱
'''

def hanuota(num, A,B,C):
    '''
    这是一个汉诺塔函数，表示将num个盘子，从A柱移动到C柱的流程
    :param num: 盘子个数
    :param A:  A柱子，起始柱子
    :param B:  B柱子，辅助柱子
    :param C:  C柱子，目的柱子
    :return: None
    '''
    if num == 1:
        print(f'将第{num}个盘子从{A}移动到{C}')
        return
    # 将num-1个盘子从A借助C移动到B
    hanuota(num-1, A,C,B)
    # 将第num个盘子，从A移动到C
    print(f'将第{num}个盘子从{A}移动到{C}')
    # 将num-1个盘子从B借助A移动到C
    hanuota(num-1,B,A,C)

hanuota(3,'A','B','C')
