---
title: 魔法方法
date: 2026-06-14 11:15:28
tags: [python,AI]
categories: [python,AI]
---

# Python 魔术方法是什么

魔术方法就是前后都有双下划线的方法，例如：

```python
__str__
__len__
__getitem__
```

它们不是让你直接调用的，而是让 Python 在某些语法场景下自动调用。

例如：

```python
len(obj)
```

背后其实会调用：

```python
obj.__len__()
```

------

# 1. `__new__`

## 作用

`__new__` 负责“创建对象”。

对象创建过程分两步：

```python
obj = 类名()
```

实际顺序是：

```python
__new__   # 先创建对象
__init__  # 再初始化对象
```

## 示例

```python
'''
演示new方法
'''
class Person:
    # cls是类名,name是形参接受实参
    # __new__的形参取决于接受的实参的个数
    def __new__(cls,name):
        print(f'__new__:创建对象')
        # 一层一层向上找，直到找到object的__new__方法
        # object的__new__方法是创建对象的
        obj = super().__new__(cls)
        return obj
    # self 存储的是对象，这个对象从__new__返回的
    def __init__(self,name):
        print(f'__init__: 初始化对象')
        self.name=name

class A:
    def __new__(cls):
        print('创建失败')
        return None
    def __init__(self):
        print('初始化')

if __name__ == '__main__':
    '''
    下面的创建对象的流程，相当于
    obj = Person.__new__(Person, 'Tom')
    obj = Person.__init__(obj,'Tom')
    '''
    p = Person('Tom')
    print(p.name)
    '''
    因为A类的new方法返回的是None, 所以不会调用init方法
    '''
    a = A()

```

输出：

```python
__new__：创建对象
__init__：初始化对象
```

## 注意

`__new__` 必须返回对象实例，否则 `__init__` 不会正常执行。

```python
class A:
    def __new__(cls):
        print("创建失败")
        return None

    def __init__(self):
        print("初始化")


a = A()
print(a)
```

输出：

```python
创建失败
None
```

------

**示例：单例**

```python
'''
演示单例模式
'''

'''
单例模式，就是无论同一个类创建多少对象，都是同一个对象
网络编程，TcpServer, DBManager
'''

class Singleton(object):
    # 类属性
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

a = Singleton()
b = Singleton()
print(a is b)
print(f'id(a) is {id(a)}')
print(f'id(b) is {id(b)}')
```

**注意：**

- 必须返回实例，否则对象创建失败
- 比 `__init__` 更底层



# 2. `__str__`

## 作用

`__str__` 用来定义对象给“用户”看的字符串。

## 触发方式

```python
print(obj)
str(obj)
```

## 示例

```python
'''
演示new方法
'''
class Person:
    def __init__(self,name):
        self.name=name
    # 打印对象的时候会输出__str__返回的字符串
    def __str__(self):
        return f'我的名字是: {self.name}'

if __name__ == '__main__':
    p = Person('Zack')
    print(f'p is {p}')

```

输出：

```python
姓名：Tom，年龄：18
```

------

# 3. `__repr__`

## 作用

`__repr__` 用来定义对象给“开发者”看的字符串，主要用于调试。

## 触发方式

```python
repr(obj)
```

或者在交互式环境中直接输入对象：

```python
p
```

## 示例

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"


p = Person("Tom", 18)

print(repr(p))
```

输出：

```python
Person(name='Tom', age=18)
```

## __str__ 和 __repr__的区别

```python
'''
演示new方法
'''
class Person:
    def __init__(self,name):
        self.name=name
    # 打印对象的时候会输出__str__返回的字符串
    def __str__(self):
        return f'我的名字是: {self.name}'

    # 用于调试的字符串输出
    def __repr__(self):
        return f'in __repr__ 我的名字是: {self.name}'

if __name__ == '__main__':
    '''
    __str__和__repr__都能在打印的时候输出指定的字符串
    如果实现了__str__优先调用__str__
    否则没有实现__str__再去查找__repr__
    '''
    p = Person('Zack')
    # 默认调用__str__
    print(f'p is {p}')
    # 显示调用repr
    print(repr(p))
    # 显示调用str
    print(str(p))

```

输出：

```python
我是 Tom
Person('Tom')
```

区别：

| 方法            | 面向对象             | 典型用途           |
| --------------- | -------------------- | ------------------ |
| `__str__`       | 普通用户             | 打印展示           |
| `__repr__`      | 开发者               | 调试、日志         |
| 只写 `__repr__` | `str(obj)` 也会用它  | 常见               |
| 只写 `__str__`  | `repr(obj)` 不会用它 | 调试信息仍然不清晰 |

------

# 4. `__len__`

## 作用

定义对象的长度。

## 触发方式

```python
len(obj)
```

## 示例

```python
'''
演示new方法
'''
class MyList:
    def __init__(self,list_data):
        self.list_data =list_data
    # 返回列表的长度
    def __len__(self):
        return len(self.list_data)

if __name__ == '__main__':
    '''
    调用len会触发__len__
    '''
    my_list = MyList([1,2,3])
    print(len(my_list))

```

输出：

```python
3
```

## 注意

`__len__` 必须返回整数。

------

# 5. `__getitem__`

## 作用

让对象支持中括号取值。

## 触发方式

```python
obj[key]
```

## 示例：像字典一样取值

```python
'''
演示new方法
'''
class MyDict:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.dict = {'name':name,'age':age}

    def __getitem__(self,key):
        if key not in self.dict:
            return None
        return self.dict[key]

if __name__ == '__main__':
    my_dict = MyDict(name='zack',age=38)
    # 当一个对象当成字典根据key获取值使用的时候会触发getitem
    print(my_dict['name'])
    print(my_dict['age'])

```

输出：

```python
zack
38
```

------

# 6. `__setitem__`

## 作用

让对象支持中括号赋值。

## 触发方式

```python
obj[key] = value
```

## 示例

```python
'''
演示new方法
'''
class MyDict:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.dict = {'name':name,'age':age}

    def __getitem__(self,key):
        if key not in self.dict:
            return None
        return self.dict[key]

    def __setitem__(self,key,value):
        self.dict[key] = value

if __name__ == '__main__':
    my_dict = MyDict(name='zack',age=38)
    # 当一个对象当成字典根据key获取值使用的时候会触发getitem
    print(my_dict['name'])
    print(my_dict['age'])
    # 当一个对象当成字典，通过key修改或者添加value的时候触发setitem
    # 添加key和value
    my_dict['hobbies'] = ['run','read','games']
    # 修改key和value
    my_dict['age'] = 18
    print(my_dict['hobbies'])
    print(my_dict['age'])
```

------

# 7. `__delitem__`

## 作用

让对象支持中括号删除。

## 触发方式

```python
del obj[key]
```

## 示例

```python
'''
演示new方法
'''
class MyDict:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.dict = {'name':name,'age':age}

    def __getitem__(self,key):
        if key not in self.dict:
            return None
        return self.dict[key]

    def __setitem__(self,key,value):
        self.dict[key] = value

    def __delitem__(self,key):
        if key not in self.dict:
            return
        del self.dict[key]

if __name__ == '__main__':
    my_dict = MyDict(name='zack',age=38)
    # 当一个对象当成字典根据key获取值使用的时候会触发getitem
    print(my_dict['name'])
    print(my_dict['age'])
    # 当一个对象当成字典，通过key修改或者添加value的时候触发setitem
    # 添加key和value
    my_dict['hobbies'] = ['run','read','games']
    # 修改key和value
    my_dict['age'] = 18
    print(my_dict['hobbies'])
    print(my_dict['age'])

    # 把一个对象当成字典，删除key和value会触发delitem
    del my_dict['hobbies']
    print(my_dict['hobbies'])
```

------

# 8. `__contains__`

## 作用

让对象支持 `in` 判断。

## 触发方式

```python
key in obj
```

## 示例

```python
'''
演示new方法
'''
class MyDict:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.dict = {'name':name,'age':age}

    def __getitem__(self,key):
        if key not in self.dict:
            return None
        return self.dict[key]

    def __setitem__(self,key,value):
        self.dict[key] = value

    def __delitem__(self,key):
        if key not in self.dict:
            return
        del self.dict[key]

if __name__ == '__main__':
    my_dict = MyDict(name='zack',age=38)
    # 当一个对象当成字典根据key获取值使用的时候会触发getitem
    print(my_dict['name'])
    print(my_dict['age'])
    # 当一个对象当成字典，通过key修改或者添加value的时候触发setitem
    # 添加key和value
    my_dict['hobbies'] = ['run','read','games']
    # 修改key和value
    my_dict['age'] = 18
    print(my_dict['hobbies'])
    print(my_dict['age'])

    # 把一个对象当成字典，删除key和value会触发delitem
    del my_dict['hobbies']
    print(my_dict['hobbies'])
```

输出：

```python
True
False
```

------

# 9. `__call__`

## 作用

让对象像函数一样被调用。

## 触发方式

```python
obj()
obj(参数)
```

## 示例

```python
class Add:
    def __call__(self, x, y):
        return x + y


add = Add()

print(add(3, 5))
```

输出：

```python
8
```

## 使用场景

常用于：

```python
模型对象()
装饰器对象()
任务执行器()
```

例如：

```python
class Greeter:
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print(f"你好，{self.name}")


g = Greeter("Tom")
g()
```

------

# 10. `__iter__`

## 作用

让对象可以被 `for` 循环遍历。

## 触发方式

```python
for x in obj:
    ...
```

实际会先调用：

```python
iter(obj)
```

也就是：

```python
obj.__iter__()
```

------

# 11. `__next__`

## 作用

定义每次迭代返回什么值。

## 触发方式

```python
next(obj)
```

## 示例：自定义计数器

```python
'''
演示迭代器实现
'''

class Counter:
    def __init__(self,max_num):
        self.max_num = max_num
        self.current = 0

    # 返回迭代器对象
    def __iter__(self):
        '''
        返回可迭代对象
        :return:
        '''
        return self

    # 返回一个值
    def __next__(self):
        '''
        next函数接受的是一个可迭代对象
        :return:
        '''
        if self.current < self.max_num:
            self.current += 1
            return self.current
        # 抛出停止异常
        raise StopIteration

if __name__ == '__main__':
    counter = Counter(2)
    # 可以通过next从迭代器中获取数据
    print(next(counter))
    print(next(counter))
    try:
        print(next(counter))
    except StopIteration:
        print('迭代停止...')
    print('😔'*20)
    # 可以使用for循环
    counter2 = Counter(3)
    for num in counter2:
        print(num)


```

## 重点

迭代器必须满足：

```python
__iter__ 返回自己
__next__ 返回下一个元素
没有元素时 raise StopIteration
```

------

# 12. `__enter__`

## 作用

进入 `with` 语句时执行。

## 触发方式

```python
with obj as x:
    ...
```

会调用：

```python
obj.__enter__()
```

------

# 13. `__exit__`

## 作用

离开 `with` 语句时执行。

即使 `with` 里面发生异常，也会执行。

## 示例

```python
class MyContext:
    def __enter__(self):
        print("进入 with")
        return "资源对象"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("退出 with")
        print("异常类型：", exc_type)
        print("异常值：", exc_val)


with MyContext() as resource:
    print(resource)
```

输出：

```python
进入 with
资源对象
退出 with
异常类型： None
异常值： None
```

------

## RAII自动加解锁

**为什么要用 `with + 锁`**

普通写法（容易出问题）：

```python
lock.acquire()
try:
    # 临界区代码
    ...
finally:
    lock.release()
```

问题：

- 容易忘记释放锁
- 出异常时容易死锁

👉 用 `with` 可以自动管理

------

**基础示例：用 `with` 实现加锁/解锁**

```python
import threading

class MyLock:
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        print("加锁")
        self.lock.acquire()
        return self  # 可选

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("解锁")
        self.lock.release()
        # return False 表示异常继续抛出（默认行为）
```

------

**使用方式**

```python
lock = MyLock()

with lock:
    print("临界区代码")
```

输出：

```
加锁
临界区代码
解锁
```

------

**关键点解释**

__enter__

```
def __enter__(self):
    self.lock.acquire()
```

👉 进入 `with` 时执行
 👉 用来“申请资源”（加锁、打开文件、连接数据库）

------

__exit__

```
def __exit__(self, exc_type, exc_val, exc_tb):
    self.lock.release()
```

👉 离开 `with` 时执行
 👉 无论是否异常都会执行

``` python
lock = MyLock()

try:
    with lock:
        print("执行中")
        raise ValueError("出错了")
except:
    print("捕获异常")
```



# 综合案例：模拟一个字典类

```python
class MyDict:
    def __init__(self):
        self.data = {}

    def __str__(self):
        return f"MyDict内容：{self.data}"

    def __repr__(self):
        return f"MyDict({self.data!r})"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        print(f"正在读取 key：{key}")
        return self.data[key]

    def __setitem__(self, key, value):
        print(f"正在设置 {key} = {value}")
        self.data[key] = value

    def __delitem__(self, key):
        print(f"正在删除 key：{key}")
        del self.data[key]

    def __contains__(self, key):
        return key in self.data

    def __call__(self):
        print("当前数据：", self.data)

    def __iter__(self):
        return iter(self.data)


d = MyDict()

d["name"] = "Tom"
d["age"] = 18

print(d["name"])
print(len(d))
print("age" in d)

for key in d:
    print(key)

d()

del d["age"]

print(d)
print(repr(d))
```

输出大致是：

```python
正在设置 name = Tom
正在设置 age = 18
正在读取 key：name
Tom
2
True
name
age
当前数据： {'name': 'Tom', 'age': 18}
正在删除 key：age
MyDict内容：{'name': 'Tom'}
MyDict({'name': 'Tom'})
```

------

# 总结

| 魔术方法       | 对应语法                  | 作用                 |
| -------------- | ------------------------- | -------------------- |
| `__new__`      | `Class()`                 | 创建对象             |
| `__str__`      | `print(obj)` / `str(obj)` | 面向用户的字符串     |
| `__repr__`     | `repr(obj)`               | 面向开发者的字符串   |
| `__len__`      | `len(obj)`                | 返回长度             |
| `__getitem__`  | `obj[key]`                | 读取元素             |
| `__setitem__`  | `obj[key] = value`        | 设置元素             |
| `__delitem__`  | `del obj[key]`            | 删除元素             |
| `__contains__` | `key in obj`              | 判断是否包含         |
| `__call__`     | `obj()`                   | 对象像函数一样调用   |
| `__iter__`     | `iter(obj)` / `for`       | 返回迭代器           |
| `__next__`     | `next(obj)`               | 返回下一个元素       |
| `__enter__`    | `with obj`                | 进入上下文           |
| `__exit__`     | `with 结束`               | 退出上下文，释放资源 |