'''
演示变量的作用域
'''

#全局变量num1
num1 = 100

#定义函数
def func_read():
    # 访问全局变量
    print(f"num1 is {num1}")

'''
python中赋值操作可被解读成两种情况
num1 = 100
1. 被当作赋值，修改原变量的值
2. 被当作变量定义，定义一个新的变量
这就是python赋值的二义性
不像是C++
int num1 = 200; //这是定义
num1 = 500; //这是修改
'''

# 在局部作用域修改全局变量
def func_write():
    # 定义一个局部变量，解释器优先查看局部作用域内是否有num1，
    # 如果没有则将这个赋值理解为定义
    num1 = 200
    num2 = 500
    print(f'in func_write num1 is {num1}')

# 在局部作用域中修改全局变量
def func_change():
    # 声明num1为全局变量
    global num1
    # 修改num1的值为200
    num1 = 200
    print(f'in func_change num1 is {num1}')

if __name__ == '__main__':
    func_read()
    print('😭*20')
    func_write()
    # 打印全局变量
    print(f'outer func num1 is {num1}')
    # 在全局作用域中无法访问局部变量num2
    # print(f'num2 is {num2}')
    print(f'😭'*20)
    func_change()
    print(f'outer func num1 is {num1}')