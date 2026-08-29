import asyncio
import redis.asyncio as aioredis
import time
import redis

async def main():
    # 创建redis连接池
    pool  = aioredis.ConnectionPool(
        host='119.91.129.93',
        port=6380,
        db=1,
        max_connections=50,  # 设置连接池的最大连接数
        decode_responses=True,
        password='123456'
    )
    # 创建redis对象
    r = aioredis.Redis(connection_pool=pool)
    print(await r.ping())
    # 设置key和value对
    await r.set('name','zack')
    print(f'name is {await r.get('name')}')
    # 管道操作
    pipe = r.pipeline()
    pipe.set('k1','v1')
    pipe.set('k2','v2')

    results = await pipe.execute()
    print(f'results is {results}')
    await r.aclose()

class RateLimiter:
    def __init__(self, r, key_prefix, limit, window):
        # 存储redis对象
        self.r = r
        # 存储前缀
        self.key_prefix = key_prefix
        # 存储最大请求数量限制
        self.limit = limit
        # 窗口时间
        self.window = window

    def is_allowed(self,user_id):
        key = f'{self.key_prefix}:{user_id}'
        now = time.time()
        # 从当前时间推算self.window之前的描述，计算这个区间内key出现了多少次
        window_start = now - self.window
        # 创建管道对象
        pipe = self.r.pipeline()
        # 删除窗口外的旧记录
        pipe.zremrangebyscore(key, 0, window_start)
        # 统计当前窗口内的请求数
        pipe.zcard(key)
        # 增加当前请求
        pipe.zadd(key, {str(now): now})
        # 设置key过期时间
        pipe.expire(key, self.window)
        # 执行管道
        _, current_count, _, _ = pipe.execute()
        return current_count < self.limit

def conn_pool():
    pool = redis.ConnectionPool(
        host='119.91.129.93',
        port = 6380,
        db = 1,
        max_connections=50,  # 设置连接池的最大连接数
        decode_responses=True,
        password='123456'
    )

    r = redis.Redis(connection_pool=pool)
    print(r.ping())
    return r

def check_limit():
    r = conn_pool()
    limiter = RateLimiter(r,'rate:api',limit=10,window=60)
    for i in range(12):
        allowed = limiter.is_allowed('user123')
        print(f"请求 {i+1}: {'通过' if allowed else '拒绝'}")
        time.sleep(0.5)

if __name__ == '__main__':
    # asyncio.run(main())
    check_limit()
