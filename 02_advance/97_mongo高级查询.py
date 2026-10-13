from pymongo import MongoClient

def init_mongo():
    # 连接本地默认端口 MongoDB
    client = MongoClient("mongodb://119.91.129.93:27199/")
    # 查询所有数据库
    db_list = client.list_database_names()
    print('当前所有数据库: ', db_list)

    return client


def find_pro(client):
    # 选择数据库
    db = client['test_db']
    # 选择集合
    coll = db['users']
    # 查找年龄在22, 25, 28岁的用户
    data1 = coll.find({'age': {'$in':[22,25,28]}})
    print(f'data1: {data1}')
    print(f'data1 type is : {type(data1)}')

    for item in data1:
        print(f'item: {item}')
    print('🖤'*10)
    # 使用or查找
    data2 = coll.find({
        "$or":[
            {"age":{"$gt":28}},
            {"gender":"female"}
        ]
    })

    for item in data2:
        print(f'item: {item}')

    print('🖤'*10)
    # 数组字段查询, 爱好包含篮球用户
    data3 = coll.find({"hobby":"爬山"})
    for item in data3:
        print(f'item: {item}')

def use_pipeline(client):
    db = client['test_db']
    coll = db['users']

    # 定义聚合管道
    pipeline = [
        # 第一步,筛选18岁以上的用户
        {"$match": {"age": {"$gt": 18}}},
        # 第二步,按性别分组聚合
        {
            "$group":{
                "_id":"$gender", # 分组字段
                "user_count": {"$sum": 1},# 统计人数
                "avg_age": {"$avg": "$age"} # 计算平均年龄
            }
        },
        # 第三步
        {"$sort":{"user_count":-1}},
    ]

    # 执行聚合查询
    result = coll.aggregate(pipeline)
    for item in result:
        print(f'聚合结果： ', item)


if __name__ == '__main__':
    client = init_mongo()
    # find_pro(client)
    use_pipeline(client)