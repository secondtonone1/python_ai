import redis
import time
import threading
import uuid

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

def set_expire_time():
    r = conn_pool()
    # 设置过期时间为3600s
    r.set('session:user123','data',ex=6)
    # 设置过期时间为5000ms
    r.set('temp','value',px= 5000)
    # time.sleep(6)
    # res = r.exists('session:user123')
    # print(f'res:{res}')
    # res = r.get('temp')
    # print(f'res:{res}')
    time.sleep(2)
    res = r.ttl('session:user123')
    print(f'res:{res}')
    # 给已有的key设置60s过期时间
    r.expire('session:user123', 60)
    res = r.ttl('session:user123')
    print(f'res:{res}')
    # 设置持久化，取消过期时间
    r.persist('session:user123')
    # 设置为持久化之后过期时间变为-1
    res = r.ttl('session:user123')
    print(f'res:{res}')

def pipe_op():
    r = conn_pool()
    # 管道
    pipe = r.pipeline()
    pipe.set('key1','value1')
    pipe.set('key2','value2')
    pipe.set('counter',1)
    pipe.incr('counter')
    pipe.set('stock:1001',5)
    results = pipe.execute()
    print(results)

    # 事务操作
    with r.pipeline() as pipe:
        # 乐观锁
        while True:
            try:
                # 1.监视某个key,比如key表示的是一个库存
                pipe.watch('stock:1001')
                # 2. 读取当前库存(watch之后再读)
                current_stock = int(pipe.get('stock:1001') or 0)

                if current_stock > 0:
                    # 3. 开启事务
                    pipe.multi()
                    # 4. 事务内部命令，扣减库存
                    pipe.decr('stock:1001')
                    # 5. 提交事务
                    pipe.execute()
                    print('扣减成功')
                    break
                else:
                    print('库存不足')
                    pipe.unwatch()
                    break

            # 当我们执行管道操作时，其他线程或者进程已经对key修改了，
            # 就会报错
            except redis.WatchError:
                continue

def publisher():
    r = conn_pool()
    for i in range(5):
        r.publish('channel:news',f'消息{i}')
        print(f'发布: 消息{i}')


def subscriber():
    r = conn_pool()
    # 创建订阅者
    pubsub = r.pubsub()
    # 设置订阅者从哪里获取消息,订阅频道
    pubsub.subscribe('channel:news')

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f'收到: {message["data"]}')
            # 如果获取到第5条消息，说明消息获取结束
            if message['data'] == '消息4':
                pubsub.unsubscribe()
                break

def pub_sub_thread():
    threading.Thread(target=publisher).start()
    threading.Thread(target=subscriber).start()


def acquire_lock(r,lock_name, acquire_time= 10):
    '''
    获取分布式锁
    :param r: redis对象
    :param lock_name: 锁的名字
    :param acquire_time: 锁持有的时间
    :return: identifier or None
    '''
    # 生成唯一id
    identifier = str(uuid.uuid4())
    # 准备key
    lock_key = f'lock:{lock_name}'

    # 设置NX(不存在才设置) + EX(设置过期时间) 保证原子性
    if r.set(lock_key, identifier, nx=True, ex=acquire_time):
        return identifier
    # 其他线程/进程无法加锁
    return None

def release_lock(r,lock_name, identifier):
    '''
    释放分布式锁,(使用lua脚本保证原子性)
    :param r: redis对象
    :param lock_name: 锁的名字
    :param identifier: 之前加锁的value
    :return:  删除成功返回1，失败返回0
    '''
    lock_key = f'lock:{lock_name}'
    lua_script = f'''
        if redis.call("get", KEYS[1]) == ARGV[1] then 
            return redis.call("del", KEYS[1])
        else
            return 0
        end
    '''
    return r.eval(lua_script, 1, lock_key, identifier)

def use_dis_redis_lock():
    r = conn_pool()
    lock_id = acquire_lock(r,'order:1001')
    if lock_id:
        try:
            print('获取锁成功，执行业务逻辑...')
            time.sleep(2)
        finally:
            release_lock(r,'order:1001',lock_id)
            print('锁已经释放')
    else:
        print('获取锁失败')

if __name__ == '__main__':
    # r = conn_pool()
    # set_expire_time()
    # pipe_op()
    # pub_sub_thread()
    use_dis_redis_lock()