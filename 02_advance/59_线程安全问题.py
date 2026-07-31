import threading
num = 0
def add():
    global num
    for _ in range(100000):
        num += 1

if __name__ == '__main__':
    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=add)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('预期200000,实际结果为: ', num)