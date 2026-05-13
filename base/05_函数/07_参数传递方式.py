'''
演示参数传递的几种方式
'''

'''
位置传参
'''
def pick_item(user, item, num):
    '''
    捡物品的函数
    :param user: 捡东西的人
    :param item: 捡什么东西
    :param num:  捡起物品的数量
    :return: str
    '''
    return f'用户【{user}】 捡起【{num}】个物品【{item}】'

print(pick_item('zack','流光星陨刀',20))

'''
关键字传参
调用方式
函数名(形参1=实参1,形参2=实参2)
'''
print(pick_item(user='zack',item='无影剑',num = 20))

'''
默认值参数
函数定义时设定一个默认值
'''
def hard_challenge(user, item, num=1):
    '''
    演示游戏中深渊挑战掉落
    :param user: 用户名
    :param item: 物品
    :param num: 数量
    :return: str
    '''
    return f'用户【{user}】挑战深渊，掉落物品【{item}】,数量为【{num}】'

print(hard_challenge('llfc','阿甘左的浪人长剑',20))
print(hard_challenge('llfc','阿甘左的浪人长剑'))

'''
可变位置参数
不定长位置参数
不定长元组参数
都是同一个意思
'''
def hard_challenge_args(*args):
    '''
    深渊挑战
    :param args: 是一个元组
    :return: str
    '''
    return f'用户【{args[0]}】挑战深渊，掉落物品【{args[1]}】,数量为【{args[2]}】'

# 将'llfc','GSD的短刀',20打包成元组('llfc','GSD的短刀',20)
print(hard_challenge_args('llfc','GSD的短刀',20))

'''
可变的关键字参数
不定长关键字参数，不定长字典参数
'''
def hard_challenge_kwargs(**kwargs):
    '''
    深渊挑战
    :param kwargs: 是一个字典
    :return: str
    '''
    return f'用户【{kwargs['name']}】挑战深渊，掉落物品【{kwargs['item']}】,数量为【{kwargs['num']}】'

# 函数调用时，会将形参和实参打包成字典传递给kwargs
'''
函数调用时，将name='zack',item='魔剑阿波菲斯',num=10
自动打包成字典
{
    'name': 'zack',
    'item':'魔剑阿波菲斯',
    'num':10
}
'''
print(hard_challenge_kwargs(name='zack',item='魔剑阿波菲斯',num=10))

'''
万能函数
def func(*args, **kwargs):
    # args是一个元组, kwargs是一个字典
    pass
'''

def func(*args, **kwargs):
    # args是一个元组, kwargs是一个字典
    print('元组信息如下:')
    for arg in args:
        print(arg)
    print('字典信息如下:')
    for k,v in kwargs.items():
        print(f'{k}:{v}')

tuple_data = (1,2,3,4,5)
dict_data = {'name':'zack','age':25}
# 将(1,2,3,4,5)打包成一个元组((1,2,3,4,5),)
func(tuple_data)
# 将{'name':'zack','age':25}打包成元组({'name':'zack','age':25},)
func(dict_data)
# *tuple_data将(1,2,3,4,5)拆包 , 拆成多个位置参数1,2,3,4,5
# 参数1,2,3,4,5会被自动打包成元组传递给args,所以args=(1,2,3,4,5)
func(*tuple_data)
# **dict_data是将字典拆包，拆成关键字传参name='zack',age=25
# 再将name='zack',age=25进行打包，生成{'name':'zack','age':25}赋值给kwargs
func(**dict_data)

# 通过位置参数和关键字参数传参, 将1,2,3,4,5打包成元组(1,2,3,4,5)赋值给args,
# 将name='zack',age=25打包成{name='zack',age=25}赋值给kwargs
func(1,2,3,4,5,name='zack',age=25)

# 通用传参，将元组和字典拆包后分别传给函数的形参，等价于上面
func(*tuple_data, **dict_data)