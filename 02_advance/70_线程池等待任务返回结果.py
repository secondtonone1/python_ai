from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED,FIRST_COMPLETED
import time

def work(x):
    time.sleep(1)
    return x

if __name__ == '__main__':
    with ThreadPoolExecutor(3) as pool:
        # 返回的futures队列
        fs = [pool.submit(work,i) for i in range(1,6)]
        # # 等待futures结果，也就是任务完成，这里只要第一个任务完成就返回
        # done, pending = wait(fs,return_when=FIRST_COMPLETED)
        # # 只要第一个任务完成返回，就可以获取结果
        # print('最先完成任务结果: ', [d.result() for d in done])

        # 等待futures结果，也就是任务完成，这里所有任务完成就返回
        done, pending = wait(fs, return_when=ALL_COMPLETED)
        # 只要第一个任务完成返回，就可以获取结果
        print('所有任务结果: ', [d.result() for d in done])