'''
演示new方法
'''
class MyDict:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.dict = {'name':name,'age':age}

    def __getitem__(self,key):
        if key not in self.dict:
            return None
        return self.dict[key]

    def __setitem__(self,key,value):
        self.dict[key] = value

    def __delitem__(self,key):
        if key not in self.dict:
            return
        del self.dict[key]

    def __contains__(self,key):
        return key in self.dict

if __name__ == '__main__':
    my_dict = MyDict(name='zack',age=38)
    # 当一个对象当成字典根据key获取值使用的时候会触发getitem
    print(my_dict['name'])
    print(my_dict['age'])
    # 当一个对象当成字典，通过key修改或者添加value的时候触发setitem
    # 添加key和value
    my_dict['hobbies'] = ['run','read','games']
    # 修改key和value
    my_dict['age'] = 18
    print(my_dict['hobbies'])
    print(my_dict['age'])

    # 把一个对象当成字典，删除key和value会触发delitem
    del my_dict['hobbies']
    print(my_dict['hobbies'])

    # 当一个对象当成字典，判断key是否在对象中
    print('hobbies' in my_dict)