'''
银行存款案例
'''

class BankAccount:
    def __init__(self, owner,balance=0):
        # 账户
        self.__owner = owner
        # 余额
        self.__balance = balance

    # 存款
    def deposit(self,amount):
        if amount <=0 :
            print(f'存款金额必须大于0')
            return
        # 存款
        self.__balance += amount

    # 取款
    def withdraw(self,amount):
        if amount <= 0:
            print(f'取款金额必须大于0')
            return

        # 判断余额是否充足
        if amount > self.__balance:
            print(f'取款的金额必须大于余额')
            return
        # 扣款
        self.__balance -= amount

    # 获取账号名
    def get_owner(self):
        return self.__owner

    #获取余额
    def get_balance(self):
        return self.__balance

    # 打印账户名和存取款信息
    def show_info(self):
        print(f'账户名: {self.__owner}, 余额: {self.__balance}')

if __name__ == '__main__':
    account = BankAccount('zack',1000)
    account.show_info()
    account.deposit(100)
    account.show_info()
    account.withdraw(300)
    account.show_info()
    account.withdraw(900)
    account.show_info()