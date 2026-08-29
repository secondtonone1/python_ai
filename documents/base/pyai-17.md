---
title: Python进阶之协程
date: 2026-07-28 15:24:08
tags: [python,AI]
categories: [python,AI]
---

# Python进阶之协程

---

## 协程基础概念

### 1\. 进程、线程、协程三者层级关系

从上至下资源粒度越来越小，切换开销依次降低：

**1\. 进程**：操作系统资源分配最小单位，内存、CPU资源完全隔离，进程间通信代价极高；

**2\. 线程**：进程内部执行单元，共享进程堆内存，由操作系统内核调度，切换存在上下文开销；多线程存在资源竞争，需要锁保证数据安全；

**3\. 协程**：单线程内的微型执行单元，别称**微线程、纤程**，属于**用户态调度**，完全由代码逻辑主动切换，不经过操作系统内核，切换开销几乎可以忽略不计。

**核心关系**：

一个进程可以包含多个线程；一个线程内部可以运行数万、十万个协程。

### 2\. 适用场景

**推荐使用：IO密集型任务**

大规模网络爬虫、调用第三方接口、MySQL/Redis异步读写、FastAPI异步Web服务、消息队列异步消费。

**禁止使用：CPU密集型数值运算**

协程绑定单线程，无法利用多核CPU并行计算；大数据运算、矩阵计算请使用 `multiprocessing` 多进程。

### 3\. 重温GIL全局解释器锁（协程性能优势根源）

CPython解释器自带GIL锁铁则：

1\. 同一时刻，单个CPU核心只能执行1条线程的字节码；

2\. 线程触发IO阻塞时，会主动释放GIL锁；CPU时间片耗尽，系统强制切换线程抢夺GIL；

**衍生结论**：

1\. 多线程无法加速CPU计算任务；

2\. IO场景多线程可以并发，但并发量上万时，操作系统频繁切换线程，性能急剧下降；

3\. **协程运行在单线程中，全程不存在GIL来回切换损耗，超高并发场景性能碾压多线程**。

---

## Python协程三代语法演进

Python协程历经三次迭代，语法逐步规范化：

**1\. 第一代：yield生成器模拟协程（Python2 \~ 3\.3）**

借助生成器`yield`暂停函数、`send()`唤醒函数模拟任务切换；

缺点：语法怪异、不支持多层嵌套、无统一IO调度器，早已被淘汰。

**2\. 第二代：@asyncio\.coroutine \+ yield from（Python3\.4）**

官方推出标准库 `asyncio`，内置事件循环调度器；依旧基于生成器封装，语法冗余晦涩。

**3\. 第三代：async / await 专属语法（Python3\.5\+ 至今通用）**

Python官方专为异步协程设计关键字，语法简洁统一，主流异步框架（aiohttp、FastAPI、aiomysql）全部基于这套语法开发，本节课全部内容以此为准。

---

## 协程两大核心关键字

![image-20260728161511497](https://cdn.llfc.club/image-20260728161511497.png)

###  async def：定义协程函数

**重中之重结论**：

调用 `async def` 修饰的函数，**不会执行函数内部任何代码**，仅仅创建一个协程对象；协程对象无法独立运行，必须提交给**事件循环 EventLoop** 调度执行。

```python
import asyncio

# 定义标准协程函数
async def hello_coroutine():
    print("协程内部代码被执行了")

# 调用协程函数：仅生成协程实例，无打印输出
coro = hello_coroutine()
print(type(coro))  # <class 'coroutine'>
```

### await：让出线程执行权，等待异步IO完成

**作用**

当前协程遇到IO阻塞（网络等待、数据库等待）时，主动暂停执行，把线程使用权交还给事件循环；事件循环调度其他就绪协程运行；等到IO操作完成后，再切回当前协程继续向下执行，并接收异步返回结果。

**强制语法规则（高频易错考点）**

1\. `await` 只能写在 `async def` 定义的协程函数内部，普通函数中使用直接抛出语法错误；

2\. `await` 后方只能跟随**可等待对象**：协程Coroutine、任务Task、底层Future；数字、字符串、普通同步函数均不能被await修饰。

**基础延时IO演示**：

```python
import asyncio

async def sleep_demo():
    print("开始异步等待2秒模拟IO阻塞")
    # 异步休眠：替代同步time.sleep()，不会卡死线程
    await asyncio.sleep(2)
    print("2秒IO等待结束，恢复协程执行")

# 启动事件循环，运行顶层协程
asyncio.run(sleep_demo())
```

---

## 事件循环 EventLoop：协程调度总指挥

事件循环是整个异步程序的核心调度中枢，所有协程都由它统一管理，核心工作流程：

1\. 接收开发者提交的所有协程、任务；

2\. 遍历所有任务，发现某个协程触发IO阻塞，立刻切换其他可运行协程；

3\. IO请求响应完毕后，唤醒对应协程继续执行；

4\. 所有任务执行完毕，关闭循环释放资源。

### 三种事件循环启动方式

**1\. Python3\.7\+ 推荐：asyncio\.run\(\)【日常开发首选】**

自动创建事件循环、执行任务、程序结束自动销毁循环，一行代码搞定，无需手动管理生命周期。

**2\. 底层原生写法（仅理解原理，项目中不用）**

```python
import asyncio

loop = asyncio.get_event_loop()
loop.run_until_complete(sleep_demo())
loop.close()
```

---

## 多协程并发执行两种主流写法

逐个串行await多个协程是顺序执行，无法发挥异步并发能力；实现并发两种标准方案：

### 方式1：asyncio\.create\_task\(\) 逐个创建任务（3\.7\+推荐）

![image-20260728163736992](https://cdn.llfc.club/image-20260728163736992.png)

将协程封装为Task任务，创建瞬间直接加入事件循环调度队列，多个任务并行执行。

**耗时对比案例**：

```python
import asyncio
import time

async def sleep_demo():
    print('开始异步等待2秒模拟IO阻塞')
    # 异步休眠，替代time.sleep(),在异步函数中使用同步阻塞会导致卡死线程
    await asyncio.sleep(2)
    print('2秒后IO等待结束，恢复协程执行')

def dm01():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sleep_demo())
    loop.close()

async def task(name, delay):
    print(f'任务{name} 启动, 需要等待 {delay} s')
    await asyncio.sleep(delay)
    print(f'任务{name} 执行完毕')
    return f'{name} 执行结果'

async def main():
    start_time = time.time()
    # 创建两个任务，并发执行，此刻并没有执行，只是将任务放到任务队列中
    t1 = asyncio.create_task(task('A',5))
    t2 = asyncio.create_task(task('B',2))

    # 主线程等待两个任务全部执行结束，接受返回值
    # 起始在这里才算做等待执行，主协程main让出cpu控制权，事件循环调度其他协程
    res1 = await t1
    res2 = await t2

    total_time = time.time()-start_time
    print(f'\n总耗时: {total_time:.2f} s')
    print(res1,res2)


def dm02():
    asyncio.run(main())


if __name__ == '__main__':
    # dm01()
    dm02()
```

**运行结果解读**：

串行执行总耗时需要 2\+3=5s；并发运行仅耗时≈3s，IO等待时间完全重叠。

### 方式2：asyncio\.gather\(\) 批量并发（爬虫批量请求最常用）

一次性接收任意数量协程，统一并发调度；等待所有任务执行完毕，返回结果列表，**结果顺序和传入协程顺序严格一致**。

```python
async def gather_main():
    start = time.time()
    # 打包所有协程，等待他们都执行结束
    result_list = await asyncio.gather(
        task('A', 2),
        task('B', 3),
        task('C', 1),
    )
    print(f'所有任务返回结果: ', result_list)
    print(f'总耗时: {time.time() - start:.2f} s')

 # 启动事件循环，调用gather main协程
asyncio.run(gather_main())
```

**补充：asyncio\.wait\(\)**

灵活性更高，会将任务划分为「已完成任务集合、未完成任务集合」，适合自定义分批执行、按需获取结果场景，入门阶段了解即可。



## 易错点补充直接等待协程对象

``` python
async def async_seq_main():
    # 也可不包裹成任务 直接等待协程执行结束
    t1 = task('C', 3)
    t2 = task('D', 5)
    # 相当于串行
    res3 = await t1
    res4 = await t2
    
asyncio.run(async_seq_main())
```

**核心区别一句话**

1. **`asyncio.create_task(协程)`：把协程打包成 Task 丢进事件循环队列，提前就绪排队，两个任务全程并发运行，总耗时 = 耗时最长的那个任务时间（5s）**
2. **直接 `await 协程对象`：协程不会提前入队，必须等到执行这行 await 才会启动，串行依次执行，总耗时 = 两个任务时间相加（5+3=8s）**

---

## 协程三大核心对象详解

**1\. Coroutine 协程对象**

`async def()` 调用生成的原始协程，无法被事件循环单独调度，必须封装为Task；

**2\. Task 任务对象**

继承自Future，协程的可调度载体，支持取消任务、判断运行状态、获取返回值；

**3\. Future 对象**

异步最底层抽象，代表一个未来会返回结果的异步操作，业务开发几乎不会直接实例化使用。

### 实操：取消正在运行的协程任务

```python
import asyncio

async def task(name, delay):
    print(f'任务{name} 启动, 需要等待 {delay} s')
    await asyncio.sleep(delay)
    print(f'任务{name} 执行完毕')
    return f'{name} 执行结果'

async def main():
    # 创建耗时5s的长任务
    t = asyncio.create_task(task('耗时任务',5))
    # 等待1s后取消任务
    await asyncio.sleep(1)
    # 取消协程t的任务
    t.cancel()
    try:
        # 执行任务会报错
        await t
    except asyncio.CancelledError:
        print('协程任务已被手动取消')

asyncio.run(main())
```

## 时序分步走

1. 进入 `main()`
2. 执行：

```python
t = asyncio.create_task(task('耗时任务',5))
```

- 仅仅：把 `task` 协程打包成 Task，扔进事件循环就绪队列；
- **此刻不会执行 task 内部代码**。

1. 执行下一行：

   ```python
   await asyncio.sleep(1)
   ```

   关键点来了`await`会让主协程 `main`

    主动挂起、交出事件循环控制权。

   事件循环无事可做，就会去调度队列里已经就绪的 `t`

    任务，开始运行 `task`

    函数内部代码：

```plaintext
任务耗时任务 启动, 需要等待 5 s
```

紧接着执行 `await asyncio.sleep(5)`：

子协程又挂起休眠 5 秒，把控制权交还事件循环。

1. 时间流逝 1 秒 之后：

   main 的 `sleep(1)` 休眠结束，主协程被唤醒，继续向下执行 `t.cancel()`

   给这个任务打上**取消标记**，但此时任务还处在休眠挂起状态，不会立刻抛出异常。

2. 执行 `await t`

   尝试等待这个被标记取消的任务完成：

   当事件循环切换到该协程时，检测到取消标记，立即抛出 `asyncio.CancelledError` 异常。

   异常被 try-except 捕获，打印：协程任务已被手动取消。

---

## asyncio常用工具API对照表

| 方法 / 属性                       | 功能说明                           |
| --------------------------------- | ---------------------------------- |
| `asyncio.run(coro)`               | 顶层入口，启动事件循环运行协程     |
| `asyncio.create_task(coro)`       | 创建Task并发任务，加入循环调度     |
| `asyncio.gather(*coros)`          | 批量并发执行协程，收集全部返回结果 |
| `asyncio.wait_for(coro, timeout)` | 设置协程最大超时时间，超时自动终止 |
| `task.cancel()`                   | 取消正在运行的异步任务             |
| `task.done()`                     | 布尔值，判断任务是否执行完毕       |
| `task.result()`                   | 获取任务最终返回结果               |
| `asyncio.current_task()`          | 获取当前正在运行的任务实例         |

### wait\_for：协程超时控制（爬虫必备）

防止网络请求卡死程序，给每个异步任务设置最大等待时长：

```python
'''
演示等待超时任务
'''

import asyncio
import time


async def long_work(name):
    await asyncio.sleep(2)
    return f'{name}任务执行完成'

async def main():
    try:
        start = time.time()
        # 本质上如果wait_for等待的是协程对象而不是task，就会按照串行执行
        # 最多等待3s,超时抛出TimeError
        res = await  asyncio.wait_for(long_work('A'), timeout=3)
        print('res:', res)
        res2 = await asyncio.wait_for(long_work('B'), timeout=3)
        print('res2:', res2)
    except asyncio.TimeoutError:
        print('任务执行超时,强制终止')
    finally:
        end = time.time()
        print(f'程序总计耗时{end-start}s')

if __name__ == '__main__':
    asyncio.run(main())
```

### 协程异常捕获两种场景

1\. 单个协程异常：`try-except` 包裹await语句即可捕获；

2\. gather批量任务异常：添加参数 `return_exceptions=True`，异常不会终止整体程序，异常对象会存入结果列表。

```python
async def error_task():
    await asyncio.sleep(1)
    raise ValueError("协程内部业务报错")

async def main():
    results = await asyncio.gather(
        task("正常任务", 1),
        error_task(),
        return_exceptions=True
    )
    print(results)

asyncio.run(main())
```

---

## 异步上下文管理器 async with

异步资源（异步HTTP会话、异步数据库连接、异步文件读写句柄）需要自动创建、自动释放资源，使用 `async with` 语法，对标同步代码的 `with` 语句，爬虫、数据库开发高频使用。

**基础语法格式**：

```python
async def demo():
    # 申请异步资源
    async with 异步资源实例 as obj:
        # 执行异步业务逻辑
        pass
    # 代码块执行完毕，自动关闭释放资源
```

---

## 协程天然无锁：不存在线程竞争、脏数据、死锁

协程全程运行在**单线程内部**，代码执行流转完全可控，只有遇到`await`才会切换任务，不会像多线程一样被操作系统随机抢占执行权：

1\. 无需使用 Lock、RLock 互斥锁；

2\. 全局变量累加修改永远不会出现脏数据；

3\. 完全不存在死锁问题。

**计数器验证案例**：

```python
import asyncio

num = 0
'''
验证，同一个线程中多个协程是并发安全的，
因为同一个线程中，多个协程在同一个时刻，
仅有一个协程执行。
'''
async def add_count():
    global num
    for  _ in range(100000):
        num += 1

async def main():
    t1 = asyncio.create_task(add_count())
    t2 = asyncio.create_task(add_count())

    await t1
    await t2

    print('最终累加结果: ', num)

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 并发限流：Semaphore 信号量

和线程信号量作用完全一致，限制同一时刻最大并发协程数量，爬虫场景用来控制请求频率，避免IP被网站封禁。

```python
import asyncio
import aiohttp

# 限定最大并发协程数：3
sem = asyncio.Semaphore(3)

async def crawl_page(session, url):
    # 占用一个并发席位，超出数量则阻塞等待
    async with sem:
        async with session.get(url) as resp:
            html = await resp.text()
            print(f"{url} 页面字节大小：{len(html)}")

async def main():
    async with aiohttp.ClientSession() as session:
        # 8个相同链接，最多同时3个并发请求
        url_list = ["https://www.baidu.com"] * 8
        tasks = [crawl_page(session, url) for url in url_list]
        await asyncio.gather(*tasks)

asyncio.run(main())
```

---

## 协程间通信：Event 事件通知

用于协程之间等待信号、触发执行，API设计和线程Event完全对齐：

\- `event.set()`：将标志位设为True，唤醒所有阻塞等待的协程

\- `event.wait(timeout)`：协程阻塞等待标志位被激活

\- `event.clear()`：重置标志位为False



**协程同步和等待案例**

```python
import asyncio

event = asyncio.Event()

# 等待信号的协程
async def wait_event_task():
    print("协程正在等待唤醒信号...")
    await event.wait()
    print("收到信号，开始执行业务逻辑")

# 发送信号的协程
async def send_event_signal():
    await asyncio.sleep(3)
    print("3秒倒计时结束，发送唤醒信号")
    event.set()

async def main():
    t1 = asyncio.create_task(wait_event_task())
    t2 = asyncio.create_task(send_event_signal())
    await t1
    await t2

asyncio.run(main())
```

---

## 协程高频踩坑清单（直播重点强调）

**1\.  禁止在协程内部调用同步阻塞代码**

同步阻塞API会直接卡死整个事件循环，所有协程全部停滞

替换对照表：

`time.sleep()` → `asyncio.sleep()`

`requests` 同步请求 → `aiohttp` 异步请求

`pymysql` 同步数据库 → `aiomysql` 异步数据库

**`awaitasync def`****2\.  关键字不能脱离 函数使用；**

**3\. CPU密集计算场景不要使用协程，优先选择多进程；**

**4\. 海量任务必须使用Semaphore限流，无限创建Task会造成并发爆炸被封IP；**

**5\. 异步项目需要全程使用异步生态库，混用同步代码是80%异步BUG的根源。**



## 核心原理

协程基于**单线程异步调度**，无需加锁就能安全完成生产者、消费者交替工作，核心依靠 `asyncio` 库 + 异步队列 `asyncio.Queue`（线程安全的异步缓冲区）。

1. **生产者协程**：持续生产数据，放入队列；队列满了自动挂起等待消费者取走数据
2. **消费者协程**：不断从队列取出数据消费；队列为空自动挂起等待生产者写入
3. `asyncio.Queue` 自带阻塞机制，天然解决线程安全问题，不需要 `threading.Lock`



## 版本 1：基础最简版（固定生产总量）

```python
import asyncio

# 异步队列：存放生产的数据，设置最大容量3（缓冲区大小）
queue = asyncio.Queue(maxsize=3)

# 生产者协程
async def producer():
    for i in range(6):  # 一共生产6个商品
        item = f"商品-{i}"
        # 队列满时，此处会自动暂停协程，让出事件循环
        await queue.put(item)
        print(f" 生产者：生产 {item}，当前队列大小：{queue.qsize()}")
        await asyncio.sleep(0.5)  # 模拟生产耗时

# 消费者协程
async def consumer():
    while True:
        # 队列为空时，协程阻塞等待数据
        item = await queue.get()
        print(f" 消费者：消费 {item}，剩余队列：{queue.qsize()}")
        await asyncio.sleep(1)  # 模拟消费耗时
        queue.task_done()  # 标记一个任务消费完成

async def main():
    # 创建生产者、消费者任务
    prod_task = asyncio.create_task(producer())
    cons_task = asyncio.create_task(consumer())

    # 等待生产者全部生产完毕
    await prod_task
    # 等待队列里所有剩余商品全部被消费完
    await queue.join()
    # 取消无限循环的消费者任务
    cons_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
```

### 运行逻辑说明

- 队列最大 3 个位置，生产者生产 3 个后就会暂停，等消费者取走才能继续生产
- 消费者消费速度比生产者慢，队列会反复填满、消耗
- 全部生产 + 消费结束后关闭消费者

## 版本 2：多生产者 + 多消费者（工程常用）

多个生产者并行造货、多个消费者并行拿货，更贴合真实场景：

```python
import asyncio

queue = asyncio.Queue(maxsize=4)

# 单个生产者逻辑
async def producer(name, total):
    for i in range(total):
        item = f'{name}-货品{i}'
        await queue.put(item)
        print(f'【{name}】产出: {item} | 队列: {queue.qsize()}')
        await asyncio.sleep(0.4)

# 单个消费者逻辑
async def consumer(name):
    while True:
        item = await queue.get()
        print(f'【{name}取走: {item} | 队列: {queue.qsize()}】')
        await asyncio.sleep(0.8)
        # 每放入1个元素，就会产生一个未标记的计数
        # task_done就会将这个未标记的计数-1，
        # 将来queue.join可以阻塞等待所有计数标记，
        # 大白话相当于所有消费者将队列消费完成
        queue.task_done()

# 定义异步函数main()
async def main():
    # 2个生产者，各生产4件产品
    producers = [
        asyncio.create_task(producer('工厂A',4)),
        asyncio.create_task(producer('工厂B',4))
    ]

    # 3个消费者，并行消费
    consumers = [asyncio.create_task(consumer(f'顾客{i}')) for i in range(3)]
    # 等待所有生产者完工
    await asyncio.gather(*producers)
    # 等待消费者消费完成队列
    await queue.join()
    # 关闭所有的消费者,因为消费者是死循环
    for c in consumers:
        c.cancel()

if __name__ == '__main__':
    asyncio.run(main())
```

无限循环

``` python
import asyncio

queue = asyncio.Queue(maxsize=4)

# 生产者：死循环永久生产，不再限制总产量
async def producer(name: str):
    num = 0
    while True:
        item = f"{name}-货品{num}"
        await queue.put(item)
        print(f"【{name}】产出：{item} | 队列当前数量:{queue.qsize()}")
        num += 1
        await asyncio.sleep(0.4)  # 生产间隔

# 消费者：死循环持续消费
async def consumer(name: str):
    while True:
        item = await queue.get()
        print(f"     【{name}】取走：{item} | 队列剩余:{queue.qsize()}")
        await asyncio.sleep(0.8)  # 消费比生产慢，队列会逐步堆满
        queue.task_done()

async def main():
    # 2个永久生产者
    producers = [
        asyncio.create_task(producer("工厂A")),
        asyncio.create_task(producer("工厂B"))
    ]
    # 3个永久消费者
    consumers = [asyncio.create_task(consumer(f"顾客{i+1}")) for i in range(3)]

    try:
        # 整体程序最多运行 8 秒就超时退出
        await asyncio.wait_for(asyncio.Future(), timeout=8)
    except asyncio.TimeoutError:
        print("\n===== 运行时间结束，准备停止所有任务 =====")

    # 取消所有生产者、消费者无限循环任务
    for task in producers + consumers:
        task.cancel()

    # 等待所有任务正常取消完毕
    await asyncio.gather(*producers, *consumers, return_exceptions=True)
    print("所有生产消费任务已全部终止")

if __name__ == "__main__":
    asyncio.run(main())
```



---

## 完整实战项目：异步爬虫通用框架（对标多线程爬虫）

### 前置依赖安装

```bash
pip install aiohttp
```

### 可直接运行完整代码

```python
import aiohttp
import asyncio

# 全局配置
MAX_CONCURRENT = 5  # 最大并发数
sem = asyncio.Semaphore(MAX_CONCURRENT)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
TIMEOUT = aiohttp.ClientTimeout(total=3)  # 请求超时3秒

async def fetch_url(session: aiohttp.ClientSession, url: str):
    """单个网页异步请求函数"""
    async with sem:
        try:
            async with session.get(url, headers=headers, timeout=TIMEOUT) as resp:
                page_html = await resp.text()
                return f"✅ {url} | 状态码:{resp.status} | 页面长度:{len(page_html)}"
        except Exception as e:
            return f"❌ {url} | 请求失败: {str(e)}"

async def main():
    # 待爬取链接列表
    url_list = [
        "https://llfc.club",
        "https://www.baidu.com",
        "https://www.bing.com",
        "https://www.qq.com",
        "https://www.zhihu.com",
        "https://www.163.com"
    ]
    # 全局复用ClientSession，性能远高于频繁创建会话
    async with aiohttp.ClientSession() as session:
        task_list = [fetch_url(session, url) for url in url_list]
        result_list = await asyncio.gather(*task_list)
    # 遍历打印所有爬取结果
    for res in result_list:
        print(res)

if __name__ == "__main__":
    asyncio.run(main())
```



## 知识点总结答疑

### IO并发三种方案选型对比

| 方案                  | 适用场景                       | 并发上限        | 优缺点                       |
| --------------------- | ------------------------------ | --------------- | ---------------------------- |
| threading多线程       | 中小规模IO任务                 | 数千            | 代码简单，上万并发性能下滑   |
| asyncio协程           | 海量高并发IO（爬虫、异步后端） | 十万级          | 开销极低，性能最优，无锁烦恼 |
| multiprocessing多进程 | CPU密集数值计算                | 取决于CPU核心数 | 利用多核算力，开销最大       |

### 线程与协程核心差异

1\. 调度主体：线程由操作系统内核调度；协程由用户代码事件循环调度；

2\. 切换开销：协程切换开销远小于线程；

3\. 锁机制：协程单线程运行无需加锁；多线程必须处理锁竞争、死锁；

4\. 并发上限：协程可轻松支持十万并发，线程上限仅有几千。

### 异步代码编写黄金规范

1\. 项目全程统一使用异步第三方库，杜绝同步、异步混用；

2\. 所有IO阻塞操作必须添加await；

3\. 批量任务一定要设置并发信号量限流；

4\. 所有网络请求统一配置超时时间，避免程序永久卡死。

---

## 课后作业

1\. **基础作业**：编写6个不同延时的协程并发执行，总耗时等于最长任务的等待时间；

2\. **进阶实战**：准备12个网页链接，使用Semaphore限制最大并发数为4，异步爬取全部页面并打印成功/失败结果。

