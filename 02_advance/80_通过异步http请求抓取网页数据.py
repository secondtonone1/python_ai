import asyncio
import aiohttp

# 限定最大并发协程数量
sem = asyncio.Semaphore(3)

async def crawl_page(session, url):
    '''

    :param session: 异步http会话对象
    :param url: 要抓取的网页的地址
    :return: None
    '''

    # 占用一个并发席位，超出数量限制则阻塞等待
    async with sem:
        # session.get(url)返回的是一个协程对象
        async with session.get(url) as resp:
            # 异步等待, 可以把resp.text()理解为一个task任务，等待任务返回
            # 等待期间会释放cpu资源，让线程调度其他协程
            # 直到resp.text()返回结果，协程继续执行
            html = await resp.text()
            print(f'{url} 页面字节大小: {len(html)}')

async def main():
    # 创建异步http会话对象
    async with aiohttp.ClientSession() as session:
        # 8个相同连接,为了演示最多3个并发请求
        url_list = ['https://llfc.club']*8
        # 用列表推导式生成协程对象列表
        tasks = [crawl_page(session, url) for url in url_list]
        # *代表解引用，将列表中的元素一个一个展开，作为可变位置参数传递给gather
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())