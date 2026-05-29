'''
演示lambda表达式用法
'''

'''
变量 = lambda 函数参数:表达式（函数代码 + return返回值）
# 调用变量
变量()
说明:
变量就是函数的地址，将来可以通过变量名调用函数
'''
def func(str):
    return 'hello '+ str

# fn是lambda表达式的地址，也就是函数地址
fn = lambda str: 'hello '+ str
# 打印函数调用结果
print(fn('zack'))

'''
带参数的lambda表达式
计算num1和num2的加法结果
'''
# fn是lambda表达式的地址，也就是函数地址
fn = lambda num1,num2:num1+num2
# 函数调用
print(fn(1,2))

'''
带默认值的参数
'''
fn2 = lambda num1, num2=20: num1-num2
# 打印函数的地址，也就是lambda表达式在堆区的地址
print(fn2)
# num2默认传递20
print(fn2(100))


def func_if(name):
    if name == 'zack':
        return 1
    else:
        return 2

print(func_if('zack'))
print(func_if('ray'))

def func_if_else(name):
    return 1 if name == 'zack' else 2

print(func_if_else('zack'))
print(func_if_else('ray'))

fn = lambda name:1 if name == 'zack' else 2
print(fn('zack'))
print(fn('ray'))

print("------------------------------------")
# 在一个列表中, 放置了三个元素, 每一个元素又是一个字典
students = [
    {'name': 'Tom', 'age': 20},
    {'name': 'Rose', 'age': 19},
    {'name': 'Jack', 'age': 22}
]
print(students)
# x就是列表中每一个元素，相当于一个字典，x['name']相当于获取key对应的value，分别为Tom,Rose,Jack
# 默认是升序
students.sort(key=lambda x:x['name'])
print(students)
# 按照年龄降序
students.sort(key=lambda x:x['age'], reverse=True)
print(students)