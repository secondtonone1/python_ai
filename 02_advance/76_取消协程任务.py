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