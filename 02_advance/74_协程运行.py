import asyncio

async def sleep_demo():
    print('开始异步等待2秒模拟IO阻塞')
    # 异步休眠，替代time.sleep(),在异步函数中使用同步阻塞会导致卡死线程
    await asyncio.sleep(2)
    print('2秒后IO等待结束，恢复协程执行')

if __name__ == '__main__':
    asyncio.run(sleep_demo())