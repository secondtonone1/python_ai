'''
读写json
'''

'''
import json
# 从文件中读取json字符串加载成json对象（字典），反序列化
json对象 = json.load(json文件)
# 将json对象（字典）写入文件中 ,叫做序列化
json.dump(json对象,文件)
'''
import json

def write_json(filename, data):
    '''

    :param filename: filename 文件名字
    :param data: json格式的对象，理解为字典
    :return:
    '''
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_json(filename):
    '''

    :param filename: 文件的名字
    :return: 字典，json对象
    '''
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    data_dict = {
        'name':'zack',
        'age':22,
        'score':88
    }

    write_json('data.json', data_dict)
    data = read_json('data.json')
    print(data)
    print(type(data))
