'''
演示带参数装饰器，根据操作类型记录不同的日志(公司审计系统)
'''

def audit(action_type):
    '''
    因为装饰器只能接受一个参数，所以考虑在装饰器外层再嵌套一层
    这个最外层的函数接受参数，返回装饰器的外层函数
    :param action_type: 装饰器的参数
    :return: 返回一个装饰器的外层函数
    '''
    def decorator(func):
        def inner(user, amount):
            # 通过闭包机制，捕获外层函数的变量
            if action_type == 'recharge':
                print('--[审计] 用户正在进行充值操作')
                return func(user, amount)

            if action_type == 'withdraw':
                print('--[审计] 用户正在进行提现操作')
                return func(user, amount)

            if action_type == 'transfer':
                print('--[审计] 用户正在进行转账操作')
                return func(user, amount)
        return inner
    return decorator

@audit('recharge')
def wallet(user,amount):
    print(f'{user} 账户变动金额: {amount}')
    return f'操作成功: {amount}'

print(wallet('Alice',100))