import random
import redis
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

class Leaderboard:
    def __init__(self,key):
        # self.key存储集合名字
        self.key = key

    def add_score(self,player,score):
        # 向集合中添加用户和得分
        r.zadd(self.key,{player:score})

    def get_top(self, n = 10):
        # 获取key集合中，前n个用户
        return r.zrevrange(self.key, 0, n-1, withscores=True)

    def get_rank(self, player):
        # 获取player对应的排名，如果排名为空则返回None否则返回rank+1
        # rank是从0开始，所以+1
        rank = r.zrevrank(self.key, player)
        return rank+1 if rank is not None else None

    def get_nearby(self,player,range_count=2):
        rank = r.zrevrank(self.key, player)
        if rank is None:
            return []
        # 获取0或者rank-range_count的最大值，防止负数越界
        # start作为当前玩家能看到的前range_count名用户
        start = max(0,rank-range_count)
        # 当前玩家能看到的后面range_count名用户
        end = range_count + rank
        return r.zrevrange(self.key, start,end, withscores=True)

if __name__ == '__main__':
    # 模拟游戏排行
    lb = Leaderboard('game:score')
    # 添加玩家分数
    players = ['Zack','Ray','Charlies','David','Eve']
    random.seed(5)
    for p in players:
        lb.add_score(p,random.randint(100,1000))

    print(f'🏆 排行榜 Top3: ')
    # enumerate(lb.get_top(3),1)表示每个元素和数字拼接，数字从1开始
    for rank, (player,score) in enumerate(lb.get_top(3),1):
        print(f"{rank}: {player}: {score}分")
    print(f'Zack的排名: 第{lb.get_rank('Zack')}名')
    print(f'Zack附近的玩家:\n')
    for player,score in lb.get_nearby('Zack'):
        print(f' {player}: {int(score)} 分')