import threading
import time

def daemon_task():
    while True:
        print('守护线程正在运行中...')
        time.sleep(1)

def normal_task():
    time.sleep(3)
    print('普通子线程结束')

if __name__ == '__main__':
    # daemon=True,说明t1是守护线程，主线程结束，t1直接被回收
    t1 = threading.Thread(target=daemon_task, daemon=True)
    # t2 不是守护线程，主线程要等待t2结束之后才能结束
    t2 = threading.Thread(target=normal_task)

    t1.start()
    t2.start()
    print('主线程执行完毕,守护线程直接销毁...')