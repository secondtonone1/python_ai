---
title: 变量和逻辑控制
date: 2026-03-27 17:22:25
tags: [python,AI]
categories: [python,AI]
---

# Python 变量和逻辑控制

## 课程目标

1. 了解 Python 语言的特点与应用场景，完成 Python 环境搭建

2. 熟练使用 PyCharm 开发工具，掌握基本操作流程

3. 精通 Python 基础语法（注释、变量、输入输出、数据类型转换、运算符、条件判断）

4. 能够运用基础语法完成简单的业务逻辑实现

##  Python 语言初识与环境搭建

### 为什么选择学习 Python

**（1）行业趋势**

Python 连续多年稳居 TIOBE 编程语言排行榜前三，在 PYPL 指数中更是长期占据榜首位置，成为全球最受欢迎的编程语言之一。无论是后端开发、数据分析、人工智能，还是自动化运维、爬虫开发，Python 都有广泛应用。

![image-20260327162617562](https://cdn.llfc.club/image-20260327162617562.png)

**（2）易学易用**

Python 仅包含 33 个关键字、7 种核心数据类型，语法规则简洁直观，接近自然语言。同样的功能实现，Python 代码量仅为 Java 的 1/5、C++ 的 1/10，极大降低了入门门槛。

**（3）生态丰富**

Python 拥有庞大的标准库和第三方库生态：

- 数据处理：NumPy、Pandas

- 可视化：Matplotlib、Seaborn

- 机器学习：Scikit-learn、TensorFlow

- Web 开发：Django、Flask

- 自动化：Selenium、PyAutoGUI

### Python 的发展历程

1989 年，荷兰程序员吉多・范・罗苏姆（Guido van Rossum，昵称 "龟叔"）为打发圣诞节假期，开始开发 Python 语言；1991 年，第一个 Python 解释器正式发布。Python 的命名源于龟叔喜爱的电视剧《Monty Python's Flying Circus》（蒙蒂・蟒蛇的飞行马戏团），也体现了 Python 轻松有趣的设计理念。

![Python’s creator shares his thoughts on other language | Guido van Rossum |  AIOC DEV'S NEWS | AIOC](https://i.ytimg.com/vi/_tUZwvgX6Yg/maxresdefault.jpg)

![人生苦短我用Python——模拟鼠标点击和键盘输入的操作 - 知乎](https://pic1.zhimg.com/v2-5f10578252c2fbdc8776cb52d8f48024_1440w.jpg?source=172ae18b)



>Life is short, use Python.

### Python 的优缺点分析

**优点**

- **简洁性**：代码可读性极高，专注解决问题而非语言本身

- **开源免费**：完全开源，可自由修改、分发，社区活跃

- **跨平台**：可在 Windows、Linux、MacOS 等主流系统无缝运行

- **全能型**：覆盖全栈开发、数据分析、人工智能等多个领域

- **胶水语言**：可轻松与 C/C++、Java、Go 等语言混合开发

**缺点**

- 执行效率较低（解释型语言特性），但可通过 C 扩展、JIT 编译（PyPy）优化

- 多线程受 GIL 限制，高并发场景需结合多进程或异步编程

### Python 解释器详解

Python 是高级编程语言，无法直接被计算机执行，需通过解释器将代码转换为机器语言（01 二进制）。常见解释器类型：

![image-20260327163308453](https://cdn.llfc.club/image-20260327163308453.png)

- **CPython**：官方默认版本，C 语言开发，应用最广泛

- **IPython**：交互式解释器，增强了 CPython 的交互体验

- **PyPy**：JIT 编译型解释器，执行效率远超 CPython

- **Jython/IronPython**：分别运行在 Java/.NET 平台的解释器

### Python 版本选择

生产环境建议选择稳定版（如 3.8/3.9/3.10/3.11），避免最新版本的兼容性问题。官方下载地址：https://www.python.org/downloads/

### 环境安装（Anaconda）

**（1）Anaconda/Miniconda/Conda 的区别**

- **Conda**：底层包管理和环境管理工具

- **Anaconda**："全家桶"，包含 Conda+Python+1500+数据科学库+图形化工具（体积约 500MB-1GB）

- **Miniconda**：迷你版，仅包含 Conda+Python+核心依赖（体积小，适合定制化环境）

**（2）安装步骤**

1 下载对应系统版本的 Anaconda（官网：https://www.anaconda.com/）开始安装

![1740668600059](https://cdn.llfc.club/1740668600059.png)

![1740668629646](https://cdn.llfc.club/1740668629646.png)

2 选择为所有人安装

![1740668667912](https://cdn.llfc.club/1740668667912.png)

3 运行安装包，建议安装到非 C 盘目录

![1740668753327](https://cdn.llfc.club/1740668753327.png)

4 勾选 "Add Anaconda to my PATH environment variable"（可选，方便命令行调用）

![1740668982175](https://cdn.llfc.club/1740668982175.png)

![1740670257930](https://cdn.llfc.club/1740670257930.png)

![1740670281760](https://cdn.llfc.club/1740670281760.png)

![1740670324881](https://cdn.llfc.club/1740670324881.png)

5 等待安装完成，验证：

![image-20260327164145237](https://cdn.llfc.club/image-20260327164145237.png)

```bash
conda -V  # 查看conda版本
python -V # 查看Python版本
```

**配置环境变量**

为了可以在cmd中使用Python, 建议去系统环境变量中配置

![image-20260327182317074](https://cdn.llfc.club/image-20260327182317074.png)

![image-20260327182327576](https://cdn.llfc.club/image-20260327182327576.png)

![image-20260327182338800](https://cdn.llfc.club/image-20260327182338800.png)



##  开发工具 PyCharm 使用指南

### PyCharm 的优势

作为 Python 专用 IDE，PyCharm 提供：

- 项目管理与代码组织
- 智能代码提示与补全
- 语法高亮与错误检测
- 断点调试与性能分析
- 内置版本控制（Git/SVN）
- 丰富的插件生态

![image-20260327164250190](https://cdn.llfc.club/image-20260327164250190.png)

###  PyCharm 版本选择

现在收费版(专业版)和免费版统一下载，免费版可以供个人使用，如果想升级收费版，需要购买激活码

### PyCharm 安装与配置

**（1）下载安装**

官网地址：https://www.jetbrains.com/pycharm/download/

安装步骤：

1. 下载对应系统版本的社区版

   ![image-20260327164503965](https://cdn.llfc.club/image-20260327164503965.png)

   双击exe安装

   ![image-20210306104505660](https://cdn.llfc.club/image-20210306104505660.png)

2. 选择非 C 盘安装路径

   ![image-20210306105046370](https://cdn.llfc.club/image-20210306105046370.png)

3. 勾选 "Create desktop shortcut" 和 ".py file association"

![image-20210306105223088](https://cdn.llfc.club/image-20210306105223088.png)

选择试用

![image-20260317101823647](https://cdn.llfc.club/image-20260317101823647.png)

**（2）核心操作**

**① 创建项目**

1. 打开 PyCharm，点击 "New Project"

2. 设置项目名称与路径（非 C 盘）

3. 选择 Python 解释器（Anaconda 或系统 Python）

   ![image-20260327165647384](https://cdn.llfc.club/image-20260327165647384.png)

4. 点击 "Create" 完成创建

ps:

如果找不到解释器，则打开目录输入解释器路径即可

![image-20260327170016782](https://cdn.llfc.club/image-20260327170016782.png)

**② 新建文件与编写代码**

1. 右键项目根目录 → New → Python File

2. 输入文件名（如 hello_world）

   ![image-20260327170302636](https://cdn.llfc.club/image-20260327170302636.png)

3. 编写入门代码：

```python
# 第一个Python程序
print("Hello Python!")
```

**③ 运行代码**

- 方式 1：右键代码编辑区 → Run '文件名'

  ![image-20260327170438953](https://cdn.llfc.club/image-20260327170438953.png)

- 方式 2：点击代码右上角的运行按钮

  ​	![image-20260327170403470](https://cdn.llfc.club/image-20260327170403470.png)

- 方式 3：快捷键 Shift+F10

**④ 个性化设置**

1. 主题设置：File → Settings → Appearance & Behavior → Appearance

   ![image-20260327170523501](https://cdn.llfc.club/image-20260327170523501.png)

2. 字体设置：File → Settings → Editor → Font（建议字号 14-16，字体 Consolas / 等线）

   ![image-20260327170604814](https://cdn.llfc.club/image-20260327170604814.png)

3. 解释器切换：File → Settings → Project: 项目名 → Python Interpreter

   ![image-20260327170707409](https://cdn.llfc.club/image-20260327170707409.png)

**⑤ 常用快捷键**

| 快捷键     | 功能                |
| ---------- | ------------------- |
| Ctrl+S     | 保存代码            |
| Ctrl+/     | 快速注释 / 取消注释 |
| Ctrl+D     | 复制当前行          |
| Ctrl+Z     | 撤销操作            |
| Ctrl+Y     | 恢复撤销            |
| Ctrl+Alt+L | 格式化代码          |
| Shift+F10  | 运行代码            |
| F9         | 断点调试            |

## Python 基础语法核心知识点

### 注释规范

注释是代码的说明文档，解释器不会执行注释内容，核心作用是提高代码可读性。

**（1）单行注释**

以`#`开头，注释单行内容：

```python
# 这是单行注释（推荐写在代码上方）
print("Hello World")  # 这是行尾注释（建议保留2个空格）
```

**（2）多行注释**

使用三引号（`"""`或`'''`）包裹多行内容：

```python
"""
这是多行注释
适用于：
1. 函数/类的功能说明
2. 大段代码的逻辑解释
3. 临时注释多行代码
"""
'''
单引号三引号同样支持多行注释
'''
print("多行注释演示")
```

###  变量的定义与使用

**（1）变量的本质**

变量是存储数据的临时容器，程序运行过程中值可动态修改。

**（2）定义语法**

```python
# 变量名 = 变量值（等号两侧保留1个空格）
age = 18  # 整数类型
name = "张三"  # 字符串类型
score = 98.5  # 浮点数类型
```

**（3）命名规则**

**强制规则**

1. 仅能包含字母、数字、下划线（_）

2. 不能以数字开头

3. 严格区分大小写（age 和 Age 是不同变量）

4. 不能使用 Python 关键字（如 if、for、while）

**推荐规范**

1. 见名知义（如 user_name 而非 a1）

2. 多个单词命名：
        

   - 小驼峰：userName（第二个单词首字母大写）

   - 下划线：user_name（推荐，Python 官方风格）

   - 大驼峰：UserName（类名专用）

**（4）变量的数据类型**

Python 是动态类型语言，变量类型由赋值的内容决定：

| 类型            | 说明                        | 示例                                |
| --------------- | --------------------------- | ----------------------------------- |
| 整数（int）     | 无小数的数字                | age = 20                            |
| 浮点数（float） | 带小数的数字                | price = 19.9                        |
| 字符串（str）   | 文本内容（单 / 双引号包裹） | name = "Python"                     |
| 布尔值（bool）  | 逻辑值（True/False）        | is_ok = True                        |
| 列表（list）    | 有序可变集合                | nums = [1,2,3]                      |
| 元组（tuple）   | 有序不可变集合              | info = ("张三", 20)                 |
| 字典（dict）    | 键值对集合                  | student = {"name":"李四", "age":19} |

**（5）类型检测**

```python
# 方法1：type()函数
age = 18
print(type(age))  # <class 'int'>

# 方法2：isinstance()函数（推荐）
print(isinstance(age, int))  # True
print(isinstance(age, str))  # False
```

### 输入与输出

**（1）格式化输出**

方式 1：f-string（Python3.6+，推荐）

```python
name = "李四"
age = 20
score = 95.5
# 基础用法
print(f"姓名：{name}，年龄：{age}，成绩：{score}")
# 格式控制（保留2位小数）
print(f"成绩：{score:.2f}")
# 数字补零（6位宽度）
print(f"学号：{1:06d}")  # 输出：000001
```

方式 2：format() 方法

```python
print("姓名：{}，年龄：{}".format(name, age))
# 指定位置
print("年龄：{1}，姓名：{0}".format(name, age))
# 格式控制
print("成绩：{:.2f}".format(score))
```

方式 3：% 占位符（兼容旧版本）

```python
print("姓名：%s，年龄：%d，成绩：%.2f" % (name, age, score))
```

**（2）转义字符**

| 转义符 | 功能               |
| ------ | ------------------ |
| \n     | 换行               |
| \t     | 制表符（4 个空格） |
| \\     | 反斜杠本身         |
| \"     | 双引号             |
| \'     | 单引号             |

示例：

```python
print("姓名：{}\t年龄：{}\n成绩：{:.2f}".format(name, age, score))
# 自定义print结束符（默认\n）
print("Hello", end=" ")
print("Python")  # 输出：Hello Python
```

**（3）输入函数 input()**

获取用户从键盘输入的内容，**所有输入均为字符串类型**：

```python
# 基础用法
name = input("请输入您的姓名：")
age = input("请输入您的年龄：")
print(f"您输入的姓名：{name}，年龄：{age}")

# 带提示的输入
phone = input("请输入您的手机号：")
print(f"手机号：{phone}，类型：{type(phone)}")
```

###  数据类型转换

当需要对输入的字符串进行数值运算时，需进行类型转换：

| 函数     | 功能             | 示例               |
| -------- | ---------------- | ------------------ |
| int(x)   | 转换为整数       | int("100") → 100   |
| float(x) | 转换为浮点数     | float("9.9") → 9.9 |
| str(x)   | 转换为字符串     | str(18) → "18"     |
| eval(x)  | 执行字符串表达式 | eval("1+2") → 3    |

示例：超市收银系统

```python
# 输入商品信息
product_name = input("请输入商品名称：")
price_str = input("请输入商品单价：")
count_str = input("请输入购买数量：")

# 类型转换
price = float(price_str)
count = int(count_str)

# 计算总价
total = price * count

# 输出结果
print(f"您购买了{product_name}，单价：{price:.2f}元，数量：{count}件，总价：{total:.2f}元")
```

###  运算符

**（1）算术运算符**

| 运算符 | 描述               | 示例          |
| ------ | ------------------ | ------------- |
| +      | 加法               | 10 + 20 → 30  |
| -      | 减法               | 20 - 10 → 10  |
| *      | 乘法               | 10 * 20 → 200 |
| /      | 除法（返回浮点数） | 20 / 10 → 2.0 |
| //     | 整除（向下取整）   | 21 // 10 → 2  |
| %      | 取模（余数）       | 21 % 10 → 1   |
| **     | 幂运算             | 2 ** 3 → 8    |

示例：

```python
a = 10
b = 3
print(f"{a} + {b} = {a + b}")    # 13
print(f"{a} - {b} = {a - b}")    # 7
print(f"{a} * {b} = {a * b}")    # 30
print(f"{a} / {b} = {a / b}")    # 3.3333333333333335
print(f"{a} // {b} = {a // b}")  # 3
print(f"{a} % {b} = {a % b}")    # 1
print(f"{a} ** {b} = {a ** b}")  # 1000
```

**（2）赋值运算符**

| 运算符 | 描述       | 示例                 |
| ------ | ---------- | -------------------- |
| =      | 基础赋值   | x = 10               |
| +=     | 加后赋值   | x += 5 → x = x + 5   |
| -=     | 减后赋值   | x -= 5 → x = x - 5   |
| *      | 乘后赋值   | x *= 5 → x = x * 5   |
| /=     | 除后赋值   | x /= 5 → x = x / 5   |
| //=    | 整除后赋值 | x //= 5 → x = x // 5 |
| %=     | 取模后赋值 | x %= 5 → x = x % 5   |
| **=    | 幂后赋值   | x **= 5 → x = x ** 5 |

**（3）比较运算符（返回布尔值）**

| 运算符 | 描述     | 示例            |
| ------ | -------- | --------------- |
| ==     | 等于     | 10 == 10 → True |
| !=     | 不等于   | 10 != 20 → True |
| >      | 大于     | 20 > 10 → True  |
| <      | 小于     | 10 < 20 → True  |
| >=     | 大于等于 | 20 >= 10 → True |
| <=     | 小于等于 | 10 <= 20 → True |

**（4）逻辑运算符**

| 运算符 | 描述               | 示例                      |
| ------ | ------------------ | ------------------------- |
| and    | 逻辑与（都真才真） | (10>5) and (20>10) → True |
| or     | 逻辑或（有真就真） | (10>5) or (20<10) → True  |
| not    | 逻辑非（取反）     | not (10>5) → False        |

### 条件判断（if 语句）

**（1）核心作用**

根据**条件表达式的布尔结果（True/False）**，执行不同的代码块，实现程序的分支逻辑，是程序实现 “判断” 能力的核心语法。

**（2）基本语法规则**

1. Python 中用 **缩进（4 个空格 / 制表符）** 划分代码块，而非大括号，缩进必须统一

2. 条件表达式后必须加**冒号 :****

3. 条件表达式可结合比较运算符、逻辑运算符组合使用

**（3）四种基本用法**

**① 单分支（if）**

**适用场景**：满足条件则执行某段代码，不满足则跳过

```python
# 语法
if 条件表达式:
    满足条件时执行的代码块（缩进）

# 示例：判断是否成年
age = 19
if age >= 18:
    print("你已成年，可独立出行")
```

**② 双分支（if-else）**

**适用场景**：二选一，满足条件执行 A 代码块，不满足执行 B 代码块

```python
# 语法
if 条件表达式:
    满足条件执行的代码块
else:
    不满足条件执行的代码块

# 示例：判断是否成年
age = int(input("请输入你的年龄："))
if age >= 18:
    print("你已成年，可观看此电影")
else:
    print("你未成年，需由监护人陪同")
```

**③ 多分支（if-elif-else）**

**适用场景**：多个条件依次判断，满足某个条件则执行对应代码块，后续条件不再判断；所有条件都不满足则执行 else

```python
# 语法
if 条件表达式1:
    满足条件1执行的代码块
elif 条件表达式2:
    满足条件2执行的代码块
elif 条件表达式3:
    满足条件3执行的代码块
...
else:
    所有条件都不满足时执行的代码块

# 示例：成绩评级
score = float(input("请输入你的考试成绩："))
if score >= 90:
    print("成绩评级：优秀")
elif score >= 80:
    print("成绩评级：良好")
elif score >= 70:
    print("成绩评级：中等")
elif score >= 60:
    print("成绩评级：及格")
else:
    print("成绩评级：不及格，需要补考")
```

**④ 嵌套分支（if 内部嵌套 if/if-else）**

**适用场景**：主条件满足后，需要再判断细分条件

```python
# 示例：判断是否能参加驾照考试
age = int(input("请输入你的年龄："))
if age >= 18:
    print("你满足年龄要求，可报名驾照考试")
    height = float(input("请输入你的身高（cm）："))
    if height >= 150:
        print("身高符合要求，可正常报名")
    else:
        print("身高未达到要求，无法报名")
else:
    print("年龄未达标，无法报名驾照考试")
```

**（4）条件表达式的高级用法**

1. 结合逻辑运算符实现复杂条件

```python
# 示例：判断是否为工作日的工作时间
hour = int(input("请输入当前小时数（0-23）："))
weekday = input("请输入是否为工作日（是/否）：")
if weekday == "是" and 9 <= hour <= 18:
    print("当前是工作时间，请专注工作")
else:
    print("当前是非工作时间，可休息")
```

1. 三元表达式（简化单 / 双分支）
       **语法**：`结果1 if 条件表达式 else 结果2`（满足条件返回结果 1，否则返回结果 2）

```python
# 示例：简化判断成年与否
age = 20
result = "成年" if age >= 18 else "未成年"
print(f"你是：{result}")

# 等价于原双分支代码
if age >= 18:
    result = "成年"
else:
    result = "未成年"
```

**（5）常见易错点**

1. 忘记写**冒号 **：条件表达式和 else/elif 后必须加冒号，否则语法报错

2. 缩进不统一：同一代码块的缩进必须一致（要么全 4 个空格，要么全制表符）

3. 把**赋值号 =**当成**等于号 ==**：条件判断中判断相等必须用`==`，`=`是赋值，会导致逻辑错误

```python
# 错误写法
if age = 18:  # 赋值操作，非判断，直接报错
    print("成年")

# 正确写法
if age == 18:
    print("刚成年")
```

1. 多分支中条件顺序错误：多分支是**依次判断**，范围大的条件不能写在前面

```python
# 错误写法：score>=60写在前面，会导致80+的成绩也判断为"及格"
score = 85
if score >= 60:
    print("及格")
elif score >= 80:
    print("良好")

# 正确写法：从范围小的条件开始判断
if score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
```

## 综合实战案例

**案例 1：简易成绩管理系统（含条件判断）**

```python
"""
简易成绩管理系统
功能：
1. 输入学生姓名和三门科目成绩
2. 计算总分和平均分
3. 根据平均分进行成绩评级
4. 格式化输出所有信息
"""

# 输入学生信息
student_name = input("请输入学生姓名：")
chinese_str = input("请输入语文成绩：")
math_str = input("请输入数学成绩：")
english_str = input("请输入英语成绩：")

# 类型转换（处理输入的字符串，转为浮点数）
chinese = float(chinese_str)
math = float(math_str)
english = float(english_str)

# 计算总分和平均分
total_score = chinese + math + english
avg_score = total_score / 3

# 条件判断：根据平均分评级
if avg_score >= 90:
    grade = "优秀"
elif avg_score >= 80:
    grade = "良好"
elif avg_score >= 70:
    grade = "中等"
elif avg_score >= 60:
    grade = "及格"
else:
    grade = "不及格"

# 格式化输出结果
print("=" * 40)
print(f"学生姓名：{student_name}")
print(f"语文成绩：{chinese:.1f}分")
print(f"数学成绩：{math:.1f}分")
print(f"英语成绩：{english:.1f}分")
print(f"总成绩：{total_score:.1f}分")
print(f"平均成绩：{avg_score:.1f}分")
print(f"成绩评级：{grade}")
print("=" * 40)
```

**案例 2：班级活动费用分摊系统（运算符 + 输入输出 + 条件判断）**

```python
"""
班级活动费用分摊系统
功能：
1. 输入参与人数和活动总花费
2. 额外收取10%组织管理费，计算最终总费用
3. 判断人数是否合法（至少1人）
4. 计算每人需要分摊的金额并输出
"""

# 输入并转换数据类型
total_people = int(input("请输入参与活动人数："))
total_cost = float(input("请输入活动总花费（元）："))

# 条件判断：人数是否合法
if total_people < 1:
    print("人数输入错误，至少1人！")
else:
    # 计算含组织管理费的总费用和人均费用
    manage_fee = total_cost * 0.1  # 10%组织管理费
    final_total = total_cost + manage_fee
    per_person = final_total / total_people
    
    # 格式化输出
    print("=" * 30)
    print(f"原始活动花费：{total_cost:.2f}元")
    print(f"10%组织管理费：{manage_fee:.2f}元")
    print(f"最终总费用：{final_total:.2f}元")
    print(f"参与人数：{total_people}人")
    print(f"每人需分摊：{per_person:.2f}元")
    print("=" * 30)
```

## 学习建议

1. 多敲代码：基础语法（尤其是 if 判断）需通过反复练习巩固，建议每天编写 1-2 个带判断逻辑的小案例

2. 注重缩进：养成统一缩进的习惯，这是 Python 的核心语法规范，也是新手最易出错的点

3. 调试思维：遇到条件判断逻辑错误时，用`print()`打印条件表达式的结果，排查判断逻辑问题

4. 简化代码：简单的双分支逻辑尝试用三元表达式实现，提升代码简洁性

5. 场景练习：结合生活场景（如成绩评级、会员判断、缴费计算）设计带判断逻辑的程序，学以致用

## 课后练习

1. 编写程序：输入一个整数，判断其是奇数还是偶数（提示：用取模运算符`%`，偶数 %2=0）

2. 编写程序：输入一个人的身高和体重，计算 BMI 指数并判断体型（偏瘦 / 正常 / 超重 / 肥胖）
        

   - BMI 公式：BMI = 体重 (kg) / (身高 (m))²

   - 标准：<18.5 偏瘦，18.5-23.9 正常，24-27.9 超重，≥28 肥胖

3. 编写程序：模拟超市会员打折，非会员无折扣，会员消费满 200 减 50，不满 200 打 9 折（输入会员状态和消费金额，输出实际支付金额）

