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