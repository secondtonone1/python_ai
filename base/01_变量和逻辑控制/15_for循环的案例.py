'''
案例：用for循环实现用户登录

① 输入用户名和密码

② 判断用户名和密码是否正确（username='student'，password='python123'）

③ 登录仅有2次机会，超过2次会提示“登录失败，次数已用完”

分析：用户登陆情况有3种:

① 用户名错误(此时便无需判断密码是否正确) -- 登陆失败

② 用户名正确 密码错误 --登陆失败

③ 用户名正确 密码正确 --登陆成功
'''
# for循环要求循环两次，生成一个序列[0,1]这样从序列中遍历就可以遍历两次
# 定义一个bool变量，用来标记是否成功
b_success = False
for i in range(2):
    # print(i)
    name = input('请输入用户名: ')
    pwd = input('请输入您的密码: ')
    if name == 'student' and pwd == 'python123':
        print('恭喜您登录成功')
        # 当用户名和密码都正确，则设置b_success成功
        b_success = True
        break
    print(f'用户名或者密码错误，请继续输入...')
if b_success:
    print('登录成功后，可以继续进行其他的操作...')
else:
    print('两次机会用尽，登录失败')
