from concurrent.futures import ThreadPoolExecutor
import time

def calc(x):
    time.sleep(1)
    return x * x

if __name__ == "__main__":
    data = [1,2,3,4,5]
    with ThreadPoolExecutor(3) as pool:
        # 自动分配线程，结果顺序和输入一致
        res = pool.map(calc, data)
        print(list(res))