'''
定义字典
格式1  变量名称 = {key1:value1, key2:value2, ...}
格式2  变量名称2 = {} 空字典,
格式3  变量名称3 = dict()
'''

#构建一个有内容的字典
person = {'name':'小明',
          'age':19,
          'address':"上海市浦东新区张江镇",
          "sex":'男',
          'hobby':'篮球、足球、游泳'}
print(person)
print(type(person))

# 构建空字典
dict1 = {}
print(type(dict1))
print(dict1)
dict2 = dict()
print(type(dict2))
print(dict2)
print('*'*50)
# 遍历操作，将字典中的key-value对中的key依次赋值给for循环的临时变量
for key in person:
    print(key)
    # 根据key获取value
    print(person[key])
# 新增操作， 字典名称[key] = value
# 当key不存在，则将key和value拆入到字典中
person['salary'] = 35000
print(person)
# 修改，字典名称[key] = value1，如果key在字典中存在
# 则将value改为新的value1
person['age'] = 38
print(person)
# 删除某个元素
del person['salary']
print(person)

# 字典清空
person.clear()
print(person)
person = {'name':'小明',
          'age':19,
          'address':"上海市浦东新区张江镇",
          "sex":'男',
          'hobby':'篮球、足球、游泳'}

# 查找一个不存在的key，会引发异常
# print(person['salary'])

# 获取字典中所有的keys，返回以字典中的key构成的序列，可以理解为list类型
print(person.keys())
# 可以遍历
for key in person.keys():
    print(key)
print('x'*20)
# 获取字典中所有的values, 将字典中的value构成序列返回
# 可以粗略理解为列表，也就是可遍历
print(person.values())
for value in person.values():
    print(value)
print('*'*20)
# 获取字典中所有的items，将字典中的item构成序列返回
# 可以粗略理解为列表，也就是可便利
print(person.items())
for item in person.items():
    print(item)
    print(item[0])
    print(item[1])
    print('?'*30)
    # 元组拆包, key接受item[0],value接受item[1]
    key, value = item
    print(key)
    print(value)
print('*'*20)
for key, value in person.items():
    print(key)
    print(value)

'''
###  案例需求

给定一个字符串my_string，现在要求统计每个字符出现的次数: 
形成结果: {'字符':出现次数,'字符2':次数}
例如: 'abcdecf' ==> {'a':1,'b':1,'c':2,'d':1,'e':1,'f':1}
思路:
最开始弄一个空字典，key为字符，value为出现的次数
1. 如果字符没有在字典中，将字符和次数1插入字典
2. 如果字符在字典中，将字符的次数+1
3. 最后遍历字典，打印每个字符出现的次数
'''
str = 'abcdecf'
count_dict = {}
for char in str:
    # 如果char不在字典中
    if char not in count_dict:
        count_dict[char] = 1
        continue
    # 如果char在字典中
    count_dict[char] += 1

for key, value in count_dict.items():
    print(f'{key}出现了{value}次')