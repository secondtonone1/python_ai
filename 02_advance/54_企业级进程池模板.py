'''
演示企业级进程池模板
'''

import multiprocessing
import time
import traceback
from multiprocessing.pool import Pool
# ======================核心工具封装(无需修改)===========
def single_task_safe_wrapper(func,*args, **kwargs):
    """
    任务安全包装器：隔离单个任务异常，防止整池崩溃
    :param func: 自定义任务函数
    :param args: 任务位置参数
    :param kwargs: 任务关键字参数
    :return: 任务结果/异常信息
    """
    try:
        result = func(*args, **kwargs)
        return {
            "status": "success",
            "data": result,
            "error":None
        }
    except Exception as e:
        return {
            "status": "fail",
            "data":None,
            "error":f"任务异常: {str(e)}",
            "traceback":traceback.format_exc()
        }

def create_production_pool(max_workers=8, max_task_per_child = 20):
    """
    创建生产级进程池
    :param max_workers: 最大并发进程数，默认自适应CPU核心数
    :param max_task_per_child: 单进程最大执行任务数，到期重建（防内存泄漏）
    :return: 进程池对象
    """
    # 自适应CPU核心数，避免资源耗尽
    if not max_workers:
        max_workers = multiprocessing.cpu_count()

    return Pool(processes=max_workers, maxtasksperchild=max_task_per_child)


def batch_run_tasks(task_func, task_params_list, timeout: int = 30):
    """
    批量并发执行多任务
    :param task_func: 业务任务函数
    :param task_params_list: 任务参数列表，每个元素为单任务参数
    :param timeout: 单任务最大超时时间(秒)
    :return: 全部任务结果列表
    """
    pool = create_production_pool()
    async_results = []

    # 异步批量提交任务
    for params in task_params_list:
        if isinstance(params, (list, tuple)):
            res = pool.apply_async(single_task_safe_wrapper, args=(task_func, *params))
        else:
            res = pool.apply_async(single_task_safe_wrapper, args=(task_func, params))
        async_results.append(res)

    # 等待并获取所有任务结果
    all_results = []
    for res in async_results:
        try:
            all_results.append(res.get(timeout=timeout))
        except multiprocessing.TimeoutError:
            all_results.append({
                "status": "timeout",
                "data": None,
                "error": f"任务超时(最大{timeout}s)",
                "traceback": None
            })

    # 关闭进程池，释放资源
    pool.close()
    pool.join()
    return all_results

# ====================== 业务层：自定义你的任务（仅需修改此处） ======================
def business_task(x):
    """
    自定义业务计算任务（用户可按需改写）
    支持数值计算、数据处理、模型推理等CPU密集操作
    """
    # 模拟重度CPU计算
    res = 0
    for i in range(1000000):
        res += i ** 2
    return x * res

def heavy_calc(n):
    s = 0
    for i in range(n):
        s += i ** 3
    return s

# ====================== 程序入口（固定写法） ======================
if __name__ == '__main__':
    # 批量任务参数
    task_params = [1, 2, 3, 4, 5, 6, 7, 8]
    # 批量执行任务
    final_results = batch_run_tasks(business_task, task_params, timeout=20)

    # 结果统计与打印
    success_count = sum(1 for res in final_results if res["status"] == "success")
    fail_count = len(final_results) - success_count

    print(f"✅ 任务执行完成：成功{success_count}个，失败/超时{fail_count}个")
    print("详细执行结果：")
    for idx, item in enumerate(final_results):
        print(f"任务{idx+1}: {item}")

    # 批量执行任务
    task_params = [1000000] * 8
    start = time.time()
    final_results = batch_run_tasks(heavy_calc, task_params, timeout=20)

    # 结果统计与打印
    success_count = sum(1 for res in final_results if res["status"] == "success")
    fail_count = len(final_results) - success_count

    print(f"✅ 任务执行完成：成功{success_count}个，失败/超时{fail_count}个")
    print("详细执行结果：")
    for idx, item in enumerate(final_results):
        print(f"任务{idx+1}: {item}")
    end = time.time()
    print('并发执行耗时: ', end - start, ' s')
