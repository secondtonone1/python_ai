---
title: Python进阶之进程
date: 2026-07-12 21:39:48
tags: [python,AI]
categories: [python,AI]
---

# 一、进程基础概念

##  进程 vs 程序 vs 线程

1. **程序**：磁盘上的静态二进制文件（`.py`/exe），无资源、不运行。
2. **进程**：程序加载到内存后**独立运行实例**，操作系统分配独立资源：
   - 独立内存空间、CPU 时间片、文件描述符、PID 进程号

   - 进程间默认内存隔离，无法直接共享变量
3. **线程**：进程内轻量级执行单元，**共享进程内存**，切换开销远小于进程。

<!-- more -->

![](https://cdn.llfc.club/image-20260712220534777.png)

##  进程核心特性

- **资源隔离**：每个进程拥有独立地址空间，一个进程崩溃不会影响其他进程；
- **多核利用**：Python GIL 锁限制单进程只能利用 1 个 CPU 核心，多进程可充分利用多核 CPU；
- **通信复杂**：进程内存隔离，必须通过管道、队列、共享内存、Socket 通信；
- **开销大**：创建 / 销毁进程比线程消耗更多内存、CPU。



##  适用场景

✅ CPU 密集型任务（矩阵运算、模型训练、加密、大规模计算），规避 GIL 锁瓶颈；
❌ IO 密集型任务（网络请求、文件读写）优先用多线程 / 协程，进程开销过大。



## 并行和并发

**并行概念**

![image-20260712221325701](https://cdn.llfc.club/image-20260712221325701.png)

不同的进程运行在不同的核心上，多个进程可以同时运行，互不影响。

同一时刻可以同时运行多个进程

**并发概念**

同一时刻只能运行一个进程

一个进程运行在一个cpu核心上，线程依附于进程运行，当一个进程开辟很多线程，这些线程运行在一个CPU核心上

![image-20260712222009294](https://cdn.llfc.club/image-20260712222009294.png)

##  Python 多进程标准库

`multiprocessing`：官方内置多进程库，Windows/Linux/macOS 跨平台兼容。

# 二、multiprocessing 核心组件

1. `Process`：基础进程类，创建自定义子进程；

2. `Pool`：进程池，批量管理进程，复用进程减少创建销毁开销；

3. `Queue`：进程安全队列，用于父子进程数据通信；

4. `Pipe`：管道，双向点对点进程通信；

5. `Manager`：创建跨进程共享变量（list/dict）；

6. `Lock`：进程锁，防止多进程并发修改共享数据产生脏数据。

---

# 三、完整代码案例（由浅入深）

## 案例 1：基础 Process 手动创建子进程（函数方式）

**关键注意：Windows 系统必须把进程启动代码放入 `if __name__ == '__main__':`，否则无限递归创建进程**

```python
import multiprocessing

import time

'''
进程运行需要执行任务，定义一个任务
'''
def task(name, delay):
    '''
    子进程执行函数
    :param name: 参数，接受子进程名字
    :param delay: 参数，接受延迟的时间s
    :return: None
    '''
    print(f'子进程 {name} 启动, PID: {multiprocessing.current_process().pid}')
    time.sleep(delay)
    print(f'子进程{name}执行完毕')

print(f'main函数外进程PID: {multiprocessing.current_process().pid}\n'
      f'__name__ : {__name__}')

if __name__ =='__main__':
    # 只有主进程能走入这里
    print(f'主进程PID：{multiprocessing.current_process().pid}')
    # 创建子进程
    p1 = multiprocessing.Process(target=task, args=('p1', 2))
    p2 = multiprocessing.Process(target=task, kwargs={
        'name':'p2',
        'delay':3,
    })
    # 启动子进程
    p1.start()
    p2.start()
    # 等待两个子进程
    p1.join()
    p2.join()
    print(f'主进程退出')
```

![image-20260712225443908](https://cdn.llfc.club/image-20260712225443908.png)

### 方法说明

- `start()`：创建操作系统真实进程，调用 target 函数；

- `join(timeout)`：阻塞等待子进程，timeout 为最长等待秒数；

- `terminate()`：强制杀死子进程（不推荐，资源无法释放）；

- `is_alive()`：判断进程是否还在运行。

## 案例 2：自定义 Process 类（面向对象写法）

继承`Process`，重写`run()`方法，逻辑封装性更强

```python
import multiprocessing
import time

class MyProcess(multiprocessing.Process):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay
    
    def run(self):
        # 进程启动后自动执行run方法
        print(f"自定义进程 {self.name} 启动 PID:{self.pid}")
        time.sleep(self.delay)
        print(f"自定义进程 {self.name} 结束")

if __name__ == '__main__':
    p = MyProcess("自定义进程C", 1.5)
    p.start()
    p.join()
    print("主进程结束")
```

## 案例 3：进程间通信 Queue（安全队列）

![image-20260716085023334](https://cdn.llfc.club/image-20260716085023334.png)

进程内存隔离，全局变量无法共享，使用`Queue`传递数据

```python
import multiprocessing
import time


def producer(q):
    '''
    生产者: 向队列写入数据
    :param q: 队列
    :return: None
    '''
    for i in range(10):
        q.put(f'数据{i}')
        print(f'生产者写入: 数据{i}')
        time.sleep(0.05)
    q.put('end')
    print('生产者进程结束')


def consumer(q):
    '''
    消费者从队列中获取数据
    :param q: 队列
    :return: None
    '''
    while True:
        # 队列为空则阻塞
        data = q.get()
        print(f'消费者读取: {data}')
        time.sleep(0.1)
        if data == 'end':
            break
    print('消费者进程结束')

if __name__ == '__main__':
    # 创建进程安全队列
    queue = multiprocessing.Queue(maxsize=10)
    # 创建生产者进程
    p_pro = multiprocessing.Process(target=producer, args=(queue,))
    # 创建消费者进程
    p_con = multiprocessing.Process(target=consumer, args=(queue,))
    # 启动两个进程
    p_pro.start()
    p_con.start()
    # 主进程等待生产者进程结束
    p_pro.join()
    p_con.join()
```

## 案例 4：进程池 Pool（批量处理任务，生产环境首选）

频繁创建销毁进程开销极大，进程池预先创建固定数量进程，重复利用

### 4\.1 map 批量同步执行

![image-20260716091017585](https://cdn.llfc.club/image-20260716091017585.png)

```python
import multiprocessing
import time

def calc_power(num):
    '''
    模拟CPU密集型任务
    :param num: 任务参数
    :return: num**2
    '''
    res = num ** 2
    time.sleep(0.3)
    print(f'计算 {num}² = {res}')
    return res

if __name__ == '__main__':
    # 获取CPU核心数，设置进程池大小
    core_count = multiprocessing.cpu_count()
    print(f'本机中CPU核心数为: {core_count}')

    # 创建进程池, 进程数=CPU核心数
    with multiprocessing.Pool(processes=core_count) as pool:
        '''
        map把要执行任务的函数和参数结合起来，交给进程池中的进程执行
        大白话: 进程池中的进程相当于水池中的鱼，任务参数相当于鱼饵，
        函数相当于吃这个动作
        '''
        data_list = [1,2,3,4,5,6,7,8,9,10]
        # map自动分配任务，阻塞等待全部任务完成，返回结果列表
        result = pool.map(calc_power, data_list)
    print(f'所有进程执行结果: {result}')
```

### 4\.2 apply\_async 异步非阻塞获取结果

```python
'''
演示进程池异步投递任务
'''
import multiprocessing
import time

def task(x):
    time.sleep(0.5)
    return x*10

if __name__ == '__main__':
    with multiprocessing.Pool(3) as pool:
        tasks = []
        for i in range(5):
            # 异步提交任务，不阻塞主进程
            # async_res是异步提交后的结果，不能直接获取任务执行的结果
            async_res = pool.apply_async(task, args=(i, ))
            # 将异步执行的结果状态放入tasks列表
            tasks.append(async_res)

        # 统一获取所有任务的返回值, res.get()会阻塞等待，直到任务执行完成
        final_results = [res.get() for res in tasks]
    print('异步任务执行结果: ', final_results)


```

## 案例 5：多进程共享数据 Manager + Lock

![image-20260716094208409](https://cdn.llfc.club/image-20260716094208409.png)

普通列表 / 字典无法跨进程共享，`Manager`创建托管对象，配合`Lock`防止并发修改冲突

```python
'''
演示进程操作共享空间
'''

import multiprocessing

def add_num(share_list, lock, num):
    '''
    将num放入列表share_list中
    :param share_list: 通过Manager()从共享空间中开辟的列表
    :param lock: 进程安全锁
    :param num: 任务数据放入列表中
    :return: None
    '''
    # 加锁 同一时间仅有一个进程修改共享数据
    lock.acquire()
    try:
        share_list.append(num)
    finally:
        lock.release()

if __name__ == '__main__':
    # 创建管理器
    manager = multiprocessing.Manager()
    # 创建跨进程共享列表
    share_data = manager.list()
    # 创建进程锁
    lock = multiprocessing.Lock()
    # 存储创建的子进程，将来主进程等待子进程执行完成
    p_list = []
    for i in range(5):
        p = multiprocessing.Process(target=add_num, args=(share_data, lock, i))
        p.start()
        p_list.append(p)

    # 等待所有子进程运行结束
    for p in p_list:
        p.join()

    print('最终共享列表:', share_data)
```

## 案例 6：Pipe 管道双向通信（点对点）

![image-20260716095849974](https://cdn.llfc.club/image-20260716095849974.png)

适合两个进程一对一数据传输，性能优于 Queue

```python
import  multiprocessing

def pipe_child(conn):
    '''
    子进程执行的函数
    :param conn: 孩子端
    :return: None
    '''
    # 子进程发送数据
    conn.send('子进程消息1')
    # 子进程从管道中读取信息，如果主进程没有发送消息，则阻塞
    print(f'子进程收到: {conn.recv()}')
    conn.close()

if __name__ == '__main__':
    # 创建管道, 返回两端连接对象
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=pipe_child, args=(child_conn,))
    p.start()

    # 主进程接受信息，如果子进程没有发送信息，则主进程阻塞
    print(f'主进程收到: {parent_conn.recv()}')
    parent_conn.send('主进程回复信息')
    p.join()
```

## 案例 7：CPU 密集型单进程 vs 多进程性能对比

直观体现多进程利用多核加速计算

```python
import multiprocessing
import time

def heavy_calc(n):
    s = 0
    for i in range(n):
        s += i ** 3
    return s

if __name__ == '__main__':
    task_data = [1000000] * 8

    # 单进程串行执行
    start = time.time()
    for data in task_data:
        heavy_calc(data)
    print(f"单进程耗时: {time.time() - start:.2f}s")

    # 多进程并行执行
    start = time.time()
    with multiprocessing.Pool() as pool:
        pool.map(heavy_calc, task_data)
    print(f"多进程耗时: {time.time() - start:.2f}s")
```

运行结果可见：多进程耗时接近单进程 1/CPU 核心数。

---

# 四、关键底层知识点

##  GIL 全局解释器锁（多进程核心优势来源）

- CPython 同一时刻只有 1 个线程执行 CPU 运算，GIL 锁导致单进程无法多核并行；

- 多进程每个子进程拥有独立 Python 解释器、独立 GIL 锁，真正多核并行计算。

## Windows / Linux 创建进程差异

1. **Linux**：`fork()`系统调用，复制父进程内存，速度快；

2. **Windows**：无 fork，使用`spawn`方式，导入主模块重建环境，**必须加****`if __name__ == '__main__'`**，否则递归创建进程卡死。

##  进程间通信方式对比

| 通信方式          | 适用场景         | 优点             | 缺点                   |
| ----------------- | ---------------- | ---------------- | ---------------------- |
| Queue             | 多生产者多消费者 | 进程安全、自带锁 | 性能一般               |
| Pipe              | 两两进程点对点   | 传输速度快       | 仅支持两端通信         |
| Manager 共享对象  | 需要读写共享变量 | 使用简单         | 性能损耗大             |
| 共享内存 RawArray | 海量数值传输     | 速度最快         | 无同步机制，需手动加锁 |

##  进程锁 Lock 作用

多进程同时修改共享数据会出现**数据竞争**（脏读、数据丢失），Lock 保证同一时间只有一个进程操作共享资源。

## 进程池常用参数

- `processes`：池内最大进程数量，推荐`multiprocessing.cpu_count()`；

- `maxtasksperchild`：每个进程最多执行任务数，到达后销毁重建，避免内存泄漏。

##  常见坑与避坑指南

1. ❌ 全局变量不能跨进程共享，必须用`Manager`/`Queue`；

2. ❌ Windows 忘记`if __name__ == '__main__'`，无限递归创建进程；

3. ❌ 不使用进程锁并发修改共享数据，结果错乱；

4. ❌ IO 密集任务盲目使用多进程，开销大于收益，改用`threading`；

5. ❌ 进程结束不调用`join()`，主进程提前退出导致子进程孤儿；

6. ❌ 大量小任务不用进程池，频繁`Process.start()`造成巨大性能损耗。

---

# 五、拓展进阶：共享内存 RawArray（高性能数值通信）

海量数字计算场景，Manager 性能不足时使用底层共享内存：

```python
import multiprocessing

def write_array(arr):
    for i in range(len(arr)):
        arr[i] = i * 2

if __name__ == '__main__':
    # 创建长度5的int类型共享数组
    share_arr = multiprocessing.RawArray('i', 5)
    p = multiprocessing.Process(target=write_array, args=(share_arr,))
    p.start()
    p.join()
    # 转换为普通列表打印
    print([x for x in share_arr])
```

---

# 六、生产级落地进程池模板

## 模板核心能力

- **异常隔离**：单个任务报错、崩溃不影响整体任务队列，统一捕获异常信息

- **超时防护**：单任务超时自动终止，避免进程卡死、程序阻塞

- **防内存泄漏**：定期重建子进程，杜绝长期运行内存堆积、溢出问题

- **自适应并发**：自动获取CPU核心数，适配设备性能，避免资源过载

- **通用性极强**：支持所有CPU密集型任务，无需重复改写底层逻辑

## 代码

```python
import multiprocessing
import traceback
from multiprocessing.pool import Pool

# ====================== 核心工具封装（无需修改） ======================
def single_task_safe_wrapper(func, *args, **kwargs):
    """
    任务安全包装器：隔离单个任务异常，防止整池崩溃
    :param func: 自定义任务函数
    :param args: 任务位置参数
    :param kwargs: 任务关键字参数
    :return: 任务结果/异常信息
    """
    try:
        result = func(*args, **kwargs)
        return {
            "status": "success",
            "data": result,
            "error": None
        }
    except Exception as e:
        return {
            "status": "fail",
            "data": None,
            "error": f"任务异常: {str(e)}",
            "traceback": traceback.format_exc()
        }

def create_production_pool(max_workers: int = None, max_task_per_child: int = 20):
    """
    创建生产级进程池
    :param max_workers: 最大并发进程数，默认自适应CPU核心数
    :param max_task_per_child: 单进程最大执行任务数，到期重建（防内存泄漏）
    :return: 进程池对象
    """
    # 自适应CPU核心数，避免资源耗尽
    if not max_workers:
        max_workers = multiprocessing.cpu_count()
    
    return Pool(processes=max_workers, maxtasksperchild=max_task_per_child)

def batch_run_tasks(task_func, task_params_list, timeout: int = 30):
    """
    批量并发执行多任务
    :param task_func: 业务任务函数
    :param task_params_list: 任务参数列表，每个元素为单任务参数
    :param timeout: 单任务最大超时时间(秒)
    :return: 全部任务结果列表
    """
    pool = create_production_pool()
    async_results = []

    # 异步批量提交任务
    for params in task_params_list:
        if isinstance(params, (list, tuple)):
            res = pool.apply_async(single_task_safe_wrapper, args=(task_func, *params))
        else:
            res = pool.apply_async(single_task_safe_wrapper, args=(task_func, params))
        async_results.append(res)
    
    # 等待并获取所有任务结果
    all_results = []
    for res in async_results:
        try:
            all_results.append(res.get(timeout=timeout))
        except multiprocessing.TimeoutError:
            all_results.append({
                "status": "timeout",
                "data": None,
                "error": f"任务超时(最大{timeout}s)",
                "traceback": None
            })
    
    # 关闭进程池，释放资源
    pool.close()
    pool.join()
    return all_results

# ====================== 业务层：自定义你的任务（仅需修改此处） ======================
def business_task(x):
    """
    自定义业务计算任务（用户可按需改写）
    支持数值计算、数据处理、模型推理等CPU密集操作
    """
    # 模拟重度CPU计算
    res = 0
    for i in range(1000000):
        res += i ** 2
    return x * res

# ====================== 程序入口（固定写法） ======================
if __name__ == '__main__':
    # 批量任务参数
    task_params = [1, 2, 3, 4, 5, 6, 7, 8]
    # 批量执行任务
    final_results = batch_run_tasks(business_task, task_params, timeout=20)

    # 结果统计与打印
    success_count = sum(1 for res in final_results if res["status"] == "success")
    fail_count = len(final_results) - success_count

    print(f"✅ 任务执行完成：成功{success_count}个，失败/超时{fail_count}个")
    print("详细执行结果：")
    for idx, item in enumerate(final_results):
        print(f"任务{idx+1}: {item}")

```



