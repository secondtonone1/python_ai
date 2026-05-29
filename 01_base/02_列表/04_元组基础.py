# 定义一个元组
one_tuple = (1,)
print('one_tuple: ', one_tuple)
print('type(one_tuple): ', type(one_tuple))
# 整数
one_num = (1)
print('one_num: ', one_num)

# 定义元组，存储不同类型的数据
user_tuple = ('小明','小红','小刚',20,30,40,True,False)
print('user_tuple: ', user_tuple)
print('type(user_tuple)',type(user_tuple))

# 获取元素，和list一致
print(user_tuple[0])
print(user_tuple[1])
print(user_tuple[2])

# 遍历
for item in user_tuple:
    print(item)
# 获取某个元素在元组中的索引
print(user_tuple.index(True))
# 获取某个元素出现了几次
print(user_tuple.count('小刚'))
# 获取元组的长度，元组内元素的个数
print(len(user_tuple))