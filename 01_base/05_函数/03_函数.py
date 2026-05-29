'''
演示函数用法
'''

'''
函数先定义再调用
定义:
def func(形参1,形参2,形参3,...):
    函数体
    return 返回值

func如果没有返回值，默认返回None, 相当于return None
函数定义的时候这个参数，叫做形式参数，简称形参

调用:
res = func(实参1, 实参2, 实参3)
res接受func返回值
函数调用时传递给函数的参数叫做实际参数，简称实参
'''
# 定义一个函数,捡道具
def pick_item():
    '''
    这个函数是捡道具的函数
    :return: None
    '''
    print('捡到1个道具!')
# 调用函数
pick_item()
pick_item()
pick_item()

# 定义一个捡道具带参数的函数
def pick_item2(item_name):
    '''
    捡道具函数
    :param item_name: 道具的名字
    :return: None
    '''
    print(f'捡到了【{item_name}】')

pick_item2('无影剑')
pick_item2('墨竹手镯')
pick_item2('骨戒')

# 设定背包容量
bag_capacity = 100
# 当前的物品的数量
current_count = 0

def pick_item3(item_name):
    '''
    捡起道具的函数
    :param item_name: 道具的名字
    :return: True表示捡起成功, False表示捡起失败
    '''
    global current_count
    if current_count >= bag_capacity:
        # 如果物品数量超过或者等于背包容量，那么直接返回False
        return False
    current_count  =  current_count +  1
    print(f'捡到了【{item_name}】!背包进度: {current_count}/{bag_capacity}')
    return True

result = pick_item3('魔剑-阿波菲斯')
if result:
    print('捡道具成功')
else:
    print('背包已满，无法获取')

pick_item3('无影剑雷诺')
if result:
    print('捡道具成功')
else:
    print('背包已满，无法获取')

pick_item3('边境荒火')
if result:
    print('捡道具成功')
else:
    print('背包已满，无法获取')

def return_value():
    return 1
    # 不会走到return 2，因为return 1函数结束了
    return 2

print(return_value())

def return_values():
    # 返回多个值，按照元组返回
    return 1,2

value = return_values()
print(value)
print(type(value))

def get_values(num1,num2):
    acc = num1*num2
    div = 0
    if num2 != 0:
        div = num1 / num2
    add = num1 + num2
    sub = num1 - num2
    return acc,div, add, sub
# 元组拆包
acc, div, add, sub = get_values(10,5)
print(acc, div, add, sub)