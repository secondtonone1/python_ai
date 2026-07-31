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

def dm03():
    # 启动事件循环，调用gather main协程
    asyncio.run(gather_main())

async def async_seq_main():
    # 也可不包裹成任务 直接等待协程执行结束
    t1 = task('C', 3)
    t2 = task('D', 5)
    # 相当于串行
    res3 = await t1
    res4 = await t2

def dm04():
    asyncio.run(async_seq_main())

if __name__ == '__main__':
    # dm01()
    # dm02()
    # dm03()
    dm04()