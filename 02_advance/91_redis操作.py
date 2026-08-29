import redis

def ping_conn():
    # 创建redis连接
    # 参1 是reis所在机器的ip地址
    # 参2 是redis服务的端口号
    # 参3 是使用redis服务的哪个扇区
    # 参4 对字节流解码为str
    # 参5 使用密码登录
    r = redis.Redis(host='119.91.129.93', port=6380, db=4,decode_responses=True,password='123456')
    # 测试连接是否通畅，如果联通则返回true
    print(r.ping())

def conn_pool():
    pool = redis.ConnectionPool(
        host='119.91.129.93',
        port = 6380,
        db = 4,
        max_connections=50,  # 设置连接池的最大连接数
        decode_responses=True,
        password='123456'
    )

    r = redis.Redis(connection_pool=pool)
    print(r.ping())
    return r

def set_string():
    r = conn_pool()
    # 设置键值对
    r.set('name','Alice')
    # 设置过期时间，超过指定时间后key和value从redis中移除
    r.set('name','Bob',ex=60)

    # 如果key不存在则设置，否则不设置(分布式锁的基础)
    # 会等待Bob过期后才设置成功
    r.set('name','Charlie',nx=True)
    # 读取
    value = r.get('name')
    print(value)

    # 批量操作,批量设置key和value对
    r.mset({'key1':'val1','key2':'val2'})
    # 批量获取value
    result = r.mget(['key1','key2'])
    print(result)

    # 自增操作
    r.set('counter',0)
    # key对应的value自增1
    r.incr('counter')
    print(r.get('counter'))
    # key对应的value自增指定的步长
    r.incrby('counter',5)
    print(r.get('counter'))

    # key对应的value自减
    r.decr('counter')
    print(r.get('counter'))
    r.decrby('counter',5)
    print(r.get('counter'))

    r.incrbyfloat('counter',1.5)
    print(r.get('counter'))

    # 其他
    r.set('temp','hello')
    r.append('temp',' world')
    print(r.get('temp'))
    print(r.strlen('temp'))
    print(r.getrange('temp',0,4))

def hset_op():
    r = conn_pool()
    r.hset('user:1001',mapping={
        'name':'张三',
        'age':25,
        'email': 'zhangsan@example.com'
    })

    # 读取字段
    name = r.hget('user:1001','name')
    print(f'name:{name}')

    # 获取所有的key:value对
    all_fields = r.hgetall('user:1001')
    print(f'all_fields:{all_fields}')

    # 字段操作
    # 年龄+1
    r.hincrby('user:1001','age',1)
    print(f"r.hgetall('user:1001'):{r.hgetall('user:1001')}")
    # 判断hash的value字典中某个key是否存在
    print(r.hexists('user:1001','phone'))
    # 删除字段
    r.hdel('user:1001','email')
    print(f"r.hgetall('user:1001'):{r.hgetall('user:1001')}")

    # 字段数量
    print(r.hlen('user:1001'))

    # 批量读取value字典中所有的key
    keys = r.hkeys('user:1001')
    print(f'keys:{keys}')

    # 获取所有的值
    values = r.hvals('user:1001')
    print(f'values:{values}')

def lpush_pop():
    r = conn_pool()
    r.delete('queue:tasks')
    # 从队列左侧插入数据
    r.lpush('queue:tasks','task1')
    # 从队列右侧插入数据
    r.rpush('queue:tasks','task2','task3')
    # 查看队列中数据, 获取队列中所有的数据
    datas = r.lrange('queue:tasks',0,-1)
    print(f'datas:{datas}')
    # 获取队列中元素的个数
    print(r.llen('queue:tasks'))
    r.delete('queue:tasks')
    # 演示栈操作
    r.lpush('queue:tasks','task1','task2','task3')
    print(r.lpop('queue:tasks'))
    print(r.lpop('queue:tasks'))
    print(r.lpop('queue:tasks'))
    print(f'🖤'*50)
    print(r.lrange('queue:tasks',0,-1))
    print(f'😊'*50)
    # 演示队列操作
    r.lpush('queue:tasks','task1','task2','task3')
    print(r.rpop('queue:tasks'))
    print(r.rpop('queue:tasks'))
    print(r.rpop('queue:tasks'))

    # 从左侧阻塞弹出,如果队列为空，最多阻塞5s
    res = r.blpop('queue:tasks',timeout=1)
    print(f'res:{res}')
    r.lpush('queue:tasks','task2')
    # 队列中插入数据/删除数据
    r.linsert('queue:tasks','before',
              'task2','new_task')
    print(r.lrange('queue:tasks',0,-1))
    # 裁剪，保留从0到0的1个元素
    r.ltrim('queue:tasks',0,0)
    print(r.lrange('queue:tasks',0,-1))
    # 删除1个值为new_task的元素
    r.lrem('queue:tasks',1,'new_task')
    print(r.lrange('queue:tasks',0,-1))

def set_op():
    r = conn_pool()
    # 添加元素
    r.sadd('tags:python','web','backend','ai')
    r.sadd('tags:java','web','backend','android')

    # 查询
    print(r.smembers('tags:python'))
    # 判断是否是成员
    print(r.sismember('tags:python','ai'))
    # 判断集合中元素的数量
    print(r.scard('tags:python'))
    # 从集合中随机抽取两个元素
    print(r.srandmember('tags:python',2))

    # 集合运算
    # 计算交集,第一个集合和第二个集合都存在的元素
    print(r.sinter('tags:python','tags:java'))
    # 计算并集,两个集合元素合并去重
    print(r.sunion('tags:python','tags:java'))
    # 计算差集, 第一个集合中有的元素，第二个集合中没有的元素
    print(r.sdiff('tags:python','tags:java'))
    # 删除
    r.srem('tags:python','ai')
    print(r.smembers('tags:python'))
    # 随机删除一个元素, 并返回删除的元素
    print(r.spop('tags:python'))
    print(r.smembers('tags:python'))

def zero_set():
    r = conn_pool()
    # 添加成员带分数
    r.zadd('leaderboard',
           {'player1':100,'player2':85,'player3':120},)
    # 查询排名, 按照升序查询，按照索引查询，从0到最后1个元素
    print(r.zrange('leaderboard',0,-1))
    # 升序带分数排名
    print(r.zrange('leaderboard',0,-1,withscores=True))
    # 降序排名，获取前3名
    print(r.zrevrange('leaderboard',0,2))
    # 获取排名，从0开始
    print(r.zrank('leaderboard','player1'))
    # 获取降序排名
    print(r.zrevrank('leaderboard','player2'))
    # 获得分数
    print(r.zscore('leaderboard','player1'))
    # 修改分数
    r.zincrby('leaderboard',5,'player1',)
    print(r.zscore('leaderboard', 'player1'))
    # 按照分数查询成员
    print(r.zrangebyscore('leaderboard',80,100))
    # 按照分数获取成员数量
    print(r.zcount('leaderboard',80,105))
    # 删除
    r.zrem('leaderboard','player3')
    print(r.zrange('leaderboard',0,-1))
    # 按照分数区间删除
    r.zremrangebyscore('leaderboard',80,105)
    print(r.zrange('leaderboard',0,-1))


if __name__ == '__main__':
    # ping_conn()
    # conn_pool()
    # set_string()
    # hset_op()
    # lpush_pop()
    # set_op()
    zero_set()
