import multiprocessing

import time

'''
进程运行需要执行任务，定义一个任务
'''
def task(name, delay):
    '''
    子进程执行函数
    :param name: 参数，接受子进程名字
    :param delay: 参数，接受延迟的时间s
    :return: None
    '''
    print(f'子进程 {name} 启动, PID: {multiprocessing.current_process().pid}')
    time.sleep(delay)
    print(f'子进程{name}执行完毕')

print(f'main函数外进程PID: {multiprocessing.current_process().pid}\n'
      f'__name__ : {__name__}')

if __name__ =='__main__':
    # 只有主进程能走入这里
    print(f'主进程PID：{multiprocessing.current_process().pid}')
    # 创建子进程
    p1 = multiprocessing.Process(target=task, args=('p1', 2))
    p2 = multiprocessing.Process(target=task, kwargs={
        'name':'p2',
        'delay':3,
    })
    # 启动子进程
    p1.start()
    p2.start()
    # 等待两个子进程
    p1.join()
    p2.join()
    print(f'主进程退出')