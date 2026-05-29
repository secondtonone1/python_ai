'''
演示循环break和continue操作
'''

'''
break是结束整个循环
continue是结束本次循环，继续下一次循环
'''
'''
老师批作业，一本一本批阅
如果批阅到第三本，发现是空白，中止批阅循环，使用break
'''
num = 1
while num <= 10:
    if num == 3:
        print(f'第{num}本为空白作业,结束批阅循环，退出循环')
        break
    print(f'老师正在批阅第{num}本作业')
    num += 1
print('循环结束')

'''
老师批作业，一本一本批阅
如果批阅到第三本发现有大量错误，跳过本次批阅，继续下一次批阅，批阅第4本，使用continue
直到循环结束
'''
print('#'*20)
# 作业本计数器
num = 1
while num <= 10:
    if num == 3:
        print(f'第{num}本有大量错误，跳过本次循环')
        # 更新计数器
        num += 1
        continue
    print(f'批阅第{num}本作业')
    num += 1

'''
死循环
while 条件判断永远为True，循环不会结束，将会一直进行
'''
while True:
    print('这是一个死循环......')