'''
演示列表的查找操作
'''

'''
列表名[下标]  获取指定下标的元素
count()   统计指定数据在当前列表中出现的次数
index() 获取指定数据所在位置的下标
in 判断某个元素是否在列表中, 如果在则返回True
not in 判断某个元素是否不在列表中, 如果不在则返回True
'''
# 定义列表
name_list = ['小明','小红','小刚','小丽','小强','zack','Ray','Lucy','Lily','小丽']
# 1 index 查找方法，根据index传入的元素，获取其索引
index = name_list.index('zack')
print(index)

# 2 count 统计元素在列表中出现的次数
count = name_list.count('小丽')
print(count)

# 3 in和not in 判断是否存在或者不存在
if '小刚' in name_list:
    print('小刚在名字列表中')
else:
    print('小刚不在名字列表中')

if '刚子' not in name_list:
    print('刚子不在名字列表中')
else:
    print('刚子在名字列表中')

'''
append() 在列表后面添加元素
extend() 在列表的结尾追加数据，extend出传递的是一个序列，将这个序列的
每一个元素逐一添加到列表中
insert() 插入，在指定位置新增数据
两个列表相加 list1+list2，相当于将list2中的内容依次取出放入list1中
'''
name_list2 = ['小浩','小奇']
name_list.extend(name_list2)
print(name_list)
# 插入
name_list.insert(2,'吹风')
print(name_list)

list1 = [1,2,3,4,5]
list2 = [6,7,8,9]
list3 = list1 + list2
print(list3)

'''
元素删除
del 列表[下标] 删除指定下标的元素
列表.pop() 删除最后一个元素
列表.pop(索引) 根据索引删除元素
'''
del list3[-1]
print(list3)
del_num = list3.pop()
print(f'删除的数字是{del_num}')
print(f'list3 is {list3}')
del_num = list3.pop(2)
print(f'删除的数字是{del_num}')
print(f'list3 is {list3}')

'''
列表[索引下标] = 修改后的值, 根据索引下标，修改对应的元素，将元素修改为后面的值
reverse() 将数据序列进行倒叙排序
sort() 对列表序列进行排序   旧列表.sort(reverse=True)， 排序后就列表顺序改变
reverse = True 表示从大到小
reverse = False 表示从小到大
默认不写，就是从小到大
'''
# 修改
name_list[0] = '大明'
print(name_list)
# reverse反转
name_list.reverse()
print(name_list)
num_list = [6,1,0,5,2,7,6]
# 从小到大
num_list.sort()
print(num_list)
# 从大到小排序
num_list.sort(reverse=True)
print(num_list)

name_list = ['项羽','甄姬','王昭君']
index = 0
while index < len(name_list):
    print(name_list[index])
    index += 1
print('------------')

index = len(name_list)-1
while index >= 0:
    print(name_list[index])
    index -= 1
print('------------')
for name in name_list:
    print(name)

print('*'*50)
# for的逆序，[len(name_list)-1, len(name_list)-2, ... 0]
# range(len(name_list)-1, -1, -1)
for index in range(len(name_list)-1, -1, -1):
    print(index)
    print(name_list[index])

'''
列表嵌套，[[元素1,元素2],[元素3,元素4],[元素5,元素6]]
'''
class1 = ['项羽','兰陵王','安其拉']
class2 = ['naruto','sasiki','itachi']
class3 = ['张良','刘伯温','诸葛亮']
classes = [class1,class2,class3]
print(classes)
print('*'*20)
for ele in classes:
    print(ele)
    for sub_ele in ele:
        print(sub_ele)
# 断言classes[0][2]必然为安其拉
assert (classes[0][2] == '安其拉')
print(classes[0][2])