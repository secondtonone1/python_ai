import threading
lock = threading.Lock()
num = 0

def add():
    # 加锁
    lock.acquire()
    print('第一次加锁成功')
    # 该代码导致死锁，因为对互斥锁重复加锁导致死锁
    lock.acquire()
    print('第二次加锁成功')
    global num
    num += 1
    lock.release()
    lock.release()

rlock = threading.RLock()
def func():
    rlock.acquire()
    print('第一次加锁')
    rlock.acquire()
    print('同一线程第二次加锁, 不会阻塞')
    rlock.release()
    rlock.release()



if __name__ == '__main__':
    # add()
    t = threading.Thread(target=func)
    t.start()
    t.join()
