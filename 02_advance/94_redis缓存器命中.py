import redis
import json
import hashlib
import functools

pool = redis.ConnectionPool(
        host='119.91.129.93',
        port = 6380,
        db = 1,
        max_connections=50,  # 设置连接池的最大连接数
        decode_responses=True,
        password='123456'
    )

# 创建redis对象
r = redis.Redis(connection_pool=pool)
print(r.ping())

def cache(expire=300):
    '''

    :param expire: redis过期时间
    :return: 装饰器外层函数
    '''
    # func将来接受load_from_db
    def decorator(func):
        '''

        :param func: 将来接受load_from_db
        :return: 内层函数
        '''
        @functools.wraps(func)
        def inner(*args, **kwargs):
            cache_key = f"cache:{func.__name__}:{hashlib.md5(str(args).encode()+str(kwargs).encode()).hexdigest()}"
            # 尝试读取缓存
            cached = r.get(cache_key)
            if cached:
                print('缓存命中')
                return json.loads(cached)
            # 执行函数并缓存结果,这里就是从数据库加载数据了
            result = func(*args, **kwargs)
            # 将数据库加载的结果放入redis
            r.set(cache_key, json.dumps(result),ex=expire)
            print(f'写入缓存')
            return result
        return inner
    return decorator


@cache(expire=60)
def load_from_db(user_id):
    # 模拟数据库查询
    print(f'查询数据库: user_id={user_id}')
    return {"id":user_id, "name":f"User_{user_id}","age":25}

# 第一次查数据库
print(load_from_db(1001))
# 第二次缓存命中
print(load_from_db(1001))