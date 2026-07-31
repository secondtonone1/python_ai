import threading
num = 0
lock = threading.Lock()
def add():
    global num
    for _ in range(100000):
        # 自动加锁，代码块运行结束自动解锁
        with lock:
            num += 1

if __name__ == '__main__':
    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=add)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(f'正确结果为: {num}')