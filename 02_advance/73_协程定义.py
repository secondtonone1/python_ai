import asyncio

# 定义协程函数
async def hello_coroutine():
    print('协程内部代码执行了')

# 调用协程函数,仅生成的是一个协程对象，不会执行函数
coro = hello_coroutine()
print(f'coro is {coro}')
print(f'type(coro) is {type(coro)}')