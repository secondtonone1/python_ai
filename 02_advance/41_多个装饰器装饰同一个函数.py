'''
多装饰器装饰同一个函数
'''

def check_login(func):
    def inner():
        print('检测用户是否登录(SSO)验证')
        func()
    return inner

def check_permission(func):
    def inner():
        print('检查用户是否具备报销权限财务系统权限()')
        func()
    return inner

# 多装饰器叠加
@check_login
@check_permission
def submit_reimbursement():
    print(f'提交报销申请(上传发票+填写金额)')

submit_reimbursement()