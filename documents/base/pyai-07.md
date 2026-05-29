---
title: Python函数
date: 2026-04-16 22:21:23
tags: [python,AI]
categories: [python,AI]
---

## 内容概览

今日内容:

* 1- 【掌握】容器的拆包
* 2- 【知道】推导式
* 3- 【掌握】Python的函数:
  * 3.1 基本定义与使用
  * 3.2 变量的作用域
  * 3.3 函数中各个参数设置
  * 3.4 lambda函数(匿名函数)



## 容器拆包

### 什么是拆包？

简单来说就是把一个元组中的数据一个一个拆解出来的过程，就称之为叫做拆包操作。

### 基本语法

```python
tuple1 = (10, 20)
# 拆包
num1, num2 = tuple1

以上代码可以简写为
num1, num2 = (10, 20)

还可以进一步简写
num1, num2 = 10, 20

```

### 拆包典型案例

**定义一个容器（元组）**

```
tuple1 = ("炸鸡", True, 25.5)
```

**将元组中每个元素分别赋值给三个变量**

```
name, is_flag, price = tuple1

print(f"{name},{is_flag},{price}")
```

输出：`炸鸡,True,25.5`

**其他自动拆包方式**

```
a, b = (10, 20)
print(f"{a},{b}")

a, b = 10, 20
print(f"{a},{b}")
```

**两变量值交换**

**初始化两个变量**

```
c1 = '游戏手柄'
c2 = 'Switch'
```

**直接交换（利用自动拆包）**

```
c1 = '游戏手柄'
c2 = 'Switch'

c2, c1 = c1, c2

print(c1)
print(c2)
```

输出：

```
Switch
游戏手柄
```

**使用临时变量（不用自动拆包）**

```
c1 = '游戏手柄'
c2 = 'Switch'

tmp = c1
c1 = c2
c2 = tmp

print(c1)
print(c2)
```

输出：

```
Switch
游戏手柄
```

------

**总结**：自动拆包本质上就是把容器的每个元素"打散"分别赋值给对应位置的变量，变量数量必须和元素数量一致。变量交换时直接 `a, b = b, a` 即可，比传统临时变量法简洁得多 

## 推导式

### 什么是推导式

​		推导式comprehensions（又称解析式），是Python的一种独有特性。推导式是可以从一个数据序列构建另一个新的数据序列（一个有规律的列表或控制一个有规律列表）的结构体。 共有三种推导：`列表推导式`、`集合推导式`、`字典推导式`。

### 为什么需要推导式

案例：创建一个0-9的列表

while循环：

```python
# 初始化计数器
i = 0
list1 = []
# 编写循环条件
while i <= 9:
    list1.append(i)
 	# 更新计数器
    i += 1
print(list1)
```

for循环：

```python
list1 = []
# 编写for循环
for i in range(0, 10):
    list1.append(i)
print(list1)
```

思考：我们能不能把以上代码简化为一行代码搞定这个程序呢？

答：可以，使用推导式



什么时候可以使用推导式:  

当需要遍历一个容器, 然后遍历后需要返回一个新容器的场景

### 列表推导式

基本语法：

```python
变量名 = [表达式 for 变量 in 列表]
变量名 = [表达式 for 变量 in 列表 if 条件]
变量名 = [表达式 for 变量 in 列表 for 变量 in 列表]
```

案例：定义0-9之间的列表

```python
list1 = []
for i in range(10):
    list1.append(i)
print(list1)
```

列表推导式

```python
# 推导式演示:
"""
    格式:
        变量名 = [表达式 for 变量 in 列表]
        变量名 = [表达式 for 变量 in 列表 if 条件]
        变量名 = [表达式 for 变量 in 列表 for 变量 in 列表]

"""

# 案例1：定义0-9之间的列表
# 非推导式方式
my_list = []

for i in range(0, 10):
    my_list.append(i)

print(my_list)

# 推导式:
my_list = [i for i in range(0, 10)]
print(my_list)

# 案例2: 给定一个列表, 将该列表内容依次添加到另一个集合中, 实现去重效果 得到一个集合:  {7,9,5,4,6}
my_list2 = [7, 9, 5, 4, 5, 7, 6]

# 非推导方式:
my_set1 = set()

for e in my_list2:
    my_set1.add(e)

print(my_set1)

# 推导式方式:
my_set2 = {e for e in my_list2}
print(my_set2)

```

执行原理：[i for i in range(10)]

```bash
列表推导式先运行表达式右边的内容：

当第一次遍历时：i = 0，其得到变量i的结果后，会放入最左侧的变量i中，这个时候列表中就是[0]
当第二次遍历时：i = 1，其得到变量i的结果后，会追加最左侧的变量i中，这个时候列表中就是[0, 1]
...
当最后一次遍历时：i = 9，其得到变量i的结果后，会追加最左侧的变量i中，这个时候列表中就是[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 列表推导式 + if条件判断

在使用列表推导式时候，我们除了可以使用for循环，其实我们还可以在其遍历的过程中，引入if条件判断。

```python
变量 = [表达式 for 临时变量 in 序列 if 条件判断]

等价于

for 临时变量 in 序列:
    if 条件判断
```

案例：生成0-9之间的偶数（i%2  0）序列

```python
#  推导式 含  IF 操作
# 格式: 变量 = [表达式 for 临时变量 in 序列 if 条件判断]

# 需求: 案例：生成0-9之间的偶数（i%2  0）序列
# 非推导式方式
my_list3 = []
for e in range(0, 10):
    if e % 2 == 0:
        my_list3.append(e)


print(my_list3)

# 推导式:
my_list4 = [e for e in range(0, 10) if e % 2 == 0]

print(my_list4)

# 需求2: 生成 0~9的序列, 然后将 > 5的数据 存储到一个新的列表中
# 推导式
my_list5 = [ e for e in range(0,10) if e > 5 ]
print(my_list5)
```

### for循环嵌套列表推导式

```python
for 临时变量 in range(n):
    for 临时变量 in range(n):
```

基本语法：

```python
变量 = [表达式 for 临时变量 in 序列 for 临时变量 in 序列]
```

**🪑 座位表生成案例**

**需求：生成教室座位坐标列表**

假设一个 3行 × 4列 的教室，生成所有座位的坐标：

```
座位布局：
    第0列  第1列  第2列  第3列
行0: (0,0)  (0,1)  (0,2)  (0,3)
行1: (1,0)  (1,1)  (1,2)  (1,3)
行2: (2,0)  (2,1)  (2,2)  (2,3)
```

------

**方法一：for循环嵌套**

```
seats = []

# 外层循环：遍历每一行
for row in range(3):
    # 内层循环：遍历每一列
    for col in range(4):
        seat = (row, col)
        seats.append(seat)

print(seats)
```

**输出：**

```
[(0, 0), (0, 1), (0, 2), (0, 3),
 (1, 0), (1, 1), (1, 2), (1, 3),
 (2, 0), (2, 1), (2, 2), (2, 3)]
```

------

**方法二：列表推导式**

```
# 推导式方式（更简洁）
seats = [(row, col) for row in range(3) for col in range(4)]

print(seats)
```

**输出：**

```
[(0, 0), (0, 1), (0, 2), (0, 3),
 (1, 0), (1, 1), (1, 2), (1, 3),
 (2, 0), (2, 1), (2, 2), (2, 3)]
```

------

**对比记忆 🧠**

| 对比项       | for循环嵌套 | 列表推导式   |
| ------------ | ----------- | ------------ |
| **代码行数** | 多行        | 一行搞定     |
| **可读性**   | 逻辑清晰    | 简洁但稍难读 |
| **执行效率** | 稍慢        | 更快         |
| **适用场景** | 复杂逻辑    | 简单转换     |

**推导式本质就是：**

```
# 外层 for 在前，内层 for 在后
[表达式 for 外层变量 in 外层范围 for 内层变量 in 内层范围]
```

------

更多练习 🎯

**题目1：** 生成 2×3 的棋盘坐标（从 (1,1) 开始）

```
# 推导式
chess = [(i, j) for i in range(1, 3) for j in range(1, 4)]
# 结果: [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3)]
```

**题目2：** 生成所有 (0-9, 0-9) 的坐标对（排除对角线 i==j）

```
# 推导式
coords = [(i, j) for i in range(10) for j in range(10) if i != j]
```



###  推导式案例

案例一：使用列表推导式生成平方数集合

例如, 用户输入10, 表示要生成 1~10的每一个数字的平方的集合

~~~python
# 推导式案例: 案例一：使用列表推导式生成平方数集合
# 例如, 用户输入10, 表示要生成 1~10的每一个数字的2平方的集合
# 1- 让用户输入一个正整数
n = int(input("请输入一个正整数:"))

# 2- 遍历 从 1 ~ N
# 2.1 初始化一个空列表
my_list7 = []
for j in range(1,n+1):
    # 2.2 计算 2的平方 将结果写入列表
    my_list7.append(j ** 2)

print(my_list7)

# 推导式 如何解决
my_list8 = [ j ** 2 for j in range(1,n+1)]
print(my_list8)
~~~



## Python中函数的作用与使用步骤

###  为什么需要函数

在Python实际开发中，我们使用函数的目的只有一个“让我们的代码可以被重复使用”

函数的作用有两个：

① 代码重用（代码重复使用）

② 模块化编程（模块化编程的核心就是函数，一般是把一个系统分解为若干个功能，每个功能就是一个函数）

> 在编程领域，编程可以分为两大类：① 模块化编程 ② 面向对象编程

###  什么是函数

所谓的函数就是一个被命名的、独立的、完成特定功能的代码段（一段连续的代码），并可能给调用它的程序一个返回值。

​	

被命名的：在Python中，函数大多数是有名函数（普通函数）。当然Python中也存在没有名字的函数叫做匿名函数。

独立的、完成特定功能的代码段：在实际项目开发中，定义函数前一定要先思考一下，这个函数是为了完成某个操作或某个功能而定义的。（函数的功能一定要专一）

返回值：很多函数在执行完毕后，会通过return关键字返回一个结果给调用它的位置。

###  函数的定义

基本语法：

```python
def 函数名称(参数1, 参数2, ...):
    函数体
    ...
    [return 返回值]


注意: 语法中的中括号表示的可选的意思
```



在Python中，函数和变量一样，都是先定义后使用。

```python
# 定义函数
def 函数名称([参数1, 参数2, ...]):
    函数体
    ...
    [return 返回值]

# 调用函数
函数名称(参数1, 参数2, ...)
```

## 背包物品管理 — 带你一步步认识函数

------

### 1️⃣ 第一步：不用函数 — 重复代码写到手酸

```
# 场景：游戏角色背包里有 100 个空格
# 每次捡到道具，都要用掉一个空格

# 第一次捡到药水
inventory = 100
inventory -= 1
print(f"捡到1个道具，背包还剩 {inventory} 个空格")

# 第二次捡到武器
inventory -= 1
print(f"捡到1个道具，背包还剩 {inventory} 个空格")

# 第三次捡到宝石
inventory -= 1
print(f"捡到1个道具，背包还剩 {inventory} 个空格")

# 第四次捡到装备
inventory -= 1
print(f"捡到1个道具，背包还剩 {inventory} 个空格")
```

**问题：** 每次捡道具都要写一模一样的 3 行代码，太繁琐了！💀

------

### 2️⃣ 第二步：封装成函数 — 代码复用

```
# 定义一个函数：捡道具
def pick_item():
    """捡起一个道具，自动占用背包一个空格"""
    print("捡到1个道具！")

# 调用函数，不用重复写代码了
pick_item()      # 第1次捡道具
pick_item()      # 第2次捡道具
pick_item()      # 第3次捡道具
pick_item()      # 第4次捡道具
```

**输出：**

```
捡到1个道具！
捡到1个道具！
捡到1个道具！
捡到1个道具！
```

**好处：** 🎉 定义一次，随时调用！再也不用复制粘贴了！

------

### 3️⃣ 第三步：函数带参数 — 告诉函数具体捡什么

```
# 场景：捡到的东西不一样，打印的信息也要不一样
# 用参数来解决这个问题

def pick_item(item_name):
    """捡起一个道具

    参数:
        item_name: 道具名称
    """
    print(f"捡到了 【{item_name}】！")

# 调用时传入具体道具名
pick_item("生命药水")   # 捡到生命药水
pick_item("火焰剑")     # 捡到火焰剑
pick_item("蓝宝石")     # 捡到蓝宝石
pick_item("黄金头盔")   # 捡到黄金头盔
```

**输出：**

```
捡到了 【生命药水】！
捡到了 【火焰剑】！
捡到了 【蓝宝石】！
捡到了 【黄金头盔】！
```

**好处：** 🎯 一个函数，变出无数种用法！

------

### 4️⃣ 第四步：函数带返回值 — 告诉调用者结果

```python
# 场景：希望函数告诉调用者，捡道具到底成不成功
# 比如背包满了就捡不了

# 设定背包容量
bag_capacity = 100
current_count = 0

def pick_item(item_name):
    """捡起一个道具
    返回 True 表示成功，False 表示失败（背包满了）
    """
    global current_count  # 声明使用全局变量

    # 检查背包是否满了
    if current_count >= bag_capacity:
        return False  # 捡不了，返回失败

    current_count += 1
    print(f"捡到了 【{item_name}】！背包进度：{current_count}/{bag_capacity}")
    return True  # 捡到了，返回成功

# 调用并判断结果
result = pick_item("生命药水")
if result:
    print("✅ 捡道具成功！")
else:
    print("❌ 背包已满，无法捡取！")

result = pick_item("火焰剑")
if result:
    print("✅ 捡道具成功！")
else:
    print("❌ 背包已满，无法捡取！")
```

**输出：**

```bash
捡到了 【生命药水】！背包进度：1/100
✅ 捡道具成功！
捡到了 【火焰剑】！背包进度：2/100
✅ 捡道具成功！
```

------

### 📊 总结对比

| 阶段             | 代码特点           | 能做什么     |
| ---------------- | ------------------ | ------------ |
| **无函数**       | 重复代码多         | 基本功能     |
| **无参函数**     | 定义一次，调用多次 | 代码复用     |
| **带参函数**     | 传入不同数据       | 一函多用     |
| **带返回值函数** | 返回执行结果       | 反馈给调用者 |

### 聊聊return返回值

思考1：如果一个函数如些两个return (如下所示)，程序如何执行？

```python
def return_num():
    return 1
    return 2


result = return_num()
print(result)  # 1
```

答：只执行了第一个return，原因是因为return可以退出当前函数，导致return下方的代码不执行。



思考2：如果一个函数要有多个返回值，该如何书写代码？

答：在Python中，理论上一个函数只能返回一个结果。但是如果我们向让一个函数可以同时返回多个结果，我们可以使用`return 元组`的形式。

```python
def return_num():
    return 1, 2


result = return_num()
print(result)
print(type(result))  # <class 'tuple'>
```



思考3：封装一个函数，参数有两个num1，num2，求两个数的四则运算结果

四则运算：加、减、乘、除

```python
def size(num1, num2):
    jia = num1 + num2
    jian = num1 - num2
    cheng = num1 * num2
    chu = num1 / num2
    return jia, jian, cheng, chu


# 调用size方法
print(size(20, 5))
```

相关演示:

```python
# 需求: 请帮我定义一个函数: computer 计算器函数, 要求给这个函数传入 2个参数, 在函数的内部完成  + - 计算, 并且将 + -的二个结果返回

# 定义函数:
def computer(a, b):
    # 编写函数功能的核心位置
    jia = a + b
    jian = a - b

    # 将加和减结果一并返回
    return jia, jian
    # return [jia, jian]
    # return {jia, jian}
    # return {'jia':jia,'jian':jian}


# 调用函数
# res = computer(3,5)
i,j = computer(3,5)  # 利用自动拆包思想

print(f'加法结果:{i},减法的结果:{j}')

```

## 函数的嵌套及案例

###  什么是函数的嵌套

所谓函数嵌套调用指的是一个函数里面又调用了另外一个函数。

### 函数嵌套的基本语法

``` python
def funca():
    return 2
def funcb():
    return funca()

funcb()
```

## 扩展递归

``` python
# 1 利用递归实现阶乘运算
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
```

``` python
# 2 利用递归青蛙台阶
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
```



![](https://cdn.llfc.club/image-20260421143018872.png)

``` python
# 3 实现汉诺塔
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
```



## 变量的作用域

### 什么是变量的作用域

变量作用域指的是变量的作用范围（变量在哪里可用，在哪里不可用），主要分为两类：全局作用域与局部作用域。

其实作用域的划分比较简单，在函数内部定义范围就称之为局部作用域，在函数外部（全局）定义范围就是全局作用域

```python
# 全局作用域
def func():
    # 局部作用域
```

### 局部变量与全局变量

在Python中，定义在函数外部的变量就称之为全局变量；定义在函数内部变量就称之为局部变量。

```python
# 定义在函数外部的变量（全局变量）
num = 10
# 定义一个函数
def func():
    # 函数体代码
    # 定义在函数内部的变量（局部变量）
    num = 100
```



演示全局和局部的使用场景

```sql
# 演示: 全局和局部变量:
#  全局变量: 指的是定义在函数外部的变量称为全局变量
#  局部变量: 指的是定义在函数内部的变量称为局部变量
#  全局变量的作用范围: 是整个全局的范围内, 一旦定义后, 在当前这个文件的任意位置均可以使用该变量
#  局部变量的作用范围: 仅在当前这个函数的内部, 一旦出了这个函数, 该变量就相当于不存在

# 定义一个全局变量:
a = 100

# 定义一个函数
def fun1():
    # 定义一个局部变量:
    b = 200
    # 在函数内部使用全局变量
    print(f"函数内--输出a的值为:{a}")
    print(f"函数内--输出b的值为:{b}")


# 调用函数
fun1()

# 在函数外部使用全局变量
print(f"函数外输出a的值:{a}")
# print(f"函数外输出a的值:{b}")
```





###  变量作用域的作用范围

全局变量：在整个程序范围内都可以直接使用

```python
str1 = 'hello'
# 定义一个函数
def func():
    # 在函数内部调用全局变量str1
    print(f'在局部作用域中调用str1变量：{str1}')

# 直接调用全局变量str1
print(f'在全局作用域中调用str1变量：{str1}')
# 调用func函数
func()
```

局部变量：在函数的调用过程中，开始定义，函数运行过程中生效，函数执行完毕后，销毁

```python
# 定义一个函数
def func():
    # 在函数内部定义一个局部变量
    num = 10
    print(f'在局部作用域中调用num局部变量：{num}')

# 调用func函数
func()
# 在全局作用域中调用num局部变量
print(f'在全局作用域中调用num局部变量：{num}')
```

运行结果：

![image-20210313145728886](https://cdn.llfc.club/image-20210313145728886.png)

> 普及小知识：计算机的垃圾回收机制 garbage collection

### global关键字的应用场景

思考一个问题：我们能不能在局部作用域中对全局变量进行修改呢？

```python
'''
在Python中有两种类型的变量
1. 可变类型 list,dict,set,自定义的类型 ，尽管数据相同，但是占用不同的内存空间
2. 不可变类型 int, bool, str, double, tuple,相同的数据在内存中只存储1份数据
a = 1
b = 1
可以理解为a和b存储的都是1的地址
当a = 2 的时候，a指向的就是2的地址
'''
a = 1
b = 1
a = 2

list_a = [1,2,3]
list_b = [1,2,3]
list_a.append(4)
print(list_a)
print(list_b)

'''
因为Python中赋值和定义具有二义性
Python不同于C++， 
C++语法
int a = 100;  a = 200;
Python中
定义和赋值弄到一起
a = 100
a = 200
如果a = 200在函数内， a = 100在函数外
两个a 不是同一个a， 函数内的a = 200会被认为定义了一个新的变量a
'''

# 定义全局变量num = 10
num = 10
# 定义一个函数func
def func():
    # 尝试在函数内部修改全局变量,但是不会修改，只会重新定义一个num
    num = 20
    print(f"函数内num:{num}, id(num): {id(num)}")

# 调用函数func
func()
# 尝试访问全局变量num
print(f"函数外num:{num}, id(num): {id(num)}")
print('*'*20)
```

![image-20260421152252236](https://cdn.llfc.club/image-20260421152252236.png)



最终结果：弹出10，所以由运行结果可知，在函数体内部理论上是没有办法对全局变量进行修改的，所以一定要进行修改，必须使用`global`关键字。



```python
# 定义全局变量num = 10
num = 10
# 定义一个函数func
def func():
    # 尝试在局部作用域中修改全局变量
    global num
    num = 20

# 调用函数func
func()
# 尝试访问全局变量num
print(num)
```

> 记住：global关键字只是针对不可变数据类型的变量进行修改操作（数值、字符串、布尔类型、元组类型），可变类型可以不加global关键字。

![image-20260421150443357](https://cdn.llfc.club/image-20260421150443357.png)



![image-20260421150940765](https://cdn.llfc.club/image-20260421150940765.png)

![image-20260421153338719](https://cdn.llfc.club/image-20260421153338719.png)

```python
# 案例: 以卖票案例

# 1 定义一个票总量
ticket = 100


# 2- 定义一个卖票的程序(函数)
def sale_ticket():
    # 标记为全局变量: 主要是针对的是不可变的数据类型, 如果是可变的, 不需要添加global关键词
    # 不可变的数据类型: 数值 字符串 元组 布尔
    # 可变的数据类型:  列表 集合 字典
    global ticket

    # 执行一次, 需要让 票数 -1
    ticket -= 1  # 默认会认为这个变量是一个局部变量

    print(f"剩余票数为:{ticket}")


# 3- 调用卖票程序
sale_ticket()
sale_ticket()
sale_ticket()
sale_ticket()
```

可变数据类型, 不需要添加global

```python
# 结论: 如果变量的数据类型是可变的, 不需要添加global 就可以 对 全局变量进行修改

# 1- 定义一个全局变量: 类型为 字典
person = {"name":"张三","age":18}

# 2- 定义一个函数
def fun1():
    # 向字典中添加一个属性:
    person['address'] = "南京市"

    print(f"函数内打印全局变量:{person}")
    #print("修改全局变量的内容")


# 3- 调用函数
fun1()

# 4- 在全局范围内 打印全局变量
print(person)
```

```
如果函数内修改的是可变对象，不需要加global,(dict,set,list,自定义类型对象)
因为不可变对象有很多种修改方式，比如字典的插入，比如列表append, remove,都可以修改，
不会被当成变量定义，所以就不用写global了

如果修改的是不可变的变量，需要加global,(字符串,元组,数字,布尔类型)
因为不可变类型的变量做修改，只能通过赋值，而赋值会产生二义性
python中=（赋值操作），有两层意思，一个是定义变量，还有一个是修改变量
在函数内部，局部作用域使用=，优先理解为定义变量

内存原理:
不可变对象，数据在内存中保留1份
可变对象，数据在内存中可以相同，可以是不同地址
```



![image-20260323113054437](https://cdn.llfc.club/image-20260323113054437.png)

![image-20260323113458929](https://cdn.llfc.club/image-20260323113458929.png)

![image-20260323114053389](https://cdn.llfc.club/image-20260323114053389.png)

![image-20260323114327460](https://cdn.llfc.club/image-20260323114327460.png)

![image-20260323120821143](https://cdn.llfc.club/image-20260323120821143.png)

作用域说明完整源码

``` python
'''
局部作用域和全局作用域
'''
'''
局部作用域: 函数内部作用域就是局部作用域
全局作用域: 在函数外部的作用域就是全局作用域
局部变量: 在函数内部定义的变量就是局部变量，可见范围只在自己定义的作用域内，
在哪个函数内定义，就在哪个函数内可见，不可被外部的全局作用域使用
全局变量: 在函数外部定义的变量就是全局变量，可以被程序的所有部分使用
'''
# 全局变量
num1 = 2000
def hello():
    # 局部变量
    num2 = 300
    print('hello world')
# 全局变量
num3 = 400
def sum(num1,num2):
    # num1和num2都是局部变量，num4
    num4 = num1 + num2
    return num4

# 全局变量
str1 = 'hello'
def func():
    # 局部变量
    str2 = 'heima'
    print(f'在局部作用域内使用全局变量str1: {str1}')
    print(f'在局部作用域内使用局部变量str2: {str2}')

func()
# 在全局作用域内无法使用局部变量
#print(f'在全局作用域内使用局部变量str2: {str2}')

# 如果局部变量和全局变量同名了，就会出现定义局部变量和全局变量冲突的问题
# 如果想要在函数内修改外部局部变量，用global声明
# 全局变量
name = 'Lisi'
def change_name():
    # 局部变量
    name = 'zs'
    print(f'局部变量name: {name}')
change_name()
print(f'全局变量name: {name}')

# 使用global关键字
def change_name2():
    # 声明全局变量
    global name
    # 修改全局变量，将lisi改为zs
    name = 'zs'
    print(f'函数内name: {name}')
change_name2()
print(f'全局变量name: {name}')

# 全局变量
name = 'Lisi'
# 使用形参name
def change_name3(name):
    # name是形参，局部变量
    # 修改全局变量，将lisi改为zs
    name = 'zs'
    print(f'函数内name: {name}')
# name 为实参，为全局变量
change_name3(name)
print(f'全局变量name: {name}')

'''
如果函数内修改的是可变对象，不需要加global,(dict,set,list,自定义类型对象)
因为可变对象有很多种修改方式，比如字典的插入，比如列表append, remove,都可以修改，
不会被当成变量定义，所以就不用写global了

如果修改的是不可变的变量，需要加global,(字符串,元组,数字,布尔类型)
因为不可变类型的变量做修改，只能通过赋值，而赋值会产生二义性
python中=（赋值操作），有两层意思，一个是定义变量，还有一个是修改变量
在函数内部，局部作用域使用=，优先理解为定义变量

内存原理:
不可变对象，数据在内存中保留1份
可变对象，数据在内存中可以相同，可以是不同地址
'''
# 这是可变类型的全局变量
person = {'name':'zs','age':18}
print(f'全局person地址: {id(person)}')
def func1():
    # = 被当作定义，所以内部person是新定义的局部变量
    person = {'name':'zs','age':18}
    print(f'函数内person地址: {id(person)}')

#func1()

def func2():
    person['address'] = 'beijing'
    print(f'函数内person地址: {id(person)}')
func2()

```



##  函数的参数进阶

###  函数的参数

在函数定义与调用时，我们可以根据自己的需求来实现参数的传递。在Python中，函数的参数一共有两种形式：

① 形参 ② 实参

形参：在函数定义时，所编写的参数就称之为形式参数

实参：在函数调用时，所传递的参数就称之为实际参数

```python
def greet(name):  # name就是在函数greet定义时，所编写的参数（形参）
    return name + '，您好'

# 调用函数
name = '老王'
greet(name)  # 在函数调用时，所传递的参数就是实际参数
```

> 注意：虽然我们在函数传递时，喜欢使用相同的名称作为参数名称。但是两者的作用范围是不同的。name = '老王'，代表实参。其是一个全局变量，而greet(name)函数中的name实际是在函数定义时才声明的变量，所以其实一个局部变量。

###  函数的参数类型(调用)

####  ☆ 位置参数

理论上，在函数定义时，我们可以为其定义多个参数。但是在函数调用时，我们也应该传递多个参数，正常情况，其要一一对应。

```python
def user_info(name, age, address):
    print(f'我的名字{name}，今年{age}岁了，家里住在{address}')
    
# 调用函数
user_info('Tom', 23, '美国纽约')
```

> 注意事项：位置参数强调的是参数传递的位置必须一一对应，不能颠倒

#### ☆ 关键词参数（Python特有）

函数调用，通过“键=值”形式加以指定。可以让函数更加清晰、容易使用，同时也清除了参数的顺序需求。

```python
def user_info(name, age, address):
    print(f'我的名字{name}，今年{age}岁了，家里住在{address}')
    
# 调用函数（使用关键词参数）
user_info(name='Tom', age=23, address='美国纽约')
```

#### ☆ 函数定义时缺省参数（参数默认值）

​		缺省参数也叫默认参数，用于定义函数，为参数提供默认值，调用函数时可不传该默认参数的值（注意：所有位置参数必须出现在默认参数前，包括函数定义和调用）。

```python
def user_info(name, age, gender='男'):
    print(f'我的名字{name}，今年{age}岁了，我的性别为{gender}')


user_info('李林', 25)
user_info('振华', 28)
user_info('婉儿', 18, '女')
```

> 谨记：我们在定义缺省参数时，一定要把其写在参数列表的最后侧



#### 相关的演示

```python
# 定义一个函数, 该函数需要传入三个参数
def fun1(name,age,address):
    print(f"姓名:{name},年龄:{age},地址:{address}")


# 如何调用呢?
# 位置传参方式: 要求调用函数的时候, 传递的参数顺序 要和 函数的形参的顺序保持一致
fun1("张三",20,"南京市")

# 关键词传参: 在传递参数的时候, 可以指定给谁传递  对顺序就没有要求
fun1(age=18,name="李四",address="北京市")

# 默认值传参: 指的是在定义这个函数的时候, 可以给某些参数赋一个默认值, 然后在调用该函数就可以不需要传递参数了
# 注意: 有默认值的形参 必须放置到整个参数列表的最后面
def fun2(name,address='南京市',age=18):
    print(f"姓名:{name},年龄:{age},地址:{address}")

# 调用操作: 如果不需要修改默认值, 那么在调用的时候也不需要传递, 如果需要修改 那么就正常传递即可
fun2(name="王五")
fun2(name="赵六",address="北京市")


注意: 如果函数中某个参数没有默认值, 那么在调用的时候, 必须传递 否则会直接报错

```







###  不定长参数

​		不定长参数也叫可变参数。用于不确定调用的时候会传递多少个参数(不传参也可以)的场景。此时，可用包裹(packing)位置参数，或者包裹关键字参数，来进行参数传递，会显得非常方便。

#### ☆ 不定长元组（位置）参数

````python
def user_info(*args):
    # print(args)  # 元组类型数据，对传递参数有顺序要求
    print(f'我的名字{args[0]}，今年{args[1]}岁了，住在{args[2]}')

# 调用函数，传递参数
user_info('Tom', 23, '美国纽约')
````

#### ☆ 不定长字典（关键字）参数

```python
def user_info(**kwargs):
    # print(kwargs)  # 字典类型数据，对传递参数没有顺序要求，格式要求key = value值
    print(f'我的名字{kwargs["name"]}，今年{kwargs["age"]}岁了，住在{kwargs["address"]}')

# 调用函数，传递参数
user_info(name='Tom', address='美国纽约', age=23)
```

> kw = keyword + args

综上：无论是包裹位置传递还是包裹关键字传递，都是一个组包的过程。

Python组包：就是把多个数据组成元组或者字典的过程。



相关演示:

```python
# 演示不定长参数:
# 不定长元组（位置）参数
# 定义函数:
def fun1(*args):  # 这种 一个 * 不定长参数, 背后 是一个容器(序列) --> 元组
    # 获取每一个参数的内容
    print(type(args))
    for e in args:
        print(f"参数:{e}")


# 调用函数
fun1("张三", "李四", "王五", "赵六", "田七")


# 不定长字典(关键词)参数
def fun2(**kwargs):  # 这种 一个 ** 不定长参数, 背后 是一个容器(序列) --> 字典
    print(type(kwargs))
    # 遍历参数
    for key in kwargs:
        print(f"参数的key:{key}, 对应的值为:{kwargs[key]}")

# 调用函数: 必须使用关键词传参
fun2(name="张三", age=18, address="南京市")  # 在调用的时候, 创建了一个字典, 将 kv数据放置到了字典中

```





案例：Python中数据的传递案例

```python
def func(*args, **kwargs):
    print(args)
    print(kwargs)


# 定义一个元组（也可以是列表）
tuple1 = (10, 20, 30)
# 定义一个字典
dict1 = {'first': 40, 'second': 50, 'third': 60}
# 需求：把元组传递给*args参数，字典传递给**kwargs
# ① 如果想把元组传递给*args，必须在tuple1的前面加一个*号
# ② 如果想把字典传递给**kwargs，必须在dict1的前面加两个**号
func(*tuple1, **dict1)
```

##  lambda函数



###  普通函数与匿名函数

在Python中，函数是一个被命名的、独立的完成特定功能的一段代码，并可能给调用它的程序一个返回值。

所以在Python中，函数大多数是有名函数 => 普通函数。但是有些情况下，我们为了简化程序代码，也可以定义匿名函数 => lambda表达式

###  lambda表达式应用场景

如果一个函数有一个返回值，并且只有一句代码，可以使用 lambda简化。

###  lambda表达式基本语法

```python
变量 = lambda 函数参数:表达式（函数代码 + return返回值）
# 调用变量
变量()
```

### 编写lambda表达式

定义一个lambda表达式

```python
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

```

![image-20260427112431224](https://cdn.llfc.club/image-20260427112431224.png)

###  编写带参数的lambda表达式

编写一个函数求两个数的和

```python
def fn1(num1, num2):
    return num1 + num2

print(fn1(10, 20))
```

lambda表达式进行简化：

```python
'''
带参数的lambda表达式
计算num1和num2的加法结果
'''
# fn是lambda表达式的地址，也就是函数地址
fn = lambda num1,num2:num1+num2
# 函数调用
print(fn(1,2))
```

#### ☆ 带默认参数的lambda表达式

```python
# 有参数 参数带有默认值:
def fn2(num1, num2=30):
    return num1 + num2


print(fn2)
print(fn2(10))

# lambda 简化
'''
带默认值的参数
'''
fn2 = lambda num1, num2=20: num1-num2
# 打印函数的地址，也就是lambda表达式在堆区的地址
print(fn2)
# num2默认传递20
print(fn2(100))
```

#### ☆ 带if判断（三目运算符）的lambda表达式

```python
# 带 if判断（三目运算符）的lambda表达式
# 普通函数
def fn3(name: str):
    a = 0
    if name == "张三":
        a = 1
    else:
        a = 0
    return a

# 普通函数
def fn4(name: str):
    return 1 if name == "张三" else 0

print(fn4("李四"))

# 基于lambda方案实现
lambda name: 1 if name == '张三' else 0 
```

#### ☆ 列表数据+字典数据排序（重点）

lambda表达式经常配合泛型编程使用

不受限于数据结构

也不受限于实际参数

封装和调用解耦合

**知识点：列表.sort(key=排序的key)**

```python
print("------------------------------------")
# 在一个列表中, 放置了三个元素, 每一个元素又是一个字典
students = [
    {'name': 'Tom', 'age': 20},
    {'name': 'Rose', 'age': 19},
    {'name': 'Jack', 'age': 22}
]
print(students)
# 按name值升序排列

# 按name值降序排列

```

