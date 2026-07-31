'''
演示死锁场景
'''
import threading
import time

lock1 = threading.Lock()
lock2 = threading.Lock()
num = 0

def task1():
    lock1.acquire()
    print(f'线程1持有lock1...')
    time.sleep(1)
    lock2.acquire()
    print(f'线程1持有lock2...')
    global num
    num += 1
    lock2.release()
    print(f'线程1释放lock2...')
    lock1.release()
    print(f'线程1释放lock1...')

def task2():
    lock2.acquire()
    print(f'线程2持有lock2...')
    time.sleep(1)
    lock1.acquire()
    print(f'线程2持有lock1...')
    global num
    num += 1
    lock1.release()
    print(f'线程2释放lock1...')
    lock2.release()
    print(f'线程2释放lock2...')



if __name__ == '__main__':
    threading.Thread(target=task1).start()
    threading.Thread(target=task2).start()
