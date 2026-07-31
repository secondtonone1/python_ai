'''
演示死锁场景
'''
import threading
lock = threading.Lock()
num = 0
# 加锁未解锁
def add():
    print(f'当前线程: {threading.current_thread().name} 执行任务add')
    lock.acquire()
    print(f'当前线程: {threading.current_thread().name}, 加锁成功!')
    global num
    num += 1
    print(f'当前线程: {threading.current_thread().name}, 线程结束')

if __name__ == '__main__':
    threading.Thread(target=add).start()
    threading.Thread(target=add).start()
