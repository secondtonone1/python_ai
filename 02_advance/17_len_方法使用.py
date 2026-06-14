'''
演示new方法
'''
class MyList:
    def __init__(self,list_data):
        self.list_data =list_data
    # 返回列表的长度
    def __len__(self):
        return len(self.list_data)

if __name__ == '__main__':
    '''
    调用len会触发__len__
    '''
    my_list = MyList([1,2,3])
    print(len(my_list))
