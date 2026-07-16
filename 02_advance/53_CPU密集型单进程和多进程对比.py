import multiprocessing
import time

def heavy_calc(n):
    s = 0
    for i in range(n):
        s += i ** 3
    return s

if __name__ == '__main__':
    task_data = [1000000] * 8

    # 单进程串行执行
    start = time.time()
    for data in task_data:
        heavy_calc(data)
    print(f"单进程耗时: {time.time() - start:.2f}s")

    # 多进程并行执行
    start = time.time()
    with multiprocessing.Pool(4) as pool:
        pool.map(heavy_calc, task_data)
    print(f"多进程耗时: {time.time() - start:.2f}s")

    # 多进程并行执行
    start = time.time()
    res_list = []
    with multiprocessing.Pool(8) as pool:

        for i in task_data:
            # 异步提交任务，不阻塞主进程
            # async_res是异步提交后的结果，不能直接获取任务执行的结果
            async_res = pool.apply_async(heavy_calc, args=(i,))
            # 将异步执行的结果状态放入tasks列表
            res_list.append(async_res)
        # res.get一定写在with里，等待进程执行完毕，如果写在with外
        # 导致进程被回收，所以get拿不到结果永久阻塞
        resuls = [res.get() for res in res_list]
    print(f"异步多进程耗时: {time.time() - start:.2f}s")