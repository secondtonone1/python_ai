'''
定义集合方式
方式1 空集合: empty_set = set()
方式2 包含元素的集合 my_set = {元素1, 元素}
'''

# 定义空集合
empty_set = set()
# 打印集合
print(empty_set)
print(type(empty_set))

# 定义空字典
empty_dict = {}
print(empty_dict)
print(type(empty_dict))

# 定义一个包含元素的集合
name_set = {'小明','小红','小刚','小明','小刚','小刚'}
print(name_set)
print(type(name_set))

# 遍历
for name in name_set:
    print(name)

# 增加元素
name_set = {'小明','小红','小刚'}
name_set.add('小强')
print(name_set)

# 删除元素
name_set.remove('小强')
print(name_set)

# 判断元素是否在集合中, in和not in
if '小明' in name_set:
    print('小明在集合中')
else:
    print('小明不在集合中')

# 判断元素不在集合中
if '小强' not in name_set:
    print('小强不在集合中')
else:
    print('小强在集合中')

"""
💡 题目：一个数组中除了两个数字只出现一次外，其他数字都出现两次。
       找出这两个只出现一次的数字。
输入: [4, 1, 2, 1, 2, 3, 5, 5]
输出: 3 和 4

思路：
1. 准备集合A和列表B，集合A用来存储出现的数字，集合B用来记录只出现过1次的数字
2. 将出现的数字和集合A判断，如果集合A中有数字，说明这个数字出现过，将数字从集合B
中删除。
如果A中没有这个数字，说明数字没出现过，将数字放入集合A和集合B
3. 最后循环结束，打印集合B，就是只出现一次的数字了
"""
num_list = [4, 1, 2, 1, 2, 3, 5, 5]
# 存储所有出现的数字
set_a = set()
# 存储只出现一次的数据
set_b = set()
for num in num_list:
    # num没有出现过
    if num not in set_a:
        set_a.add(num)
        set_b.add(num)
        continue
    # num出现过，则从set_b中移除该数字
    set_b.remove(num)

print('出现过1次的数字: ')
for num in set_b:
    print(num,end='\t')
print()