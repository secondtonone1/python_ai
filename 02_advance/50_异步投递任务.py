'''
演示进程池异步投递任务
'''
import multiprocessing
import time

def task(x):
    time.sleep(0.5)
    return x*10

if __name__ == '__main__':
    with multiprocessing.Pool(3) as pool:
        tasks = []
        for i in range(5):
            # 异步提交任务，不阻塞主进程
            # async_res是异步提交后的结果，不能直接获取任务执行的结果
            async_res = pool.apply_async(task, args=(i, ))
            # 将异步执行的结果状态放入tasks列表
            tasks.append(async_res)

        # 统一获取所有任务的返回值, res.get()会阻塞等待，直到任务执行完成
        final_results = [res.get() for res in tasks]
    print('异步任务执行结果: ', final_results)

