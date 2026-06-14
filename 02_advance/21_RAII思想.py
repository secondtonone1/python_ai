'''
演示RAII思想的应用
'''

'''
RAII思想
就是在对象初始化的时候创建资源
在对象结束的时候回收资源
达到资源和对象绑定的效果，资源的回收和创建绑定给了对象的生命周期
'''
import threading

class MyLock(object):
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        print('加锁')
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('解锁')
        self.lock.release()

if __name__ == '__main__':
    '''
    自动加锁和解锁
    '''
    with MyLock() as lock:
        print('我正在上厕所')
        print('上完厕所了')

    # 即使出现异常，也不会导致锁未被释放
    try:
        with MyLock() as lock:
            print('我正在上厕所')
            raise ValueError("领导让我来开会")
            print('上完厕所了')
    except Exception:
        print('捕获异常')

    # 如下操作会导致锁未被释放
    try:
        print('加锁')
        threading.Lock().acquire()
        print('我正在上厕所')
        raise ValueError('领导让我来开会')
        print('厕所上完了')
        threading.Lock().release()
        print('解锁')
    except Exception:
        print('捕获异常')