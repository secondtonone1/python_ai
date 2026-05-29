'''
### 案例需求（全新）

判断相邻元素的变化趋势

给定一个正整数数组，判断每一对相邻元素是“上升”“下降”还是“相等”，并输出结果列表

例如：
 输入: `[3, 5, 5, 2, 4]`
 输出: `['上升', '相等', '下降', '上升']`
'''

# 定义上一个元素
last = None
# 数字列表
num_list = [3, 5, 5, 2, 4]
# 存储结果的列表
res_list = []
# 从列表中获取元素赋值给cur
for cur in num_list:
    # 这是刚取出第一个元素
    if last == None:
        last = cur
        continue
    if cur < last:
        res_list.append('下降')
        last = cur
        continue
    if cur == last:
        res_list.append('相等')
        last = cur
        continue
    res_list.append('上升')
    last = cur

print('res_list:', res_list)

'''
找出列表中第一次出现的重复元素

给定一个列表，找到**第一个重复出现的元素**（只要出现第二次就算重复），并输出该元素

例如：
 输入: `[2, 3, 5, 3, 6, 5, 7]`
 输出: `3`
'''
src_list = [2,3,5,3,6,5,7]
# 记录取出来的元素
back_list = []
# 记录重复的元素
dupilicate_num = None

# 从src_list中取元素赋值给cur
for cur in src_list:
    # 如果cur在back_list说明重复了
    if cur in back_list:
        dupilicate_num = cur
        break
    # 如果不在back_list，那么就将该元素放入back_list中
    back_list.append(cur)
if dupilicate_num:
    print(f'重复元素为: ', dupilicate_num)
else:
    print('不存在重复元素')