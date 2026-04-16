---
title: 字符串用法
date: 2026-04-08 21:26:39
tags: [python,AI]
categories: [python,AI]
---

## 【掌握】字符串定义和切片

###  字符串的定义

字符串是 Python 中最常用的数据类型。我们一般使用引号来创建字符串。创建字符串很简单，只要为变量分配一个值即可。

**案例1：使用单引号或双引号定义字符串变量**

```python
# 方式一: 使用 单引号 或者 双引号创建
student_name1 = '李明'
student_name2 = "李明"

# 思考: 如果在字符串里面也有单引号或者双引号怎么办呢?
# 解决方案一: 使用转义符 \
# msg = 'It\'s a wonderful day'
# 解决方案二:如果里面是单引号,那么外部就使用双引号,反之也可以
# msg = "It's a wonderful day"

# 如果字符串里面既有单引又有双引: 也可以针对跟外部引号一致的内容使用转义符
# msg = " He said \"It's great\" "
```

**案例2：使用3个引号定义字符串变量**

```python
# 创建方式二: 使用三个引号(引号可以是单引也可以双引)
# msg = """ He said "It's great" """
# msg = ''' He said "It's great" '''
# 三引号支持换行
msg = ''' 
        Python编程语言
        学习资料
        第一章内容
    '''

print(msg)
```

> 注意：三引号形式的字符串支持换行操作

**案例3：思考如何使用字符串定义"It's sunny"**

使用单引号情况

```python
weather = 'It's sunny'
```

运行结果：会出现语法错误

出现以上问题的主要原因在于，以上字符串的定义代码出现了(syntax)语法错误。单引号在字符串定义中必须成对出现，而且Python解析器在解析代码时，会自动认为第一个单引号和最近的一个单引号是一对！

如果一定要在单引号中在放入一个单引号，必须使用反斜杠进行转义。

```python
weather = 'It\'s sunny'
```

使用双引号情况

```python
weather = "It's sunny"
```

> 注：在Python中，如果存在多个引号，建议① 单引号放在双引号中 ② 双引号放在单引号中。

---

###  字符串在计算机底层的存储形式

在计算机中，Python中的字符串属于序列结构。所以其底层存储占用一段**连续的内存空间**。

```python
course = 'python'
```

结构原理图：

索引的最大值 = len(字符串) - 1

6个字符，则索引下标的最大值为6-1 = 5

```
+---+---+---+---+---+---+
| p | y | t | h | o | n |
+---+---+---+---+---+---+
  0   1   2   3   4   5
```

> 注意：索引下标从0开始。

###  聊聊索引下标

`索引下标`，就是编号。比如电影院座位号，座位号的作用：按照编号快速找到对应的座位。同理，下标的作用即是通过下标快速找到对应的数据。

举个例子：

```python
text = 'hello'
print(text[0])  # h
print(text[3])  # l
```

###  什么是字符串切片

所谓的切片是指对操作的对象截取其中一部分的操作。字符串、列表、元组都支持切片操作。

### 字符串切片基本语法

顾头不顾尾：

```python
序列名称[开始位置下标:结束位置下标:步长(步阶)]

# 三个参数都有默认值: 
#     开始位置默认值: 0
#     结束位置默认值: -1 (最后一个)
#     步长: 1

digits = '0123456789'
digits[0:3:1]  # 012 => range方法非常类似，步长：每次前进1步
digits[0:3:2]  # 02 => 每次前进2步
# 步长可以为负数，正数代表从左向右截取，负数代表从右向左截取
```

① 不包含结束位置下标对应的数据，正负整数均可；

② 步长是选取间隔，正负整数均可，正数从左向右，负数从右向左。默认步长为1。

还是有点陌生，没关系，给你举个栗子：

```python
digits = '0123456789'
```

字符串切片示意图：

```
索引（正索引）:  0    1   2   3   4   5   6   7   8   9
字符:           '0' '1' '2' '3' '4' '5' '6' '7' '8' '9'
索引（逆索引）: -10  -9  -8  -7  -6  -5  -4  -3  -2  -1
```

###  字符串切片案例

* **案例1：基础切片操作**

  ```python
  # 案例一:
  digits = '0123456789'
  
  # 1、从2到5开始切片，步长为1
  print(digits[2:5])     # 输出: 234
  
  # 2、只有结尾的字符串切片：代表从索引为0开始，截取到索引为5的位置（不包含索引为5的数据）
  print(digits[:5])      # 输出: 01234
  
  # 3、只有开头的字符串切片：代表从起始位置开始(例如 1)，一直截取到字符串的结尾
  print(digits[1:])      # 输出: 123456789
  
  # 4、获取或拷贝整个字符串
  print(digits[:])       # 输出: 0123456789
  
  # 5、调整步阶：类似求偶数
  print(digits[::2])     # 输出: 02468
  
  # 6、把步阶设置为负整数：类似字符串翻转
  print(digits[::-1])    # 输出: 9876543210
  
  # 7、起始位置与结束位置都是负数
  print(digits[-5:-1])   # 输出: 5678
  
  # 8、结束字符为负数，如截取012345678
  print(digits[:-1])     # 输出: 012345678
  ```

* **案例2：给定一个图片的名称为"photo.jpg"，代码实现获取这个图片的名称(photo)以及这个图片的后缀(.jpg)。**

  * 分析：

    * ① 建议先获取点号的位置（目前还未学习，只能一个一个数）
    * ② 从开头切片到点号位置，得到的就是文件的名称
    * ③ 从点号开始切片，一直到文件的结尾，则得到的就是文件的后缀

  * 代码

    ```python
    # 案例二: 给定一个图片的名称为"photo.jpg"，代码实现获取这个图片的名称(photo)以及这个图片的后缀(.jpg)。
    filename = "photo.jpg"
    
    # 方法一：已知点号位置在索引5
    name = filename[:5]      # photo
    suffix = filename[5:]    # .jpg
    
    print(f"文件名: {name}")
    print(f"后缀名: {suffix}")
    
    # 方法二：使用字符串方法(后续会学习)
    dot_index = filename.find('.')
    name = filename[:dot_index]
    suffix = filename[dot_index:]
    ```

---

## 【掌握】字符串的操作方法（内置）

###  字符串中的查找方法

所谓字符串查找方法即是查找子串在字符串中的位置或出现的次数。

基本语法：

```python
字符串.find(要查找的字符或者子串)
```

| **编号** | **函数** | **作用**                                                     |
| -------- | -------- | ------------------------------------------------------------ |
| 1        | find()   | 检测某个子串是否包含在这个字符串中，如果在返回这个子串开始的位置下标，否则则返回-1。 |
| 2        | index()  | 检测某个子串是否包含在这个字符串中，如果在返回这个子串开始的位置下标，否则则报异常。 |

### ☆ find()方法

作用：检测某个子串是否包含在这个字符串中，如果在返回这个子串开始的位置下标，否则则返回-1。

```python
# 定义一个字符串
message = 'welcome to Python programming, Python is great'

# 查找Python子串是否出现在字符串中
position = message.find('Python')
print(f"Python首次出现的位置: {position}")  # 输出: 11

# 在message中查找不存在的子串
position2 = message.find('Java')
print(f"Java出现的位置: {position2}")  # 输出: -1
```

**案例：使用input方法输入任意一个文件名称，求点号的索引下标**

```python
filename = input("请输入文件名: ")
dot_position = filename.find('.')
if dot_position != -1:
    print(f"点号的位置在索引: {dot_position}")
    print(f"文件名: {filename[:dot_position]}")
    print(f"扩展名: {filename[dot_position:]}")
else:
    print("该文件名中没有扩展名")
```

### ☆ index()方法

index()方法其功能与find()方法完全一致，唯一的区别在于当要查找的子串没有出现在字符串中时，find()方法返回-1，而index()方法则直接报错。

```python
fruits = 'apple, banana, orange, grape'

# 判断apple是否出现在字符串fruits中
position = fruits.index('apple')
print(f"apple的位置: {position}")  # 输出: 0

# 查找不存在的子串会报错
# position = fruits.index('mango')  # 这行会引发ValueError异常
```

---

###  字符串的修改方法

所谓修改字符串，指的就是通过函数（方法）的形式修改字符串中的数据。

| **编号** | **函数**  | **作用**             |
| -------- | --------- | -------------------- |
| 1        | replace() | 返回替换后的字符串   |
| 2        | split()   | 返回切割后的列表序列 |
| 3        | title()   | 所有单词首字母大写   |

#### ☆ replace()方法

基本语法：

```python
字符串.replace(要替换的内容, 替换后的内容, 替换的次数-可以省略)
```

**案例：编写一个字符串，然后把字符串中的Java替换为Python**

```python
text = 'I love Java programming and Java is powerful'

# 把字符串中所有Java字符替换为Python
new_text = text.replace('Java', 'Python')
print(new_text)  # 输出: I love Python programming and Python is powerful

# 把字符串中的第一个Java进行替换为Python
new_text2 = text.replace('Java', 'Python', 1)
print(new_text2)  # 输出: I love Python programming and Java is powerful

# 把and字符串替换为&
new_text3 = text.replace('and', '&')
print(new_text3)  # 输出: I love Java programming & Java is powerful
```

目前在工作中，replace主要用于实现关键字替换或过滤功能。例如：敏感词过滤、地名简写替换等。

#### ☆ split()方法

作用：对字符串进行切割操作，返回一个list()列表类型的数据

```python
# 示例：按照逗号分隔日期
date_str = '2024-03-15'
date_parts = date_str.split('-')
print(date_parts)  # 输出: ['2024', '03', '15']

# 示例：分割邮箱地址
email = 'user@example.com'
parts = email.split('@')
print(f"用户名: {parts[0]}")  # 输出: user
print(f"域名: {parts[1]}")    # 输出: example.com
```

#### ☆ join()方法

作用：和split()方法正好相反，其主要功能是把序列拼接为字符串

```python
字符串.join(数据序列)
```

**案例：把水果列表['apple', 'banana', 'orange']拼接成'apple-banana-orange'**

```python
fruit_list = ['apple', 'banana', 'orange']
result = '-'.join(fruit_list)
print(result)  # 输出: apple-banana-orange

# 其他示例
words = ['Hello', 'Python', 'World']
sentence = ' '.join(words)
print(sentence)  # 输出: Hello Python World
```

---

###  字符串案例

#### 案例需求

生成一个6位随机验证码，要求包含大写字母、小写字母和数字的组合。

示例:
```
生成的验证码: aB3xK9
生成的验证码: Q7mN2p
```

#### 实现思路

1. 定义包含所有可用字符的字符串（大写字母、小写字母、数字）
2. 使用切片和索引随机选取字符
3. 将选取的字符拼接成最终的验证码

#### 代码实现

```python
import random

def generate_code(length=6):
    """
    生成指定长度的随机验证码
    参数:
        length: 验证码长度，默认为6
    返回:
        生成的验证码字符串
    """
    # 定义所有可用字符
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    
    # 合并所有字符
    all_chars = uppercase + lowercase + digits
    
    # 生成验证码
    code = ''
    for i in range(length):
        # 随机选择一个索引位置
        random_index = random.randint(0, len(all_chars) - 1)
        # 通过索引获取字符并添加到验证码中
        code += all_chars[random_index]
    
    return code

# 测试：生成5个验证码
print("生成5个随机验证码：")
for i in range(5):
    print(f"验证码{i+1}: {generate_code()}")

# 生成不同长度的验证码
print("\n生成不同长度的验证码：")
print(f"4位验证码: {generate_code(4)}")
print(f"8位验证码: {generate_code(8)}")
```

**扩展练习：**

```python
# 练习1：确保验证码至少包含一个数字和一个字母
def generate_secure_code(length=6):
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    all_chars = uppercase + lowercase + digits
    
    while True:
        code = ''
        for i in range(length):
            random_index = random.randint(0, len(all_chars) - 1)
            code += all_chars[random_index]
        
        # 检查是否包含数字和字母
        has_letter = any(c in uppercase + lowercase for c in code)
        has_digit = any(c in digits for c in code)
        
        if has_letter and has_digit:
            return code

print("安全验证码:", generate_secure_code())

# 练习2：验证用户输入的验证码是否正确（不区分大小写）
def verify_code(user_input, correct_code):
    """验证验证码（不区分大小写）"""
    return user_input.lower() == correct_code.lower()

# 模拟验证码验证
real_code = "aB3xK9"
user_code = "AB3XK9"
if verify_code(user_code, real_code):
    print("验证码正确！")
else:
    print("验证码错误！")
```