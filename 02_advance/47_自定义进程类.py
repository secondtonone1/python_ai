'''
演示如何自定义进程类
'''

import multiprocessing
import time

from dask import delayed


class MyProcess(multiprocessing.Process):
    def __init__(self, name,delayed):
        super().__init__()
        self.name = name
        self.delay = delayed

    def run(self):
        # 进程启动要执行的逻辑
        print(f'自定义进程 {self.name} 启动 PID: {self.pid}')
        time.sleep(self.delay)
        print(f'自定义进程 {self.name} 结束')

if __name__ == '__main__':
    p = MyProcess('恋恋风辰zack', 1.5)
    p.start()
    p.join()
    print('主进程结束')