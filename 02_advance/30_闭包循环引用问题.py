'''
演示闭包的循环引用问题
'''

# 错误案例
funcs = []
# i是局部变量
for i in range(3):
    def inner():
        # 因为内部函数要是用变量i，所以触发闭包机制
        # 将i打包成cell，放入inner.__clouser__,
        # 内部函数访问i其实是获取i的地址中的数据
        print(i)
    # 将函数存储到列表中
    funcs.append(inner)

# 全部输出2,而非0，1，2
funcs[0]()
funcs[1]()
funcs[2]()

# 正确案例
funcs = []
# i是局部变量
for i in range(3):
    def inner(num=i):
        print(num)
    funcs.append(inner)

funcs[0]()
funcs[1]()
funcs[2]()

