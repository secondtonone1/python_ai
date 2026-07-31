---
title: Python进阶之线程
date: 2026-07-18 20:38:35
tags: [python,AI]
categories: [python,AI]
---

## 线程基础概念

### 1. 进程 vs 线程

- **进程**：操作系统资源分配最小单位，每个进程独立内存、CPU、文件句柄，进程间通信成本极高。
- **线程**：进程内执行单元，共享进程内存资源，创建销毁开销极小，又称**轻量级进程**。
- 关系：一个进程至少包含 1 个主线程，多线程共享全局变量。

### 2. 适用场景

✅ 适合：IO 密集型任务（网络请求、文件读写、数据库、等待接口）

❌ 不适合：CPU 密集型计算（Python GIL 全局解释器锁限制，同一时刻仅 1 个线程执行 CPU 运算）

![image-20260719185501598](https://cdn.llfc.club/image-20260719185501598.png)

### 3. GIL 全局解释器锁

CPython 独有锁，规则：

1. 同一时间只有一个线程持有 GIL 执行字节码；

2. IO 阻塞时自动释放 GIL；

3. CPU 运算达到时间片阈值会切换 GIL；

   

   结论：多线程对 CPU 计算无加速效果，CPU 密集任务改用`multiprocessing`多进程。

## Python 线程两大标准库

1. `_thread`：底层简陋库，不推荐生产使用
2. `threading`：高层封装，功能完善，日常开发首选

## 创建线程两种方式

### 方式 1：函数式（最简单，推荐日常使用）

```python
import threading
import time

def task(name, delay):
    """线程执行函数"""
    print(f"线程 {name} 启动，休眠 {delay}s")
    time.sleep(delay)
    print(f"线程 {name} 执行完毕")

if __name__ == "__main__":
    # 创建线程对象 target=执行函数 args=参数元组
    t1 = threading.Thread(target=task, args=("A", 2))
    t2 = threading.Thread(target=task, args=("B", 1))

    # 启动线程，调用函数
    t1.start()
    t2.start()

    # join()：主线程阻塞，等待子线程执行完成再往下走
    t1.join()
    t2.join()
    print("所有子线程执行完成，主线程退出")
```

运行结果：B 先执行完毕，A 后结束，证明线程并发执行。

### 方式 2：类继承 Thread（适合复杂任务，需维护状态）

重写`run()`方法，线程启动自动执行 run：

```python
import threading
import time

class MyThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()  # 必须调用父类构造
        self.name = name
        self.delay = delay

    def run(self):
        # 线程核心逻辑，start()自动调用
        print(f"线程 {self.name} 启动")
        time.sleep(self.delay)
        print(f"线程 {self.name} 结束")

if __name__ == "__main__":
    t1 = MyThread("线程1", 1)
    t2 = MyThread("线程2", 2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("程序结束")
```

## 主线程、守护线程 daemon

###  非守护线程（默认）

主线程会等待所有子线程全部执行完，才退出程序。

### 守护线程 daemon=True

主线程退出时，守护线程直接被杀死，不会等待其完成。

适用：日志后台打印、心跳检测、定时巡检。

```python
import threading
import time

def daemon_task():
    while True:
        print("守护线程运行中...")
        time.sleep(1)

def normal_task():
    time.sleep(3)
    print("普通子线程结束")

if __name__ == "__main__":
    t1 = threading.Thread(target=daemon_task, daemon=True)
    t2 = threading.Thread(target=normal_task)

    t1.start()
    t2.start()

    t2.join()  # 等待普通线程3秒结束
    print("主线程执行完毕，守护线程直接销毁")
```

运行逻辑：3 秒后普通线程结束，主线程退出，无限循环的守护线程直接终止。

> 注意：`daemon`必须在`start()`前设置，启动后修改无效。

## 线程常用属性与方法

|         方法 / 属性          |                      作用                      |
| :--------------------------: | :--------------------------------------------: |
|          `start()`           |             启动线程，调用 run ()              |
|           `run()`            |                线程执行逻辑入口                |
|     `join(timeout=None)`     | 阻塞主线程等待子线程，timeout 设置最大等待秒数 |
|         `is_alive()`         |        返回布尔值，判断线程是否正在运行        |
|     `getName()` / `name`     |              获取 / 设置线程名称               |
| `threading.current_thread()` |              获取当前运行线程对象              |
|   `threading.enumerate()`    |            返回当前所有存活线程列表            |
|  `threading.active_count()`  |              获取当前活跃线程总数              |

示例：线程状态监控

```python
import threading
import time

def test():
    time.sleep(2)

t = threading.Thread(target=test)
print("启动前是否活跃：", t.is_alive())
t.start()
print("启动后是否活跃：", t.is_alive())
print("当前线程名：", threading.current_thread().name)
print("活跃线程数量：", threading.active_count())
t.join()
print("结束后是否活跃：", t.is_alive())
```

##  线程竞争问题（脏数据）

多线程同时修改全局变量会出现数据错乱：

```python
import threading

num = 0

def add():
    global num
    for _ in range(100000):
        num += 1

if __name__ == "__main__":
    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=add)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("预期200000，实际结果：", num)
```

输出一定小于 200000，原因：`num +=1`分为「取值 + 计算 + 赋值」三步，线程切换打断操作。

## 互斥锁 Lock（最常用）

同一时间仅一个线程获取锁，保证代码块原子操作。

方法：

- `lock.acquire(blocking=True)`：获取锁，阻塞等待
- `lock.release()`：释放锁
- 推荐 `with lock:` 自动释放，避免死锁

修复上面计数错误案例：

```python
import threading

num = 0
lock = threading.Lock()  # 创建互斥锁

def add():
    global num
    for _ in range(100000):
        # 自动加锁，代码块结束自动释放
        with lock:
            num += 1

if __name__ == "__main__":
    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=add)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("正确结果：", num) # 固定输出200000
```

## 可重入锁 RLock

普通 Lock 同一线程重复 acquire 会**死锁**，RLock 支持同一线程多次加锁，需要同等次数释放：

```python
import threading

rlock = threading.RLock()

def func():
    rlock.acquire()
    print("第一次加锁")
    rlock.acquire()
    print("同一线程二次加锁，不会阻塞")
    rlock.release()
    rlock.release()

t = threading.Thread(target=func)
t.start()
t.join()
```

## 死锁产生与规避

### 死锁场景

**加锁未解锁**

``` python
'''
演示死锁场景
'''
import threading
lock = threading.Lock()
num = 0
# 加锁未解锁
def add():
    print(f'当前线程: {threading.current_thread().name} 执行任务add')
    lock.acquire()
    print(f'当前线程: {threading.current_thread().name}, 加锁成功!')
    global num
    num += 1
    print(f'当前线程: {threading.current_thread().name}, 线程结束')

if __name__ == '__main__':
    threading.Thread(target=add).start()
    threading.Thread(target=add).start()

```



**对一个互斥锁重复加锁**

``` python
'''
演示死锁场景
'''
import threading
lock = threading.Lock()
num = 0

def add_():
    lock.acquire()
    global num
    num += 1
    lock.release()

# 嵌套加锁
def add():
    print(f'当前线程: {threading.current_thread().name} 执行任务add')
    lock.acquire()
    print(f'当前线程: {threading.current_thread().name}, 加锁成功!')
    global num
    num += 1
    add_()
    print(f'当前线程: {threading.current_thread().name}, 线程结束')
    lock.release()

if __name__ == '__main__':
    threading.Thread(target=add).start()
    threading.Thread(target=add).start()

```



**两个线程互相持有对方需要的锁，无限等待**：

```python
'''
演示死锁场景
'''
import threading
import time

lock1 = threading.Lock()
lock2 = threading.Lock()
num = 0

def task1():
    lock1.acquire()
    print(f'线程1持有lock1...')
    time.sleep(1)
    lock2.acquire()
    print(f'线程1持有lock2...')
    global num
    num += 1
    lock2.release()
    print(f'线程1释放lock2...')
    lock1.release()
    print(f'线程1释放lock1...')

def task2():
    lock2.acquire()
    print(f'线程2持有lock2...')
    time.sleep(1)
    lock1.acquire()
    print(f'线程2持有lock1...')
    global num
    num += 1
    lock1.release()
    print(f'线程2释放lock1...')
    lock2.release()
    print(f'线程2释放lock2...')



if __name__ == '__main__':
    threading.Thread(target=task1).start()
    threading.Thread(target=task2).start()

```



### 规避方案

1. 统一所有线程获取锁的顺序；
2. 设置 acquire 超时 `lock.acquire(timeout=3)`；
3. 减少嵌套锁；
4. 使用 RLock 替代普通 Lock。

# 五、线程同步工具（高级）

## 信号量 Semaphore：限制最大并发线程

控制同时运行线程数量，例如限制爬虫并发数：

```python
import threading
import time
# 最多同时3个线程运行
sem = threading.Semaphore(3)
# 定义爬虫函数
def crawl(url):
    # 通过with语法将被sem控制的逻辑写入with下面
    with sem:
        print(f'正在爬取 {url}, 线程: {threading.current_thread().name}')
        time.sleep(2)
        print(f'爬取完成 {url}')

if __name__ == '__main__':
    urls = ['https://www.baidu.com/',
            'https://www.zhihu.com/',
            'https://www.yahoo.com/',
            'https://www.sogou.com/',
            'https://www.jianshu.com/',
            'https://llfc.club/',
            'https://gitbookcpp.llfc.club/',
            'https://www.yuque.com/lianlianfengchen-cvvh2',
            'https://www.limerence2017.com/'
            ]
    thread_list = []
    for url in urls:
        t = threading.Thread(target=crawl, args=(url,))
        thread_list.append(t)
        # 子线程启动
        t.start()

    for t in thread_list:
        # 主线程等待子线程退出
        t.join()
```

## 5.2 事件 Event：线程间通知机制

核心方法：

- `event.set()`：设置标志为 True，唤醒等待线程
- `event.wait(timeout)`：阻塞等待标志为 True
- `event.clear()`：重置标志为 False

生产者 - 等待通知案例：

```python
import threading
import time

event = threading.Event()

def wait_task():
    print("子线程等待信号...")
    event.wait() # 阻塞，直到set()
    print("收到信号，开始执行任务")

def send_signal():
    time.sleep(3)
    print("发送通知信号")
    event.set()

t1 = threading.Thread(target=wait_task)
t2 = threading.Thread(target=send_signal)
t1.start()
t2.start()
t1.join()
t2.join()
```

## 5.3 条件变量 Condition：复杂生产消费模型

### 网络服务架构

![image-20260722091523971](https://cdn.llfc.club/image-20260722091523971.png)



结合锁 + 事件，用于「满足条件才执行」场景：

核心 API：`wait()` / `notify()` / `notify_all()`

```python
import threading
import time

cond = threading.Condition()
goods = 0
max_goods = 5

# 生产者
def producer():
    global goods
    while True:
        with cond:
            if goods >= max_goods:
                print("仓库满，生产者等待")
                cond.wait()
            goods += 1
            print(f"生产1件，库存：{goods}")
            cond.notify_all() # 唤醒消费者
        time.sleep(0.5)

# 消费者
def consumer():
    global goods
    while True:
        with cond:
            if goods <= 0:
                print("仓库空，消费者等待")
                cond.wait()
            goods -= 1
            print(f"消费1件，库存：{goods}")
            cond.notify_all() # 唤醒生产者
        time.sleep(1)

t_p = threading.Thread(target=producer, daemon=True)
t_c = threading.Thread(target=consumer, daemon=True)
t_p.start()
t_c.start()
time.sleep(10)
print("程序结束")
```

# 六、线程池 ThreadPoolExecutor（工程开发首选）

手动创建大量线程开销大、难管理，`concurrent.futures.ThreadPoolExecutor` 内置线程池，自动复用线程。

## 6.1 submit () 提交单个任务（返回 Future 对象）

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(num):
    print(f"任务{num}开始")
    time.sleep(1)
    return f"任务{num}完成"

if __name__ == "__main__":
    # max_workers：线程池最大并发数
    with ThreadPoolExecutor(max_workers=4) as pool:
        # 提交任务，返回Future
        futures = [pool.submit(task, i) for i in range(6)]
        # 获取结果
        for f in futures:
            print(f.result())
```

## 6.2 map () 批量处理迭代数据（简化循环）

```python
from concurrent.futures import ThreadPoolExecutor
import time

def calc(x):
    time.sleep(1)
    return x * x

if __name__ == "__main__":
    data = [1,2,3,4,5]
    with ThreadPoolExecutor(3) as pool:
        # 自动分配线程，结果顺序和输入一致
        res = pool.map(calc, data)
        print(list(res))
```

## 6.3 异常捕获 + 任务超时

Future.result (timeout = 秒数) 超时抛 TimeoutError

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

def err_task():
    time.sleep(2)
    raise ValueError("任务内部报错")

with ThreadPoolExecutor(2) as pool:
    f = pool.submit(err_task)
    try:
        res = f.result(timeout=1)
    except TimeoutError:
        print("任务执行超时")
    except Exception as e:
        print("任务异常：", e)
```

## 6.4 等待全部 / 任意任务完成

- `wait(futures, return_when=ALL_COMPLETED)`：等待所有任务结束
- `wait(futures, return_when=FIRST_COMPLETED)`：任一任务完成立即返回

```python
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED,FIRST_COMPLETED
import time

def work(x):
    time.sleep(1)
    return x

if __name__ == '__main__':
    with ThreadPoolExecutor(3) as pool:
        # 返回的futures队列
        fs = [pool.submit(work,i) for i in range(1,6)]
        # # 等待futures结果，也就是任务完成，这里只要第一个任务完成就返回
        # done, pending = wait(fs,return_when=FIRST_COMPLETED)
        # # 只要第一个任务完成返回，就可以获取结果
        # print('最先完成任务结果: ', [d.result() for d in done])

        # 等待futures结果，也就是任务完成，这里所有任务完成就返回
        done, pending = wait(fs, return_when=ALL_COMPLETED)
        # 只要第一个任务完成返回，就可以获取结果
        print('所有任务结果: ', [d.result() for d in done])
```

# 七、线程本地存储 threading.local ()

多线程共用全局变量会竞争，`local` 为每个线程创建独立私有变量，互不干扰：

```python
import threading

local_data = threading.local()

def func(name):
    # 每个线程独立存储value
    local_data.value = name
    print(f"线程{name}：{local_data.value}")

t1 = threading.Thread(target=func, args=("A",))
t2 = threading.Thread(target=func, args=("B",))
t1.start()
t2.start()
```

# 八、常见问题总结

## 1. 什么时候用线程？什么时候用进程？

- IO 密集（爬虫、接口、文件、数据库）：`threading` / `ThreadPoolExecutor`
- CPU 密集（矩阵计算、大数据运算）：`multiprocessing` 多进程

## 2. GIL 会完全废掉多线程吗？

不会，IO 阻塞场景 GIL 释放，多线程依然大幅提升效率；仅纯 CPU 循环无加速。

## 3. 锁使用规范

1. 尽量用`with lock:`自动释放，避免遗漏 release；
2. 缩短锁内部代码，减少线程等待；
3. 复杂嵌套锁使用 RLock；
4. 统一锁获取顺序防止死锁。

## 4. 守护线程使用注意

守护线程不能执行文件、数据库落盘操作，主线程退出会强制杀死，数据丢失。

## 5. 线程池最佳实践

生产环境禁止手动无限创建 Thread，统一使用 ThreadPoolExecutor 设置合理 max_workers（IO 任务可设大一点，CPU 任务不宜过大）。

# 九、完整实战案例：多线程爬虫简易框架

```python
from concurrent.futures import ThreadPoolExecutor
import requests

# 限制并发5
MAX_WORKER = 5
headers = {"User-Agent": "Mozilla/5.0"}

def fetch(url):
    try:
        resp = requests.get(url, headers=headers, timeout=3)
        return f"{url} 状态码：{resp.status_code}"
    except Exception as e:
        return f"{url} 请求失败：{str(e)}"

if __name__ == "__main__":
    url_list = [
        "https://llfc.club",
        "https://www.yuque.com/lianlianfengchen-cvvh2",
        "https://gitbookcpp.llfc.club/",
		"https://www.limerence2017.com/"
    ]
    with ThreadPoolExecutor(max_workers=MAX_WORKER) as pool:
        results = pool.map(fetch, url_list)
    for ret in results:
        print(ret)
```