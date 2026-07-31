from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

def err_task():
    time.sleep(2)
    raise ValueError("任务内部报错")

with ThreadPoolExecutor(2) as pool:
    f = pool.submit(err_task)
    try:
        res = f.result(timeout=1)
    except TimeoutError:
        print("任务执行超时")
    except Exception as e:
        print("任务异常：", e)