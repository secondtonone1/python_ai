import aiohttp
import asyncio

# 全局配置
MAX_CONCURRENT = 5  # 最大并发数
sem = asyncio.Semaphore(MAX_CONCURRENT)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
TIMEOUT = aiohttp.ClientTimeout(total=3)  # 请求超时3秒

async def fetch_url(session: aiohttp.ClientSession, url: str):
    """单个网页异步请求函数"""
    async with sem:
        try:
            async with session.get(url, headers=headers, timeout=TIMEOUT) as resp:
                page_html = await resp.text()
                return f" {url} | 状态码:{resp.status} | 页面长度:{len(page_html)}"
        except Exception as e:
            return f" {url} | 请求失败: {str(e)}"

async def main():
    # 待爬取链接列表
    url_list = [
        "https://llfc.club", # 官方博客
        "https://gitbookcpp.llfc.club/", # 编程笔记
        "https://www.limerence2017.com/", # 个人博客
        "https://www.yuque.com/lianlianfengchen-cvvh2" #个人语雀花园

    ]
    # 全局复用ClientSession，性能远高于频繁创建会话
    async with aiohttp.ClientSession() as session:
        task_list = [fetch_url(session, url) for url in url_list]
        result_list = await asyncio.gather(*task_list)
    # 遍历打印所有爬取结果
    for res in result_list:
        print(res)

if __name__ == "__main__":
    asyncio.run(main())