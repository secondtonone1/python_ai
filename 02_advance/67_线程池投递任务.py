from concurrent.futures import ThreadPoolExecutor
import time

def task(num):
    print(f'任务{num}开始')
    time.sleep(1)
    return f'任务{num}完成'

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        # 提交任务, 返回的是一个列表，每个列表是要执行的任务
        futures = [pool.submit(task,i) for i in range(6)]
        # 获取结果
        for f in futures:
            print(f.result())