'''
演示mongodb的连接，数据读取，关闭等操作
'''

from pymongo import MongoClient

def init_mongo():
    # 连接本地默认端口 MongoDB
    client = MongoClient("mongodb://119.91.129.93:27199/")
    # 查询所有数据库
    db_list = client.list_database_names()
    print('当前所有数据库: ', db_list)

    return client

def use_db_coll(client):
    # 选择数据库
    db = client['test_db']
    # 选择集合
    coll = db['users']
    # 查看所有集合
    coll_names = db.list_collection_names()
    print(f'查看所有集合为: {coll_names}')

def insert_data(client):
    # 选择数据库
    db = client['test_db']
    # 选择集合
    coll = db['users']

    # 文档数据(Python 字典格式）
    user = {
        'name':'zack',
        'age': 38,
        'gender':'male',
        'hobby': ['爬山','看海','编程'],
        'desc': '代码理性到底，文字情深入骨',
        'address': {'city':'天津','district':'滨海新区'}
    }

    # 插入单条数据
    res = coll.insert_one(user)
    print('新增文档ID: ', res.inserted_id)

def insert_many(client):
    db = client['test_db']
    coll = db['users']
    user_list = [
        {"name":"李四",'age':38,'gender':'male'},
        {'name':'王五','age':18,'gender':'male'},
        {'name': '赵六','age':28,'gender':'female'},
    ]
    # 批量插入
    res = coll.insert_many(user_list)
    print('批量新增ID列表： ', res.inserted_ids)

def find(client):
    db = client['test_db']
    coll = db['users']
    data = coll.find_one({'name':'zack'})
    print(f'单条查询信息: {data}')

    # 查找所有人信息
    all_data = coll.find()
    for item in all_data:
        print(item)

    print(f'年龄大于25岁用户信息:\n')
    # 查找年龄大于25岁用户
    filter_data = coll.find({'age': {'$gte': 25}})
    for item in filter_data:
        print(item)

def find_fields(client):
    db = client['test_db']
    coll = db['users']
    data = coll.find({},{'name':1,'age':1,'_id':0})
    for item in data:
        print(item)

def find_by_page(client, page):
    db = client['test_db']
    coll = db['users']
    page_data = coll.find().sort('age',-1).skip((page-1)*3).limit(3)

    for item in page_data:
        print(item)


def update_data(client):
    db = client['test_db']
    coll = db['users']
    res = coll.update_one({'name':'zack'},{"$set":{'age':18}})
    print(f'更新成功条数: ', res.modified_count)

def update_many(client):
    db = client['test_db']
    coll = db['users']
    res = coll.update_many({'age':{'$lt':25}},
                           {"$inc":{'age':1}})

    print(f'批量更新的条数: {res.modified_count}')

def delete_one(client):
    db = client['test_db']
    coll = db['users']
    res = coll.delete_one({'name':'李四'})
    print('删除条数: ', res.deleted_count)

def delete_many(client):
    db = client['test_db']
    coll = db['users']
    res = coll.delete_many(
        {'age':{'$gt':25}},
    )
    print(f'批量删除的条数: {res.deleted_count}')

if __name__ == '__main__':
    client = init_mongo()
    use_db_coll(client)
    insert_data(client)
    insert_many(client)
    # find(client)
    # find_fields(client)
    # find_by_page(client,2)
    # update_data(client)
    # update_many(client)
    # delete_one(client)
    # delete_many(client)


