from pymongo import MongoClient
from bson import ObjectId
from typing import Dict, Optional, List, Any

class MongoDBDao:
    '''MongoDB 通用的操作封装类'''
    def __init__(self, uri:str='mongodb://119.91.129.93:27199/',db_name: str='test-db'):
        # 全局单例客户端
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, coll_name):
        ''' 获取集合对象'''
        return self.db[coll_name]

    def add_one(self, coll_name:str, data: Dict[str, Any]):
        ''' 新增单条数据 '''
        coll = self.get_collection(coll_name)
        res = coll.insert_one(data)
        return res.inserted_id

    def get_by_id(self, coll_name:str, doc_id: str):
        ''' 根据id查询数据'''
        try:
            coll = self.get_collection(coll_name)
            return coll.find_one({"_id": ObjectId(doc_id)})
        except Exception as e:
            return None

    def list_data(self, coll_name,  filter_dict=None, page = 1, page_size = 10):
        '''分页查询'''
        filter_dict = filter_dict or {}
        skip_num = (page-1)*page_size
        coll = self.get_collection(coll_name)
        return  list(coll.find(filter_dict).skip(skip_num).limit(page_size))

    def update_by_id(self, coll_name:str, doc_id: str, data: Dict[str, Any]):
        ''' 根据id更新数据'''
        coll = self.get_collection(coll_name)
        res = coll.update_one({"_id": ObjectId(doc_id)}, {"$set": data})
        return res.modified_count

    def delete_by_id(self, coll_name, doc_id):
        ''' 根据ID删除数据 '''
        coll = self.get_collection(coll_name)
        res = coll.delete_one({"_id": ObjectId(doc_id)})
        return res.deleted_count

if __name__ == '__main__':
    # 创建mongo操作对象
    mongo_dao = MongoDBDao()
    # 新增数据
    new_id = mongo_dao.add_one('users', {'name':'潮奈1695','age':24})
    print('新增数据ID: ', new_id)
    # 查询数据
    print('查询数据: ', mongo_dao.get_by_id('users', new_id))