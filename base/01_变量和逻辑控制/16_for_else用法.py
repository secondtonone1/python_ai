'''
演示for else用法
'''

'''
基本语法
for 临时变量 in 序列:
    循环逻辑
else:
    for循环正常结束的逻辑
    
正常结束:
for循环遍历次数用尽，continue也包括在正常结束的范围
非正常结束：
break, 程序触发异常
'''
str = 'python'
for i in str:
    if i == 'h':
        print('遇到h强制结束循环')
        break
    print(i)
else:
    print('循环正常结束后执行此处代码')
print('#'*50)
str = 'python'
for i in str:
    if i == 'h':
        print('遇到h不打印')
        continue
    print(i)
else:
    print('循环正常结束后执行此处代码')
print('#'*50)

for i in range(6):
    print(i)
else:
    print('循环正常结束')
print('#'*50)


