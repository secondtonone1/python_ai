import functools
import time


def cost_time(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'函数{func.__name__}执行耗时: {end - start:.4f}秒')
        return result
    return inner

@cost_time
def heavy_task():
    s = 0
    for i in range(1000000):
        s += i
    return s

heavy_task()

def catch_error(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f'函数{func.__name__}出现了异常, 异常为{e}')
            return None
    return inner

@catch_error
def div(a,b):
    return a / b

div(3,0)

# 通过类封装装饰器
class LogDecorator(object):
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        print('类装饰器: 函数开始执行')
        result =  self.func(*args, **kwargs)
        print('类装饰器: 函数执行结束')
        return result

@LogDecorator
def add(a, b):
    print('业务代码运行')

add(3,5)

# 练习题
# 带参数的通用日志装饰器
def log_action(action_type):
    # 第二层 接受被装饰的函数
    def decorator(func):
        @functools.wraps(func)
        # 第三层，通用执行逻辑
        def inner(*args, **kwargs):
            print(f'正在运行[{action_type}]数据操作')
            # 调用原函数
            result = func(*args, **kwargs)
            # 返回原函数执行的结果
            return result
        return inner
    return decorator

# 测试1: 数据查询功能
@log_action('查询')
def query_data(table_name):
    print(f'正在读取数据表: {table_name}')
    return '读取数据完成'

# 测试2：数据录入功能
@log_action("录入")
def insert_data(table_name, count):
    print(f"向{table_name}插入{count}条记录")
    return "录入完成"

# 测试3：数据移除功能
@log_action("移除")
def remove_data(row_id):
    print(f"删除行号：{row_id}的数据")
    return "删除完成"

# 调用测试
print(query_data("sales_data"))
print("-"*25)
print(insert_data("user_info", 35))
print("-"*25)
print(remove_data(608))