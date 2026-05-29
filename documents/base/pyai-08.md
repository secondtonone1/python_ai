---
title: Python文件读写和异常处理
date: 2026-05-03 12:06:09
tags: [python,AI]
categories: [python,AI]
---

## 目录

1. 文件读写基础
2. 异常处理
3. 包与模块管理
4. 实战项目

------

## 第一部分：文件读写基础

###  为什么要学文件操作？

程序运行时的数据存储在内存中，程序结束后数据就消失了。文件操作让我们能够：

- **数据持久化**：保存数据到硬盘
- **数据读取**：读取之前保存的数据
- **大数据处理**：处理超过内存容量的数据
- **日志记录**：记录程序运行过程

### 文件操作的三个步骤

```
1. 打开文件 (open)
   ↓
2. 读写文件 (read/write)
   ↓
3. 关闭文件 (close)
```

###  open() 函数详解

#### 基本语法

```python
open(filename, mode, encoding)
```

#### 参数说明

| 参数     | 说明         | 示例                             |
| -------- | ------------ | -------------------------------- |
| filename | 文件名或路径 | 'example.txt', './data/file.txt' |
| mode     | 打开模式     | 'r', 'w', 'a', 'x'               |
| encoding | 编码方式     | 'utf-8', 'gbk'                   |

#### 打开模式详解

| 模式 | 含义         | 文件存在 | 文件不存在 |
| ---- | ------------ | -------- | ---------- |
| 'r'  | 读取（默认） | 打开     | 报错       |
| 'w'  | 写入         | 覆盖     | 创建       |
| 'a'  | 追加         | 追加     | 创建       |
| 'x'  | 创建         | 报错     | 创建       |

###  最简单的文件读取

```python
# 方式1：一次性读取全部内容
with open('example.txt', 'r', encoding='utf-8') as f:
    content = f.read()
print(content)
```

**为什么使用 with 语句？**

- 自动打开文件
- 自动关闭文件
- 即使发生错误也会关闭文件
- 代码更简洁

###  三种读取方式

#### 方式1：read() - 一次性读取全部

```python
with open('example.txt', 'r', encoding='utf-8') as f:
    content = f.read()  # 返回字符串
```

**适用场景**：小文件，需要全部内容
**风险**：大文件会占用大量内存

#### 方式2：readline() - 逐行读取

```python
with open('example.txt', 'r', encoding='utf-8') as f:
    line = f.readline()  # 读取一行
    while line:
        print(line.rstrip('\n'))  # 移除换行符
        line = f.readline()
```

**适用场景**：需要逐行处理
**优点**：内存占用少

#### 方式3：readlines() - 读取所有行到列表

```python
with open('example.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()  # 返回列表
    for i, line in enumerate(lines):
        print(f"第{i+1}行: {line.rstrip()}")
```

**适用场景**：需要随机访问行
**风险**：大文件占用内存

#### 方式4：迭代读取（最推荐）

```python
with open('example.txt', 'r', encoding='utf-8') as f:
    for line in f:  # 最高效的方式
        print(line.rstrip('\n'))
```

**优点**：

- 内存效率最高
- 代码最简洁
- 最Pythonic

### 处理大文件

#### 分块读取

```python
def read_large_file_by_chunks(filename, chunk_size=1024):
    """分块读取大文件"""
    with open(filename, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            process_data(chunk)
```

#### 按行分块读取

```python
def read_large_file_by_lines(filename, batch_size=1000):
    """按行分块读取大文件"""
    batch = []
    with open(filename, 'r', encoding='utf-8') as f:
        # 从文件中按照行读取
        for line in f:
            batch.append(line.rstrip('\n'))
            if len(batch) == batch_size:
                process_batch(batch)
                batch = []
        if batch:
            process_batch(batch)
```

###  文件写入

#### 写入模式

```python
# 模式1：写入（覆盖）
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('第一行\n')
    f.write('第二行\n')

# 模式2：追加
with open('output.txt', 'a', encoding='utf-8') as f:
    f.write('追加的内容\n')

# 模式3：使用 print() 函数
with open('output.txt', 'w', encoding='utf-8') as f:
    print('第一行', file=f)
    print('第二行', file=f)
```

#### 写入列表

```python
lines = ['第一行\n', '第二行\n', '第三行\n']
with open('output.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)
```

###  文件指针操作

```python
with open('example.txt', 'r', encoding='utf-8') as f:
    # tell() - 获取当前位置
    print(f.tell())  # 0
    
    # 读取 10 个字符
    content = f.read(10)
    print(f.tell())  # 10
    
    # seek() - 移动指针
    f.seek(0)  # 回到开头
    f.seek(5, 0)  # 从开头移动 5 字节
    
    # 获取文件大小
    f.seek(0, 2)
    file_size = f.tell()
```

###  处理 CSV 文件

```python
# 读取 CSV
def read_csv(filename):
    students = []
    with open(filename, 'r', encoding='utf-8') as f:
        f.readline()  # 跳过表头
        for line in f:
            name, age, score = line.rstrip('\n').split(',')
            students.append({
                'name': name,
                'age': int(age),
                'score': int(score)
            })
    return students

# 写入 CSV
def write_csv(filename, students):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('name,age,score\n')
        for student in students:
            line = f"{student['name']},{student['age']},{student['score']}\n"
            f.write(line)
```

###  处理 JSON 文件

```python
import json

# 读取 JSON
def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 写入 JSON
def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

------

## 第二部分：异常处理

###  什么是异常？

异常是程序执行过程中发生的错误事件。

**常见异常类型**：

- `FileNotFoundError` - 文件不存在
- `PermissionError` - 没有权限
- `ValueError` - 值错误
- `TypeError` - 类型错误
- `ZeroDivisionError` - 除以零
- `IndexError` - 索引超出范围
- `KeyError` - 字典键不存在

### 为什么需要异常处理？

1. **防止程序崩溃** - 程序可以继续运行
2. **提供有意义的错误信息** - 帮助用户理解问题
3. **采取恢复措施** - 尝试其他方法或保存数据

###  基础异常处理：try-except

#### 基本结构

```python
try:
    # 可能出错的代码
except 异常类型:
    # 处理异常的代码
```

#### 示例1：捕获特定异常

```python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("错误：不能除以零")
        return None
    return result

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # 错误：不能除以零
```

#### 示例2：文件操作中的异常处理

```python
def safe_read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
        return None
```

### 2.4 捕获多个异常

#### 方式1：多个 except 块

```python
try:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print("错误：文件不存在")
except PermissionError:
    print("错误：没有权限")
except UnicodeDecodeError:
    print("错误：编码错误")
```

#### 方式2：一个 except 块捕获多个异常

```python
try:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
except (FileNotFoundError, PermissionError):
    print("错误：文件访问失败")
```

###  获取异常信息

```python
try:
    with open('nonexistent.txt', 'r') as f:
        content = f.read()
except FileNotFoundError as e:
    print(f"异常类型: {type(e)}")
    print(f"异常信息: {e}")
```

###  完整的异常处理结构

```python
try:
    # 可能出错的代码
    with open('example.txt', 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print("错误：文件不存在")
except Exception as e:
    print(f"发生错误: {e}")
else:
    # 只有在 try 块成功执行时才运行
    print(f"文件读取成功，内容长度: {len(content)} 字符")
finally:
    # 无论如何都会执行
    print("文件操作完成")
```

**执行流程**：

1. 执行 try 块
2. 如果发生异常，执行对应的 except 块
3. 如果没有异常，执行 else 块
4. 无论如何，最后执行 finally 块

###  finally 块的重要用途

```python
f = None
try:
    f = open('example.txt', 'r', encoding='utf-8')
    content = f.read()
except FileNotFoundError:
    print("错误：文件不存在")
finally:
    # 即使发生异常，这里也会执行
    if f is not None:
        f.close()
        print("文件已关闭")
```

**注意**：这种方式不如 with 语句安全，推荐使用 with 语句。

###  异常的传播

```python
def func2():
    x = 1 / 0  # 这里会抛出异常

def func1():
    func2()  # 异常会从这里传播出去

def main():
    try:
        func1()
    except ZeroDivisionError:
        print("捕获到异常：除以零")

main()
```

**异常传播链**：

```
main() 
  ↓
func1() 
  ↓
func2() (异常发生)
  ↓
func1() (没有处理，继续传播)
  ↓
main() (捕获异常)
```

###  实战：安全的文件读写

```python
def safe_read_file(filename):
    """完整的安全文件读取函数"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
        return None
    except PermissionError:
        print(f"错误：没有权限读取文件 '{filename}'")
        return None
    except UnicodeDecodeError:
        print(f"错误：文件编码错误，尝试使用 GBK 编码")
        try:
            with open(filename, 'r', encoding='gbk') as f:
                content = f.read()
            return content
        except:
            return None
    except IOError as e:
        print(f"错误：I/O 错误 - {e}")
        return None

def safe_write_file(filename, content):
    """完整的安全文件写入函数"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"成功写入文件 '{filename}'")
        return True
    except PermissionError:
        print(f"错误：没有权限写入文件 '{filename}'")
        return False
    except IOError as e:
        print(f"错误：写入失败 - {e}")
        return False
```

------

## 第三部分：包与模块管理

###  模块与包的概念

#### 模块（Module）

- 单个 `.py` 文件
- 包含 Python 代码
- 可以被导入使用

#### 包（Package）

- 包含 `__init__.py` 文件的目录
- 可以包含多个模块和子包
- 用于组织相关的模块

###  最小包结构

```
myproject/
├── mypackage/
│   ├── __init__.py
│   └── module.py
└── main.py
```

###  完整包结构

```
myproject/
├── README.md
├── setup.py
├── requirements.txt
├── mypackage/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   └── utils.py
│   ├── io/
│   │   ├── __init__.py
│   │   ├── reader.py
│   │   └── writer.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
└── examples/
    └── example.py
```

###  **init**.py 的作用

#### 作用1：标记目录为包

```python
# 有 __init__.py 的目录被识别为包
# 没有 __init__.py 的目录不是包
```

#### 作用2：初始化包

```python
# mypackage/__init__.py
print("mypackage 已加载")
```

#### 作用3：定义公共接口

```python
# mypackage/__init__.py
from .core import engine
from .io import reader

__all__ = ['engine', 'reader']
```

###  导入方式

#### 方式1：导入整个模块

```python
import mypackage.core.engine
engine_obj = mypackage.core.engine.Engine()
```

#### 方式2：导入特定内容

```python
from mypackage.core.engine import Engine
engine_obj = Engine()
```

#### 方式3：导入子包

```python
from mypackage.core import engine
engine_obj = engine.Engine()
```

#### 方式4：相对导入（仅在包内使用）

```python
# 在 mypackage/io/reader.py 中
from . import writer  # 导入同级模块
from ..core import engine  # 导入上级包的模块
```

###  创建自定义包

#### 步骤1：创建目录结构

```bash
mkdir datatools
mkdir datatools/core
mkdir datatools/io
mkdir datatools/utils
```

#### 步骤2：创建 **init**.py 文件

```python
# datatools/__init__.py
__version__ = "1.0.0"

from .core import processor
from .io import reader, writer

__all__ = ['processor', 'reader', 'writer']
```

#### 步骤3：创建模块文件

```python
# datatools/core/processor.py
def process_data(data):
    """处理数据"""
    return data
# datatools/io/reader.py
def read_file(filename):
    """读取文件"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()
```

#### 步骤4：使用包

```python
import datatools
from datatools import processor, reader

data = reader.read_file('data.txt')
result = processor.process_data(data)
```

###  setup.py - 包的安装配置

```python
from setuptools import setup, find_packages

setup(
    name='datatools',
    version='1.0.0',
    description='数据处理工具包',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/datatools',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.19.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
```

###  安装包

```bash
# 本地开发安装（推荐）
pip install -e .

# 普通安装
pip install .

# 从 PyPI 安装
pip install datatools

# 指定版本
pip install datatools==1.0.0
```

###  requirements.txt

```
# requirements.txt
numpy>=1.19.0
pandas>=1.1.0
requests>=2.25.0
```

**使用方式**：

```bash
pip install -r requirements.txt
```

------

## 第四部分：实战项目

### 项目1：学生成绩管理系统

#### 项目结构

```
grade_system/
├── main.py
├── students.csv
└── utils.py
```

#### main.py

```python
import csv
import json

def read_students_csv(filename):
    """读取学生信息"""
    students = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append({
                    'name': row['name'],
                    'age': int(row['age']),
                    'score': float(row['score'])
                })
        return students
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
        return []
    except ValueError:
        print("错误：数据格式错误")
        return []

def calculate_average(students):
    """计算平均成绩"""
    if not students:
        return 0
    total = sum(float(s['score']) for s in students)
    return total / len(students)

def find_top_student(students):
    """找出成绩最高的学生"""
    if not students:
        return None
    return max(students, key=lambda s: s['score'])

def save_report(filename, students):
    """保存成绩报告"""
    try:
        report = {
            'total_students': len(students),
            'average_score': calculate_average(students),
            'top_student': find_top_student(students),
            'students': students
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"报告已保存到 '{filename}'")
    except IOError as e:
        print(f"错误：保存报告失败 - {e}")

def main():
    """主函数"""
    # 读取学生信息
    students = read_students_csv('students.csv')
    
    if not students:
        print("没有学生数据")
        return
    
    # 显示统计信息
    print(f"总学生数：{len(students)}")
    print(f"平均成绩：{calculate_average(students):.2f}")
    
    top = find_top_student(students)
    if top:
        print(f"最高成绩：{top['name']} - {top['score']}")
    
    # 保存报告
    save_report('report.json', students)

if __name__ == '__main__':
    main()
```

### 项目2：日志记录系统

#### 项目结构

```
log_system/
├── main.py
├── logger.py
└── logs/
```

#### logger.py

```python
import os
from datetime import datetime

def create_log_file(log_dir='logs'):
    """创建日志目录"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def write_log(message, log_dir='logs', level='INFO'):
    """写入日志"""
    try:
        # 创建日志目录
        create_log_file(log_dir)
        
        # 生成日志文件名
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(log_dir, f'{today}.log')
        
        # 生成日志内容
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_content = f"[{timestamp}] [{level}] {message}\n"
        
        # 写入日志
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_content)
        
        print(f"日志已记录：{log_content.strip()}")
    except IOError as e:
        print(f"错误：写入日志失败 - {e}")

def read_logs(log_dir='logs', date=None):
    """读取日志"""
    try:
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        log_file = os.path.join(log_dir, f'{date}.log')
        
        if not os.path.exists(log_file):
            print(f"日志文件不存在：{log_file}")
            return []
        
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = f.readlines()
        
        return logs
    except IOError as e:
        print(f"错误：读取日志失败 - {e}")
        return []

def main():
    """主函数"""
    # 写入日志
    write_log("程序启动", level='INFO')
    write_log("开始处理数据", level='INFO')
    
    try:
        # 模拟处理
        result = 10 / 0
    except ZeroDivisionError:
        write_log("发生错误：除以零", level='ERROR')
    
    write_log("程序结束", level='INFO')
    
    # 读取日志
    logs = read_logs()
    print("\n今日日志：")
    for log in logs:
        print(log.strip())

if __name__ == '__main__':
    main()
```

### 项目3：配置文件管理

#### 项目结构

```
config_system/
├── main.py
├── config.json
└── config_manager.py
```

#### config_manager.py

```python
import json
import os

def load_config(filename):
    """加载配置文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"配置已加载：{filename}")
        return config
    except FileNotFoundError:
        print(f"错误：配置文件不存在 - {filename}")
        return {}
    except json.JSONDecodeError:
        print(f"错误：配置文件格式错误 - {filename}")
        return {}

def save_config(filename, config):
    """保存配置文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"配置已保存：{filename}")
        return True
    except IOError as e:
        print(f"错误：保存配置失败 - {e}")
        return False

def get_config_value(config, key, default=None):
    """获取配置值"""
    return config.get(key, default)

def set_config_value(config, key, value):
    """设置配置值"""
    config[key] = value
    return config

def main():
    """主函数"""
    config_file = 'config.json'
    
    # 加载配置
    config = load_config(config_file)
    
    if not config:
        # 创建默认配置
        config = {
            'app_name': 'MyApp',
            'version': '1.0.0',
            'debug': True,
            'port': 8000
        }
        save_config(config_file, config)
    
    # 获取配置值
    app_name = get_config_value(config, 'app_name')
    print(f"应用名称：{app_name}")
    
    # 修改配置
    config = set_config_value(config, 'debug', False)
    save_config(config_file, config)

if __name__ == '__main__':
    main()
```

------

