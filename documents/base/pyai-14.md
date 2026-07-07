---
title: 装饰器和闭包
date: 2026-06-25 17:37:27
tags: [python,AI]
categories: [python,AI]
---

# 一、全局变量和局部变量

## 作用域

作用域就是代码生效的范围

在Python代码中，作用域分为两种情况：全局作用域 与 局部作用域

## 变量的作用域

全局作用域：在函数外面的作用域就是全局作用域

局部作用域：在函数内的作用域就是局部作用域

在全局作用域定义的变量 =\> 全局变量

在局部作用域定义的变量 =\> 局部变量

## 全局变量与局部变量的访问范围

### 局部作用域可以访问全局变量，且可通过global修改全局变量

在函数局部作用域中，默认可以读取全局变量；如果需要修改全局变量，需要使用 **global** 关键字声明。

>python中赋值操作可被解读成两种情况
>num1 = 100
>1. 被当作赋值，修改原变量的值
>2. 被当作变量定义，定义一个新的变量
>这就是python赋值的二义性
>不像是C++
>int num1 = 200; //这是定义
>num1 = 500; //这是修改

```python
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

```

### 全局作用域无法访问局部变量

函数内部定义的局部变量，仅能在函数局部作用域中使用，函数执行结束后会被回收，全局作用域无法读取。

```python
'''
演示全局无法访问局部变量
'''
def func():
    # 局部变量，仅函数内部有效
    num2 = 200
    print(f'函数内部访问局部变量num2 = {num2}')

func()
# 下方代码会报错 NameError: name 'num2' is not defined
# print(num2)

```

###  全局无法访问局部变量的底层原因

主要原因在于，在Python的底层存在“垃圾回收机制”，用于自动回收闲置内存空间，提升程序运行效率。函数执行结束后，函数内部定义的所有局部变量都会被系统自动回收释放，因此全局作用域无法访问已销毁的局部变量。

## Python变量查找LEGB规则（核心底层）

Python访问变量时，会严格按照固定层级逐层查找，找不到则抛出 **NameError**，也是闭包、变量作用域的底层原理：

- **L（Local）局部作用域**：当前函数内部变量

- **E（Enclosing）嵌套作用域**：外层嵌套函数的局部变量（闭包专属层级）

- **G（Global）全局作用域**：文件顶层定义的全局变量

- **B（Built\-in）内置作用域**：Python系统内置变量/函数（print、len等）

## global 与 nonlocal 关键字对比

| 关键字   | 作用范围              | 使用场景                                   |
| -------- | --------------------- | ------------------------------------------ |
| global   | 全局作用域（G层）     | 函数内部修改全局变量，无法操作嵌套函数变量 |
| nonlocal | 嵌套局部作用域（E层） | 闭包内部修改外层函数变量，无法操作全局变量 |

# 二、闭包

## 闭包定义

在**函数嵌套**的前提下，内部函数**使用了外部函数的变量**，并且外部函数**返回了内部函数**，这个引用外层变量的内部函数即为闭包。

## 闭包的构成条件（三步走）

1. 有嵌套：存在外层函数和内层函数的嵌套结构

2. 有引用：内层函数调用外层函数的局部变量/参数

3. 有返回：外层函数将内层函数作为返回值返回

## 基础闭包代码演示

```python
'''
闭包基础演示
条件:
1. 函数嵌套
2. 内部函数使用外部函数的变量
3. 外部函数返回内部函数
'''
# 定义外部函数
def outer_func(num1):
    # 定义内部函数
    def inner_func(num2):
        # 使用外部函数的变量num1
        num = num1+num2
        print('现在的值:', num)
    # 返回内部函数
    return inner_func

# 调用外部函数, 返回内层函数的内存地址
# fn 等价于 inner_func，常驻内存
fn = outer_func(10)
# 调用闭包函数，等价于 inner_func(1)
fn(1)

```

![image-20260626105417850](https://cdn.llfc.club/image-20260626105417850.png)

## 闭包核心作用

正常函数执行结束后，内部局部变量会被垃圾回收机制销毁。而**闭包可以常驻外层函数的局部变量**，实现全局作用域中间接访问、持续使用已结束函数的局部变量。

## 闭包注意事项

由于闭包会持续引用外部函数的变量，导致外层变量无法被垃圾回收，会长期占用内存，大量使用闭包可能造成内存资源消耗。（内存逃逸）

## 闭包中修改外层变量（nonlocal关键字）

###  变量赋值二义性问题

Python中 `=` 赋值存在二义性：左侧变量会被优先判定为**本地局部变量**。如果闭包内层函数直接修改外层变量，会因找不到本地变量报错，此时需要 **nonlocal** 声明外层变量。

###  标准修改案例

```python
'''
演示nonlocal关键字的用法
'''

def outer_func():
    num1 = 10
    def inner_func():
        # 赋值优先被当作定义
        num1 = 20
        print(f'inner func num1 is {num1}')
    inner_func()
    print(f'outer func num1 is {num1}')
    return inner_func

def outer_func2():
    num1 = 10
    def inner_func():
        # 可以声明nonlocal，表示不是本地变量
        # 通知解释器去外层查找num1
        nonlocal num1
        # 修改的是outer_func2内部的局部变量num1
        num1 = 20
        print(f'inner func num1 is {num1}')
    inner_func()
    print(f'outer func num1 is {num1}')
    return inner_func

def outer_func3():
    num1 = 10
    def inner_func():
        # 使用外层函数的num1
        nonlocal num1
        num1 = num1 + 20
        print(f'inner func num1 is {num1}')

    inner_func()
    print(f'outer func num1 is {num1}')
    return inner_func


if __name__ == '__main__':
    outer_func()
    print('😀'*20)
    outer_func2()
    print('😀'*50)
    outer_func3()
```

###  特殊规则：可变对象无需nonlocal

如果外层变量是列表、字典等**可变对象**，仅修改容器内部元素、不对变量整体重新赋值时，无需使用 nonlocal 关键字。

```python
def outer():
    # 可变对象列表
    data = [1, 2, 3]
    def inner():
        # 仅修改列表内部元素，无整体赋值
        data.append(4)
        print(data)
    return inner

f = outer()
f()

```

## 闭包进阶知识点

###  自由变量

闭包中被内层函数引用的外层变量，称为**自由变量**。闭包会将自由变量保存在函数内置属性中，阻止垃圾回收。可通过内置属性查看：

```python
def outer():
    num = 100
    def inner():
        print(num)
    return inner

fn = outer()
# 查看自由变量名称
print(fn.__code__.co_freevars)
# 查看闭包保存的变量对象
print(fn.__closure__)

```

###  闭包经典陷阱：循环延迟绑定

循环批量生成闭包时，所有闭包会共用同一个外层变量，最终取值均为循环最后值，是高频面试坑点。

```python
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


```

![image-20260626114057223](https://cdn.llfc.club/image-20260626114057223.png)

![image-20260626114821655](https://cdn.llfc.club/image-20260626114821655.png)

###  闭包内存释放

闭包会造成内存常驻，无需使用时可手动解除引用，释放内存：`fn = None`

## 闭包综合案例

```python
'''
闭包累加案例：持续保留上次计算结果
'''
def func():
    # 外层变量，常驻内存
    result = 0
    def inner_func(num):
        # 引用外层变量并修改
        nonlocal result
        result = result + num
        return result
    # 返回闭包
    return inner_func

# 绑定闭包函数
g = func()
print(g(1))  # 0+1=1
print(g(2))  # 1+2=3
print(g(3))  # 3+3=6

```

# 三、装饰器入门与进阶

## 装饰器定义

装饰器是**特殊的闭包函数**，核心作用：**不修改原有函数源代码、不改变原有函数调用方式**，动态为函数新增额外功能。

装饰器必备条件（闭包三条件）：函数嵌套、内层引用外层参数（原函数）、外层返回内层函数。

## 基础装饰器（无语法糖）

```python
'''
演示装饰器用法
'''

'''
装饰器实现步骤:
1. 函数嵌套
2. 内层函数引用外层函数的参数，这里引用外层函数的形参，也就是原函数
3. 在外层函数内返回内层函数
4. 在内层函数中装饰原函数
'''


# 原函数
def play_game():
    print('打一局蛋仔派对...')

# 定义装饰器(外层函数接受原函数)
def check(fn):
    # 封装一个内层函数，该内层函数使用外层函数的参数
    # 装饰器就是内层函数使用外层函数的形参(fn函数,原函数)
    def inner():
        # 新增装饰功能
        print('登录验证')
        # 执行原函数的功能
        fn()
    return inner

# 等号左侧的play_game相当于inner函数
play_game = check(play_game)
play_game()
```

![image-20260702084516505](https://cdn.llfc.club/image-20260702084516505.png)

##  语法糖装饰器（推荐写法）

`@装饰器名` 是Python提供的语法糖，等价于手动赋值装饰，代码更简洁。

```python
'''
演示装饰器语法糖
'''

# 定义装饰器
def check(fn):
    def inner():
        print('验证登录')
        fn()
    return inner

# 相当于 comment = check(comment)

@check
def comment():
    print('发表评论')

comment()

```

## 各类场景装饰器实战

### 装饰有参数无返回值函数

```python
def print_info(func):
    def inner(a,b):
        print(f'正在努力计算中。。。。')
        func(a,b)
    return inner

@print_info
def get_sum(x,y):
    z = x+y
    print(f'两数之和为:{z}')

get_sum(1,2)

```

###  装饰有返回值函数

```python
def print_info(func):
    def inner():
        print(f'友好提示，正在努力计算中...')
        res = func()
        print(f'计算成功...')
        # 返回原函数调用结果
        return res
    return inner



@print_info
def get_sum():
    return 20 + 38


print(get_sum())

```

###  装饰有参数有返回值函数

```python
def print_info(func):
    # 内层参数与原函数保持一致
    def inner(a,b):
        print(f'正在努力计算中...')
        res = func(a,b)
        print(f'计算成功！！！')
        return res
    return inner

@print_info
def get_sum(x,y):
    z = x + y
    return z

print(get_sum(1,2))

```

###  装饰可变参数函数（\*args、\*\*kwargs）

**装饰可变位置参数的函数**

``` python

def decorator1(func):
    # 内层函数接受可变位置参数
    def inner(*args):
        print('努力计算中...')
        # args本质上是一个元组，
        # *args就是将元组中的数据拆包，拆成1个1个的位置参数
        result = func(*args)
        print('计算成功')
        return result
    return inner

@decorator1
def sum(a,b):
    return a+b

print(sum(1,2))

@decorator1
def sum2(a,b, c,d):
    return a+b+c+d

print(sum2(1,2,3,4))
# 调用失败，inner接受的是可变位置参数
# sum(a = 1, b = 2)

```



![image-20260702091752408](https://cdn.llfc.club/image-20260702091752408.png)



**装饰可变关键字参数的函数**

``` python

def decorator(func):
    # 内层函数接受可变关键字参数
    def inner(**kwargs):
        print('努力计算中...')
        # kwargs本质上是一个字典
        # **kwargs就是将字典中的数据拆包，拆成1个1个的key=value的形式
        print(f'kwargs = {kwargs}')
        result = func(**kwargs)
        print('计算成功')
        return result
    return inner

@decorator
def sum(a,b):
    return a+b
# 因为inner无法接受可变位置参数
# print(sum(1,2))

# inner可以接受可变关键字参数
print(sum(a = 1, b = 2))

```



![image-20260702093200634](https://cdn.llfc.club/image-20260702093200634.png)



通过可变参数适配**任意参数数量、任意参数类型**的原函数，是通用装饰器核心写法。

```python
'''
这是通用装饰器
'''

def decorator(func):
    def inner(*args, **kwargs):
        print(f'努力计算中...')
        print(f'args = {args}')
        print(f'kwargs = {kwargs}')
        # 元组，字典拆包
        # args相当于元组，*args相当于将元组拆解成可变位置参数
        # kwargs相当于字典，**kwargs相当于将字典拆解为可变关键字参数
        return func(*args, **kwargs)
    return inner

@decorator
def sum(*args,**kwargs):
    '''
    需求，对元组中的所有数据求和，对字典中的value求和
    :param args: args是可变位置参数打包后的元组
    :param kwargs: kwargs是可变关键字参数打包后的字典
    :return:
    '''
    sum = 0
    # 遍历元组求和
    for arg in args:
        sum += arg

    # 遍历字典的value求和
    for value in kwargs.values():
        sum += value
    return sum

print(sum(1,2,3, a = 4, b=5, c = 6))
# 打印sum函数的名字
print(f'sum.__name__ = {sum.__name__}')
# 打印函数的文档
print(f'sum.__doc__ = {sum.__doc__}')

```

![image-20260702094758275](https://cdn.llfc.club/image-20260702094758275.png)

###  多个装饰器装饰同一个函数

执行规则：**从上到下装饰包裹，从下到上执行逻辑**

```python
'''
多装饰器执行：先登录校验、再权限校验，最后执行业务
'''

def check_login(func):
    def inner():
        print('✔ 检测用户是否登录（SSO验证）')
        func()
    return inner

def check_permission(func):
    def inner():
        print('✔ 检查用户是否具备报销权限（财务系统权限）')
        func()
    return inner

# 多装饰器叠加
@check_login
@check_permission
def submit_reimbursement():
    print('📄 提交报销申请（上传发票+填写金额）')

submit_reimbursement()
```

![image-20260707095118051](https://cdn.llfc.club/image-20260707095118051.png)

### 带参数装饰器（三层函数结构）

带参装饰器为**三层函数结构**：外层接收自定义参数、中层接收原函数、内层执行业务逻辑。

```python
'''
带参数装饰器：根据操作类型记录不同日志（公司审计系统）
'''

def audit(action_type):
    # 中层：接收原函数
    def decorator(func):
        # 内层：执行业务
        def inner(user, amount):
            if action_type == 'recharge':
                print('--[审计] 用户正在进行充值操作')
            elif action_type == 'withdraw':
                print('--[审计] 用户正在进行提现操作')
            elif action_type == 'transfer':
                print('--[审计] 用户正在进行转账操作')

            result = func(user, amount)
            return result
        return inner
    return decorator


@audit('recharge')
def wallet(user, amount):
    print(f'{user} 账户变动金额：{amount}')
    return f'操作成功：{amount}'


print(wallet('Alice', 100))
```

![image-20260707101031179](https://cdn.llfc.club/image-20260707101031179.png)

##  装饰器高阶进阶

### 解决装饰器函数元信息丢失

函数被装饰后，默认会丢失原函数的函数名、文档注释等元信息，可通过 **functools\.wraps** 修复，所有正式项目必须使用。

```python
import functools

def timer(func):
    # 保留原函数元信息
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@timer
def calc():
    """数值计算函数"""
    pass

# 正常输出原函数信息
print(calc.__name__)
print(calc.__doc__)

```

**自定义func_wrapper**

``` python

# 自定义一个带参数的装饰器，模仿functools.wraps这个函数
def func_wrapper(func):
    # func是函数接受的参数，原函数
    def decorator(fn):
        # fn相当于另一个开发者实现的装饰器中的inner函数
        # 不是下面的inner函数
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)
        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        return inner
    return decorator


def timer(func):
    @func_wrapper(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@timer
def calc():
    '''数值计算函数'''
    pass

# 打印函数名字
print(calc.__name__)
print(calc.__doc__)
```



![image-20260707102533236](https://cdn.llfc.club/image-20260707102533236.png)



![image-20260707104123529](https://cdn.llfc.club/image-20260707104123529.png)

###  常用实战通用装饰器

#### 耗时统计装饰器

```python
import time
import functools

def cost_time(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"函数{func.__name__}执行耗时：{end-start:.4f}秒")
        return result
    return inner

@cost_time
def heavy_task():
    s = 0
    for i in range(1000000):
        s += i
    return s

heavy_task()

```

#### 异常捕获装饰器

```python
import functools

def catch_error(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"函数执行异常：{e}")
            return None
    return inner

@catch_error
def div(a, b):
    return a / b

print(div(10, 0))

```

### 类装饰器拓展

通过类实现装饰器，依靠 `__call__` 魔法方法让类实例可被调用，适用于复杂装饰场景。

```python
import functools

class LogDecorator:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)  # 正确保留函数元信息

    def __call__(self, *args, **kwargs):
        print("类装饰器：函数开始执行")
        result = self.func(*args, **kwargs)
        print("类装饰器：函数执行结束")
        return result


@LogDecorator
def test():
    print("业务代码运行")


test()

```

# 四、课后实战练习

## 需求

实现三层嵌套的带参数装饰器 `log_action`，接收字符串参数 `action_type`（取值：`查询`、`录入`、`移除`、`更新`）。

功能要求：

1. 函数执行前打印：`正在执行【xxx】数据操作`

2. 兼容任意参数、任意返回值的函数（使用 `*args、**kwargs`）

3. 保留原函数返回结果，使用 `functools.wraps` 修复函数元信息

4. 严格使用三层函数结构：外层收参数、中层收函数、内层执行业务

## 完整实现代码

```python
import functools

# 带参数通用日志装饰器
def log_action(action_type):
    # 第二层：接收被装饰函数
    def decorator(func):
        @functools.wraps(func)
        # 第三层：通用执行逻辑
        def inner(*args, **kwargs):
            print(f"正在执行【{action_type}】数据操作")
            # 执行原函数并接收返回值
            ret = func(*args, **kwargs)
            # 返还原函数结果
            return ret
        return inner
    return decorator

# 测试1：数据查询功能
@log_action("查询")
def query_data(table_name):
    print(f"正在读取数据表：{table_name}")
    return "数据读取完成"

# 测试2：数据录入功能
@log_action("录入")
def insert_data(table_name, count):
    print(f"向{table_name}插入{count}条记录")
    return "录入完成"

# 测试3：数据移除功能
@log_action("移除")
def remove_data(row_id):
    print(f"删除行号：{row_id}的数据")
    return "删除完成"

# 调用测试
print(query_data("sales_data"))
print("-"*25)
print(insert_data("user_info", 35))
print("-"*25)
print(remove_data(608))

```

## 预期输出

```bash
正在执行【查询】数据操作
正在读取数据表：sales_data
数据读取完成
-------------------------
正在执行【录入】数据操作
向user_info插入35条记录
录入完成
-------------------------
正在执行【移除】数据操作
删除行号：608的数据
删除完成

```

