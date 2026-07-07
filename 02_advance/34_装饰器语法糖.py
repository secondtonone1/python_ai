'''
演示装饰器语法糖
'''

# 定义装饰器
def check(fn):
    def inner():
        print('验证登录')
        fn()
    return inner

# 相当于 comment = check(comment)

@check
def comment():
    print('发表评论')

comment()