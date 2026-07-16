'''
演示进程操作共享空间
'''

import multiprocessing

def add_num(share_list, lock, num):
    '''
    将num放入列表share_list中
    :param share_list: 通过Manager()从共享空间中开辟的列表
    :param lock: 进程安全锁
    :param num: 任务数据放入列表中
    :return: None
    '''
    # 加锁 同一时间仅有一个进程修改共享数据
    lock.acquire()
    try:
        share_list.append(num)
    finally:
        lock.release()

if __name__ == '__main__':
    # 创建管理器
    manager = multiprocessing.Manager()
    # 创建跨进程共享列表
    share_data = manager.list()
    # 创建进程锁
    lock = multiprocessing.Lock()
    # 存储创建的子进程，将来主进程等待子进程执行完成
    p_list = []
    for i in range(5):
        p = multiprocessing.Process(target=add_num, args=(share_data, lock, i))
        p.start()
        p_list.append(p)

    # 等待所有子进程运行结束
    for p in p_list:
        p.join()

    print('最终共享列表:', share_data)