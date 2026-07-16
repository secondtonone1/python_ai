import multiprocessing
import time

def calc_power(num):
    '''
    模拟CPU密集型任务
    :param num: 任务参数
    :return: num**2
    '''
    res = num ** 2
    time.sleep(0.3)
    print(f'计算 {num}² = {res}')
    return res

if __name__ == '__main__':
    # 获取CPU核心数，设置进程池大小
    core_count = multiprocessing.cpu_count()
    print(f'本机中CPU核心数为: {core_count}')

    # 创建进程池, 进程数=CPU核心数
    with multiprocessing.Pool(processes=core_count) as pool:
        '''
        map把要执行任务的函数和参数结合起来，交给进程池中的进程执行
        大白话: 进程池中的进程相当于水池中的鱼，任务参数相当于鱼饵，
        函数相当于吃这个动作
        '''
        data_list = [1,2,3,4,5,6,7,8,9,10]
        # map自动分配任务，阻塞等待全部任务完成，返回结果列表
        result = pool.map(calc_power, data_list)
    print(f'所有进程执行结果: {result}')