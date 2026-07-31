import threading
import time
class MyThread(threading.Thread):
    def __init__(self,name,delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):
        # 线程核心逻辑，start时自动调用
        print(f'线程 {self.name} 启动')
        time.sleep(self.delay)
        print(f'线程 {self.name} 结束')

if __name__ == '__main__':
    t1 = MyThread('线程1',1)
    t2 = MyThread('线程2', 2)
    t1.start()
    t2.start()
    # t1.join()
    # t2.join()
    print('程序结束')
