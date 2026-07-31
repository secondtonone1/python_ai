import threading
import time

event = threading.Event()

def wait_task():
    print('子线程等待信号...')
    # 接受Event事件
    event.wait()
    print('收到信号,并且开始执行任务')

def send_signal():
    time.sleep(3)
    print('发送通知信号')
    # 发送Event事件
    event.set()

if __name__ == '__main__':
    t1 = threading.Thread(target=wait_task)
    t2 = threading.Thread(target=send_signal)
    t1.start()
    t2.start()
    t1.join()
    t2.join()