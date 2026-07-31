import asyncio

event = asyncio.Event()

# 等待信号的协程
async def wait_event_task():
    print('协程正在等待唤醒信号...')
    await event.wait()
    print('收到信号,开始执行业务逻辑')

# 发送信号的协程
async def send_event_signal():
    await asyncio.sleep(3)
    print('3秒倒计时结束,发送唤醒信号')
    event.set()

# 异步主函数
async def main():
    t1 = asyncio.create_task(wait_event_task())
    t2 = asyncio.create_task(send_event_signal())
    await t1
    await t2

if __name__ == '__main__':
    asyncio.run(main())