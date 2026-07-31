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