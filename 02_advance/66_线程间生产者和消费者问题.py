import threading
import time
import queue
# 创建一个条件变量对象
cond = threading.Condition()
# 用列表模拟队列
task_list = []
# 队列最大大小
task_max_len = 5

# 生产者任务
def producer():
    product_id = 0
    while True:
        with cond:
            # 队列满了
            if len(task_list) >= task_max_len:
                print('仓库满了,生产者等待')
                cond.wait()
            # 走到这里队列不满
            product_id = product_id + 1
            task_list.append(product_id)
            print(f'生产者生产产品, {product_id}')
            # 如果队列大小为1，则说明仓库由空到1，激活消费者
            if len(task_list) == 1:
                cond.notify_all()
        time.sleep(0.5)

# 消费者任务
def consumer():
    while True:
        with cond:
            # 队列为空，则等待
            if len(task_list) == 0:
                print('仓库为空,消费者等待')
                cond.wait()
            # 走到这里，说明队列不为空，则消费者消费
            product_id = task_list.pop(0)
            print(f'消费者消费商品, {product_id}')
            if len(task_list) == task_max_len-1:
                # 条件变量通知生产者
                cond.notify_all()
        time.sleep(1)

if __name__ == '__main__':
    producer = threading.Thread(target=producer)
    consumer = threading.Thread(target=consumer)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()

