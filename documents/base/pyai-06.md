---
title: 常见数据结构
date: 2026-04-11 21:33:24
tags: [python,AI]
categories: [python,AI]
---

# 1. 列表及其应用场景

## 为什么需要列表

思考：有一个人的姓名(LiLei)怎么书写存储程序？

答：变量。

思考：如果一个班级50位学生，每个人的姓名都要存储，应该如何书写程序？声明50个变量吗？

答：No，我们使用列表就可以了， 列表一次可以存储多个数据。

> 在Python中，我们把这种数据类型称之为列表。但是在其他的编程语言中，如Java、PHP、Go等等中其被称之为数组。

## 列表的定义

```python
列表序列名称 = [列表中的元素1, 列表中的元素2, 列表中的元素3, ...]

注意: 列表是可变的
```

案例演示：定义一个列表，用于保存橙子、葡萄以及芒果

```python
fruit_list = ['orange', 'grape', 'mango']
# list列表类型支持直接打印
print(fruit_list)
# 打印列表的数据类型
print(type(fruit_list))  # <class 'list'>
```

> 注意：列表可以一次存储多个数据且可以为不同的数据类型

![image-20260411215004239](https://cdn.llfc.club/image-20260411215004239.png)

相关操作:

```python
# 演示: 如何定义列表
# 格式: 变量名称 = [元素1,元素2,元素3......]
# 需求: 构建一个列表, 保存 小明 小红 小刚 小丽 四个名字
name_list = ['小明','小红','小刚','小丽']
print(name_list)

# 如何获取列表中某一个元素呢? 与 字符串 一致
print(name_list[0])
print(name_list[1])
print(name_list[2])

# 如何遍历列表呢?
print("-----------------")
# for循环
for name in name_list:
    print(name)

# while循环
print("-----------------")
# 计数器
i = 0

while i < len(name_list):
    print(name_list[i])

    # 更新计数器
    i += 1
```

##  列表的相关操作

列表的作用是一次性存储多个数据，程序员可以对这些数据进行的操作有：

增、删、改、查。

### ☆ 查操作

列表在计算机中的底层存储形式，列表和字符串一样，在计算机内存中都占用一段连续的内存地址，我们向访问列表中的每个元素，都可以通过"索引下标"的方式进行获取。

如果我们想获取列表中的某个元素，非常简单，直接使用索引下标：

```python
fruit_list = ['orange', 'grape', 'mango']
# 获取列表中的grape
print(fruit_list[1])
```

查操作的相关方法：

| 编号 | 函数    | 作用                                                         |
| ---- | ------- | ------------------------------------------------------------ |
| 1    | index() | 指定数据所在位置的下标                                       |
| 2    | count() | 统计指定数据在当前列表中出现的次数                           |
| 3    | in      | 判断指定数据在某个列表序列，如果在返回True，否则返回False    |
| 4    | not in  | 判断指定数据不在某个列表序列，如果不在返回True，否则返回False |

### ☆ 增操作

| 编号 | 函数     | 作用                                                         |
| ---- | -------- | ------------------------------------------------------------ |
| 1    | append() | 增加指定数据到列表中                                         |
| 2    | extend() | 列表结尾追加数据，如果数据是一个序列，则将这个序列的数据逐一添加到列表 |
| 3    | insert() | 指定位置新增数据                                             |

### ☆ 删操作

| 编号 | 函数           | 作用                                             |
| ---- | -------------- | ------------------------------------------------ |
| 1    | del 列表[索引] | 删除列表中的某个元素                             |
| 2    | pop()          | 删除指定下标的数据(默认为最后一个)，并返回该数据 |
| 3    | remove()       | 移除列表中某个数据的第一个匹配项。               |

### ☆ 改操作

| 编号 | 函数                    | 作用                   |
| ---- | ----------------------- | ---------------------- |
| 1    | 列表[索引] = 修改后的值 | 修改列表中的某个元素   |
| 2    | reverse()               | 将数据序列进行倒叙排列 |
| 3    | sort()                  | 对列表序列进行排序     |

相关功能的演示:

```python
# 演示列表的API
name_list = ['小明', '小红', '小刚', '小丽', '小强', '小芳', '小亮', '小红']
# 查询相关方法:
# 1- index(): 查询指定数据所在位置的下标  如果不存在 直接报错
index = name_list.index("小丽")
print(index)  # 3

# 2- count(): 统计数据在当前列表中出现的次数
count = name_list.count("小红")
print(count)  # 2

# 3- in 和 not in 判断是否存在或不存在
bool = "小刚" in name_list
print(bool)
bool = "小刚" not in name_list
print(bool)

# 增加函数
# 1- append()  增加指定数据到列表中
# 如果 小宇 不在列表中, 请增加到列表中
if "小宇" not in name_list:
    # 能进来, 说明 小宇 不在, 如果不在 添加到列表中
    name_list.append("小宇")

print(name_list)

# 2- extend(): 将一个序列 追加到另一个序列中
# 2.1 先定义一个新的序列
name2_list = ['小浩', '小琪']

# 2.2 将新列表中数据 增加 到 原有列表中
name_list.extend(name2_list)

print(name_list)

# 3- insert() 在指定位置新增数据
name_list.insert(4, '小诺')

print(name_list)

# 删除操作
# 1- del 列表[索引]
del name_list[-1]

print(name_list)

# 2- pop() 删除指定下标的数据, 默认是删除最后一个 并且会返回删除的数据
element = name_list.pop()
print(element)
print(name_list)

element = name_list.pop(2)
print(element)
print(name_list)

# 3- remove() 移除列表中某个指定数据  如果不存在, 也不会报错 无效果
name_list.remove("小诺")
print(name_list)

# 修改操作
# 1-  修改某个索引的值
name_list[0] = '大明'
print(name_list)

# 2- reverse: 反转操作
name_list.reverse()

print(name_list)

# 3- 排序操作: reverse 设置 是否反转   True 反转(倒序)  False 不反转(正序)
num_list = [3, 7, 10, 56, 2, 9, 4, 5]
num_list.sort(reverse=True)
print(num_list)
```

## 列表的循环遍历

什么是循环遍历？答：循环遍历就是使用while或for循环对列表中的每个数据进行打印输出

while循环：

```python
star_list = ['西施', '王昭君', '杨玉环']
i = 0
while i < len(star_list):
    print(star_list[i])
    i += 1
```

for循环（个人比较推荐）：

```python
star_list = ['西施', '王昭君', '杨玉环']
for star in star_list:
    print(star)
```

## 列表的嵌套

列表的嵌套：列表中又有一个列表，我们把这种情况就称之为列表嵌套

> 在其他编程语言中，称之为叫做二维数组或多维数组

应用场景：要存储班级一、二、三  => 三个班级学生姓名，且每个班级的学生姓名在一个列表。

```python
classes = ['第一个班级','第二个班级','第三个班级']

一班：['小明', '小红']
二班：['小刚', '小丽']
三班：['小强', '小芳']

把班级和学员信息合并在一起，组成一个嵌套列表
students = [['小明', '小红'],['小刚', '小丽'],['小强', '小芳']]

students = [x,y,z]
students[0] == ['小明', '小红']
students[0][1]
```

问题：嵌套后的列表，我们应该如何访问呢？

```python
# 访问小红
print(students[0][1])
# 嵌套列表进行遍历，获取每个班级的学员信息
for i in students:
    print(i)
```

相关演示:

```python
# 演示 列表嵌套
# 说明: 容器内部嵌套容器方式
# 需求: 有 三个班级, 分别为 前端1班 前端2班  后端1班, 每个班级分别有5位学生
# 定义 班级列表
front1_class = ['小明','小红','小刚','小丽','小强']
front2_class = ['小芳','小亮','小宇','小浩','小琪']
back1_class = ['小诺','小泽','小琳','小航','小彤']

# 定义 学校列表, 学校列表中有三个班级
school_list = [front1_class,front2_class,back1_class]

# 以上内容 如果直接使用列表嵌套写法
school_list = [
    ['小明','小红','小刚','小丽','小强'],
    ['小芳','小亮','小宇','小浩','小琪'],
    ['小诺','小泽','小琳','小航','小彤']
]

# 如何 获取里面的数据呢?  比如 我想获取到 小浩
front2_class = school_list[1]
name = front2_class[3]
print(name)

# 可以简写
name = school_list[1][3]
print(name)

# 如何遍历打印每一个元素
for classes in school_list:
    for name in classes:
        print(name)
    print("-----------")
```

## 列表案例

### 案例需求（全新）

判断相邻元素的变化趋势

给定一个正整数数组，判断每一对相邻元素是“上升”“下降”还是“相等”，并输出结果列表

例如：
 输入: `[3, 5, 5, 2, 4]`
 输出: `['上升', '相等', '下降', '上升']`

------

### 实现思路

① 定义原始列表

② 创建一个空列表用于保存结果

③ 遍历相邻元素（当前值和下一个值）

④ 比较大小关系

- 当前 < 下一个 → 上升
- 当前 > 下一个 → 下降
- 相等 → 相等

⑤ 将结果添加到列表中

⑥ 输出结果

------

### 代码实现

```python
# 判断相邻元素变化趋势

num_list = [3, 5, 5, 2, 4]

result_list = []

i = 0

while i < len(num_list) - 1:
    if num_list[i] < num_list[i + 1]:
        result_list.append("上升")
    elif num_list[i] > num_list[i + 1]:
        result_list.append("下降")
    else:
        result_list.append("相等")

    i += 1

print(result_list)
```

------

## 巩固练习（全新）

找出列表中第一次出现的重复元素

给定一个列表，找到**第一个重复出现的元素**（只要出现第二次就算重复），并输出该元素

例如：
 输入: `[2, 3, 5, 3, 6, 5, 7]`
 输出: `3`

------

### 实现思路

① 创建一个空列表用于记录已经出现过的元素

② 遍历原始列表

③ 判断当前元素是否已经出现过

- 如果出现过 → 直接输出并结束
- 如果没有 → 添加到记录列表

④ 如果循环结束都没找到，说明没有重复

------

### 代码实现

```python
# 找第一个重复元素

num_list = [2, 3, 5, 3, 6, 5, 7]

seen_list = []

for e in num_list:
    if e in seen_list:
        print(e)
        break
    else:
        seen_list.append(e)
```



#  2.元组的定义与使用

## 为什么需要元组

思考：如果想要存储多个数据，但是这些数据是不能修改的数据，怎么做？

答：列表？列表可以一次性存储多个数据，但是列表中的数据允许更改。

```python
num_list = [20, 30, 40]
num_list[0] = 200
```

那这种情况下，我们想要存储多个数据且数据不允许更改，应该怎么办呢？

答：使用元组，元组可以存储多个数据且元组内的数据是不能修改的。

## 元组的定义

元组特点：定义元组使用小括号，且使用逗号隔开各个数据，数据可以是不同的数据类型。

基本语法：

```python
# 多个数据元组
tuple1 = (20, 30, 40)

# 单个数据元组
tuple2 = (20,)
```

> 注意：如果定义的元组只有一个数据，那么这个数据后面也要添加逗号，否则数据类型为唯一的这个数据的数据类型。

## 元组的相关操作方法

由于元组中的数据不允许直接修改，所以其操作方法大部分为查询方法。

| 编号 | 函数       | 作用                                                         |
| ---- | ---------- | ------------------------------------------------------------ |
| 1    | 元组[索引] | 根据索引下标查找元素                                         |
| 2    | index()    | 查找某个数据，如果数据存在返回对应的下标，否则报错，语法和列表、字符串的index方法相同 |
| 3    | count()    | 统计某个数据在当前元组出现的次数                             |
| 4    | len()      | 统计元组中数据的个数                                         |

```python
# 1- 如何定义元组
# 格式:
#   变量名称 = (元素1,元素2,元素3......)
#   变量名称 = (元素1,) : 如果元组中只有一个元素, 必须在后面添加一个逗号 否则编译器会自动转换为 数据的本身类型, 而不是元组类型
user_tuple = ('小明','小红','小刚',20,30,40,True,False)
print(user_tuple)
print(type(user_tuple))

tuple1 = ('小明',)
print(tuple1)
print(type(tuple1))

# 2- 如何使用元组
# 2.1 获取元组中某个元素:  与 列表 和 字符串 一致 都是通过索引的方式来获取
print(user_tuple[0])
print(user_tuple[1])
print(user_tuple[2])

# 2.2 遍历: 与 列表 一致
for e in user_tuple:
    print(e)

# 2.3 获取某个元素在元组中索引值: index
print(user_tuple.index(True))

# 2.4 获取某个元素在元组中出现了几次
print(user_tuple.count('小刚'))

# 2.5 获取元组长度
print(len(user_tuple))
```

## 元组案例

**案例需求1**

编写一个程序，计算嵌套元组中所有数字的总和。

例如：在嵌套元组 `((2,3,4),(3,5,7),(3,4,6))` 中，所有元素相加的结果为：

```
2+3+4+3+5+7+3+4+6 = 37
```

输出结果为：`37`

**实现思路**

① 定义一个嵌套元组

② 定义一个变量，用来保存总和，初始值为 0

③ 使用外层循环遍历每个子元组

④ 使用内层循环遍历子元组中的每个元素

⑤ 将每个元素依次累加到总和变量中

⑥ 输出最终结果



**代码实现**

```python
# 编写一个程序，计算嵌套元组中所有数字的总和
# 例如: ((2,3,4),(3,5,7),(3,4,6)) 的总和为 37

# 1- 初始化嵌套元组
tuple1 = (
    (2, 3, 4),
    (3, 5, 7),
    (3, 4, 6)
)

# 2- 定义变量，用于保存总和
total = 0

# 3- 遍历嵌套元组中的每个子元组
for tup_e in tuple1:
    # 4- 遍历子元组中的每个元素
    for e in tup_e:
        # 5- 累加每个元素
        total += e

# 6- 打印结果
print(total)
```

**案例需求2**

给定一个元组 `my_tuple`，里面包含 `2, 3, 4, 5, 6, 7, 8, 9, 10` 元素，要求找出其中所有大于 5 的数字，并放入一个新列表中。

输出结果为：`[6, 7, 8, 9, 10]`

------

**实现思路**

① 定义一个元组

② 创建一个空列表，用于保存大于 5 的数字

③ 遍历元组中的每个元素

④ 判断当前元素是否大于 5

⑤ 如果大于 5，就添加到结果列表中

⑥ 输出结果列表

------

**代码实现**

```
# 给定一个元组my_tuple，找出其中所有大于5的数字

my_tuple = (2, 3, 4, 5, 6, 7, 8, 9, 10)

# 1- 创建空列表，用于保存结果
result_list = []

# 2- 遍历元组中的每个元素
for e in my_tuple:
    # 3- 判断是否大于5
    if e > 5:
        # 4- 如果大于5，则添加到列表中
        result_list.append(e)

# 5- 打印结果
print(result_list)
```

------

这两个新案例和原来的区别比较明显：



# 3.【熟悉】集合的定义与使用

##  什么是集合

集合（set）是一个无序的不重复元素序列。

① 天生去重

② 无序

##  集合的定义

在Python中，我们可以使用一对花括号{}或者set()方法来定义集合，但是如果你定义的集合是一个空集合，则只能使用set()方法。

```python
# 1- 如何定义集合
# 格式:
#       格式一:  变量名称 = {元素1,元素2,元素3......}
#       格式二:  变量名称 = set()   空集合
# 特性: 无序 + 去重
# 定义一个有内容的集合
name_set = {'小明','小红','小刚','小明','小刚','小丽'}

print(name_set) #  去重 和 无序  发现每次都是不一样的 所以是无序的
print(type(name_set))
# 定义 空集合
# set2 = {}  # 此种定义方法 并不是定义空集合, 而是空的字典
empty_set = set()
print(type(empty_set))

# 获取数据: 遍历的方式
# for 循环
for name in name_set:
    print(name)
```

## 集合操作的相关方法（增删查）

### ☆ 集合的增操作

add()方法：向集合中增加一个元素（单一）

```python
name_set = {'小明','小红','小刚'}
name_set.add('小强')
print(name_set)
```

### ☆ 集合的删操作

remove()方法：删除集合中的指定数据，如果数据不存在则报错。

```python
name_set = {'小明','小红','小刚'}
name_set.remove('小红')
print(name_set)
```

### ☆ 集合中的查操作

① in ：判断某个元素是否在集合中，如果在，则返回True，否则返回False

② not in ：判断某个元素不在集合中，如果不在，则返回True，否则返回False

```python
name_set = {'小明','小红','小刚'}
print('小明' in name_set)  # True
print('小丽' not in name_set)  # True
```

③ 集合的遍历操作

```python
name_set = {'小明','小红','小刚'}
for name in name_set:
    print(name)
```

### 相关操作

```python
# 演示 集合的API
num_set = {3,4, True,'小明',False}
# 1- 添加数据的API: add
num_set.add("小红")
print(num_set)

# 2- 删除数据的API: remove  在删除的时候 如果在集合中没有该值 会直接报错
num_set.remove(False)

print(num_set)

# 3- 判断是否存在和不存在操作: in 和 not in
# 如果 小刚在集合中不存在, 请添加该元素
if '小刚' not in num_set:
    # 能进来, 说明 小刚 不在集合中
    num_set.add('小刚')

print(num_set)
```

## 集合案例

### 案例 1：找连续整数的断点

```python
"""
💡 题目：给定一个连续递增的整数列表，找出中断的位置。
例如：[1, 2, 3, 5, 6, 8] 中，3→5 断了，6→8 也断了。
"""
```

------

### 案例 2：找出数组中出现奇数次的数字

```python
'''
定义集合方式
方式1 空集合: empty_set = set()
方式2 包含元素的集合 my_set = {元素1, 元素}
'''

# 定义空集合
empty_set = set()
# 打印集合
print(empty_set)
print(type(empty_set))

# 定义空字典
empty_dict = {}
print(empty_dict)
print(type(empty_dict))

# 定义一个包含元素的集合
name_set = {'小明','小红','小刚','小明','小刚','小刚'}
print(name_set)
print(type(name_set))

# 遍历
for name in name_set:
    print(name)

# 增加元素
name_set = {'小明','小红','小刚'}
name_set.add('小强')
print(name_set)

# 删除元素
name_set.remove('小强')
print(name_set)

# 判断元素是否在集合中, in和not in
if '小明' in name_set:
    print('小明在集合中')
else:
    print('小明不在集合中')

# 判断元素不在集合中
if '小强' not in name_set:
    print('小强不在集合中')
else:
    print('小强在集合中')

"""
💡 题目：一个数组中除了两个数字只出现一次外，其他数字都出现两次。
       找出这两个只出现一次的数字。
输入: [4, 1, 2, 1, 2, 3, 5, 5]
输出: 3 和 4

思路：
1. 准备集合A和列表B，集合A用来存储出现的数字，集合B用来记录只出现过1次的数字
2. 将出现的数字和集合A判断，如果集合A中有数字，说明这个数字出现过，将数字从集合B
中删除。
如果A中没有这个数字，说明数字没出现过，将数字放入集合A和集合B
3. 最后循环结束，打印集合B，就是只出现一次的数字了
"""
num_list = [4, 1, 2, 1, 2, 3, 5, 5]
# 存储所有出现的数字
set_a = set()
# 存储只出现一次的数据
set_b = set()
for num in num_list:
    # num没有出现过
    if num not in set_a:
        set_a.add(num)
        set_b.add(num)
        continue
    # num出现过，则从set_b中移除该数字
    set_b.remove(num)

print('出现过1次的数字: ')
for num in set_b:
    print(num,end='\t')
print()
```

------

### 案例 3：统计每个数字出现的次数（去重后排序）

```python
"""
💡 题目：统计列表中每个数字出现的次数，并按数字大小排序输出。
输入: [4, 2, 2, 8, 3, 3, 1, 4, 3]
"""


```

------

### 案例 4：判断是否为连续序列

```python
"""
💡 题目：判断一个列表中的数字是否能组成连续序列。
例如：[4, 2, 3, 1] → True（可以重排成 [1,2,3,4]）
      [5, 3, 2, 6] → False（范围是 2~6，缺了 4）
"""

```



------

### 案例 5：找出数组中消失的数字（变形）

```python
"""
💡 题目：给你一个 1 到 n 的数组，但缺少了一些数字。
       找出所有 1~n 范围内消失的数字。
输入: [4, 3, 2, 7, 8, 2, 3, 1]  (n=8，但数组里缺了 5, 6)
"""
```



# 4.字典的定义与使用

## 为什么需要字典(dict)

思考1：比如我们要存储一个人的信息，姓名：ZhangSan，年龄：19周岁，性别：男，家庭住址：上海市浦东新区，如何快速存储。

```python
person = ['ZhangSan', 19, '男', '上海市浦东新区']
```

思考2：在日常生活中，姓名、年龄以及性别同属于一个人的基本特征。但是如果使用列表对其进行存储，则分散为3个元素，这显然不合逻辑。我们有没有办法，将其保存在同一个元素中，姓名、年龄以及性别都作为这个元素的3个属性。

答：使用Python中的字典

## Python中字典(dict)的概念

特点：

① 符号为大括号（花括号） =>  {}

② 数据为键值对形式出现   =>  {key:value}，key：键名，value：值，在同一个字典中，key必须是唯一（类似于索引下标）

③ 各个键值对之间用逗号隔开

> 在字典中，键名除了可以使用字符串的形式，还可以使用数值的形式来进行表示

定义：

```python
# 有数据字典
dict1 = {'name': 'ZhangSan', 'age': 19, 'gender': '男'}

# 空字典
dict2 = {}

dict3 = dict()
```

> 在Python代码中，字典中的key必须使用引号引起来

相关操作:

```python
# 1- 演示: 如何定义字典
# 格式:
#   格式1:  变量名称 = {key1:value1,key2:value2,key3:value3.....}
#   格式2:  变量名称 = {}  或者 变量名称 = dict()   空字典

# 构建一个有内容的字典
person = {'name': '小明', 'age': 19, 'address': "上海市浦东新区张江镇", 'sex': '男', 'hobby': '篮球、足球、游泳'}
print(person)
print(type(person))

# 构建空字典
dict1 = {}
dict2 = dict()
print(dict1)
print(type(dict1))
print(dict2)
print(type(dict2))

# 遍历操作
for key in person:
    print(key)
    print(person[key])
```

## 字典的增操作（重点）

基本语法：

```python
字典名称[key] = value
注：如果key存在则修改这个key对应的值；如果key不存在则新增此键值对。
```

## 字典的删操作

① del 字典名称[key]：删除指定元素

```python
person = {'name': '小明', 'age': 19}
del person['age']
print(person)
```

② clear()方法：清空字典中的所有key

```python
person = {'name': '小明', 'age': 19}
person.clear()
print(person)
```

## 字典的改操作

基本语法：

```python
字典名称[key] = value
注：如果key存在则修改这个key对应的值；如果key不存在则新增此键值对。
```

案例：定义一个字典，里面有name、age以及address，修改address这个key的value值

```python
person = {'name': '小明', 'age': 19, 'address': '上海市浦东新区'}
person['address'] = '上海市黄浦区'
print(person)
```

## 字典的查操作

① 查询方法：使用具体的某个key查询数据，如果未找到，则直接报错。

```python
字典序列[key]
```

② 字典的相关查询方法

| 编号 | 函数     | 作用                                |
| ---- | -------- | ----------------------------------- |
| 1    | keys()   | 以列表返回一个字典所有的键          |
| 2    | values() | 以列表返回字典中的所有值            |
| 3    | items()  | 以列表返回可遍历的(键, 值) 元组数据 |

案例1：提取person字典中的所有key

```python
person = {'name': '小明', 'age': 19, 'address': '上海市浦东新区'}
print(person.keys())
```

案例2：提取person字典中的所有value值

```python
person = {'name': '小明', 'age': 19, 'address': '上海市浦东新区'}
print(person.values())
```

案例3：使用items()方法提取数据

```python
person = {'name': '小明', 'age': 19, 'address': '上海市浦东新区'}
print(person.items())
```

相关的API操作:

```python
# 字典的相关API:
# 如何增加元素:
# 需求: 为person 字典增加一个 birthday 属性 值为 2005-08-20
person = {'name': '小明', 'age': 19, 'address': "上海市浦东新区张江镇", 'sex': '男', 'hobby': '篮球、足球、游泳'}
person["birthday"] = '2005-08-20'

print(person)

# 如何修改元素: 与添加一直, 如果key存在就是修改 如果不存在 就是添加
# 需求: 修改性别为 女
person['sex'] = "女"
print(person)

# 如何删除元素
# 删除某个元素:  根据key
del person['birthday']
print(person)
# 清空字典
# person.clear()
# print(person)

# 如何查询:
# 1- 根据 key 直接获取value: 如果key 不存在 直接报错
# 获取 address的值
print(person['address'])

# 2- 获取所有的keys
keys_list = person.keys()
print(keys_list)
# 3- 获取所有的value
values_list = person.values()
print(values_list)
# 4- 获取字典中每一个 kv对
# 快速返回变量: ctrl + alt + v
items = person.items()
print(items)

for kv in items:
    print(kv)
    print(f'{kv[0]},{kv[1]}')
```

## 字典案例

###  案例需求

给定一个字符串my_string，现在要求统计每个字符出现的次数: 形成结果: {'字符':出现次数,'字符2':次数}例如: 'abcdecf' ==> {'a':1,'b':1,'c':2,'d':1,'e':1,'f':1}

**实现思路**

①定义一个字符串

②初始化空字典，来存储对应字符和出现次数

③循环遍历字符串中每个字符

④如果字符串已经在字典中，计数加1，如果不在，初始化计数1:  字典['key'] += 1

⑤输出统计每个字符出现的次数

**代码实现**

```python
"""
    给定一个字符串my_string，现在要求统计每个字符出现的次数: 形成结果: {'字符':出现次数,'字符2':次数}

    例如: 'abcdecf' ==> {'a':1,'b':1,'c':2,'d':1,'e':1,'f':1}
"""
# 1- 创建一个字符串
my_string = 'abcdecf'

# 2- 遍历字符串, 获取每一个字符
# 2.1 初始化一个用于保存结果的空字典
my_dict = {}
for e in my_string:
    
    # 2.2 判断 当前遍历的这个元素 是否在 字典中存在呢?
    if e in my_dict.keys():
        # 说明 当前遍历的元素 在 字典中是存在的
        my_dict[e] += 1
    else:
        # 说明 当前遍历的元素 在 字典中是不存在的
        my_dict[e] = 1

print(my_dict)
```

### 巩固练习

需求: 编写一个程序将字符串转换为字典  例如:输入: '8=Eight 9=Nine 10=Ten'   输出: {'8': 'Eight', '9': 'Nine', '

