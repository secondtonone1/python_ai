import threading
import time
# 最多同时3个线程运行
sem = threading.Semaphore(3)
# 定义爬虫函数
def crawl(url):
    # 通过with语法将被sem控制的逻辑写入with下面
    with sem:
        print(f'正在爬取 {url}, 线程: {threading.current_thread().name}')
        time.sleep(2)
        print(f'爬取完成 {url}')

if __name__ == '__main__':
    urls = ['https://www.baidu.com/',
            'https://www.zhihu.com/',
            'https://www.yahoo.com/',
            'https://www.sogou.com/',
            'https://www.jianshu.com/',
            'https://llfc.club/',
            'https://gitbookcpp.llfc.club/',
            'https://www.yuque.com/lianlianfengchen-cvvh2',
            'https://www.limerence2017.com/'
            ]
    thread_list = []
    for url in urls:
        t = threading.Thread(target=crawl, args=(url,))
        thread_list.append(t)
        # 子线程启动
        t.start()

    for t in thread_list:
        # 主线程等待子线程退出
        t.join()