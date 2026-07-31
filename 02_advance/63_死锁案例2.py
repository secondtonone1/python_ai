'''
演示死锁场景
'''
import threading
lock = threading.Lock()
num = 0

def add_():
    lock.acquire()
    global num
    num += 1
    lock.release()

# 嵌套加锁
def add():
    print(f'当前线程: {threading.current_thread().name} 执行任务add')
    lock.acquire()
    print(f'当前线程: {threading.current_thread().name}, 加锁成功!')
    global num
    num += 1
    add_()
    print(f'当前线程: {threading.current_thread().name}, 线程结束')
    lock.release()

if __name__ == '__main__':
    threading.Thread(target=add).start()
    threading.Thread(target=add).start()
