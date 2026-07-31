import asyncio

async def error_task():
    await asyncio.sleep(1)
    raise ValueError('协程内部业务报错')

async def task(name, delay):
    #print(f'任务{name} 启动, 需要等待 {delay} s')
    await asyncio.sleep(delay)
    #print(f'任务{name} 执行完毕')
    return f'{name} 执行结果'

async def main():
    results = await asyncio.gather(
        task('正常任务',1),
        error_task(),
        return_exceptions=True
    )

    print(results)

if __name__ == '__main__':
    asyncio.run(main())