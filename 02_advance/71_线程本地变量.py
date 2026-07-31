import threading
# 线程本地数据
local_data= threading.local()

def func(name):
    # 每个线程独立存储value
    local_data.value = name
    print(f'线程{name}: {local_data.value}')

if __name__ == '__main__':
    t1 = threading.Thread(target=func, args=('A',))
    t2 = threading.Thread(target=func, args=('B',))
    t1.start()
    t2.start()
