'''
演示如何创建线程
'''
import threading
import time

def task(name, delay):
    '''

    :param name: 线程名字
    :param delay: 睡眠时间单位s
    :return: None
    '''
    print(f'线程{name}启动,休眠{delay}s')
    time.sleep(delay)
    print(f'线程{name}执行完毕')

if __name__ == '__main__':
    # 创建线程对象, target=执行函数  args=参数元组
    t1 = threading.Thread(target=task,args=('A',2))
    t2 = threading.Thread(target=task,kwargs={
        'name':'B',
        'delay':1,
    })

    # 启动线程
    t1.start()
    t2.start()
    # join 主线程阻塞，等待子线程执行完毕后继续往下走
    t1.join()
    t2.join()
    print('所有子线程执行完毕')