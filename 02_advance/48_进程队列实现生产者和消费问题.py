import multiprocessing
import time


def producer(q):
    '''
    生产者: 向队列写入数据
    :param q: 队列
    :return: None
    '''
    for i in range(10):
        q.put(f'数据{i}')
        print(f'生产者写入: 数据{i}')
        time.sleep(0.05)
    q.put('end')
    print('生产者进程结束')


def consumer(q):
    '''
    消费者从队列中获取数据
    :param q: 队列
    :return: None
    '''
    while True:
        # 队列为空则阻塞
        data = q.get()
        print(f'消费者读取: {data}')
        time.sleep(0.1)
        if data == 'end':
            break
    print('消费者进程结束')

if __name__ == '__main__':
    # 创建进程安全队列
    queue = multiprocessing.Queue(maxsize=10)
    # 创建生产者进程
    p_pro = multiprocessing.Process(target=producer, args=(queue,))
    # 创建消费者进程
    p_con = multiprocessing.Process(target=consumer, args=(queue,))
    # 启动两个进程
    p_pro.start()
    p_con.start()
    # 主进程等待生产者进程结束
    p_pro.join()
    p_con.join()