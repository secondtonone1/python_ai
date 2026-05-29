'''
演示双层循环实现九九乘法表
'''

'''
双层循环，如果内层循环使用了break，break只能跳出
它所在的循环，也就是内层循环
'''

'''
需求：
实现九九乘法表
思路:
1. 变量row控制行号,row从1到9结束,[1,9]
2. 变量col控制列号，col从1开始回到当前行号结束，[1,row]
3. 用外层循环控制行号的变化，内层循环控制列号的变化
for row in range(1,10):
    for col in range(1,row+1):
        pass
'''
for row in range(1,10):
    for col in range(1,row+1):
        # print(f'当前行号{row},当前列号{col}')
        print(f'{col} * {row} = {row * col}',end='\t')
    # print()默认输出换行符
    print()

print('#'*100)
'''
要求九九乘法表最多只输出到第3列
思路：
col为4的时候结束内层循环即可，外层循环继续
'''
for row in range(1,10):
    for col in range(1,row+1):
        # print(f'当前行号{row},当前列号{col}')
        print(f'{col} * {row} = {row * col}',end='\t')
        # 当col为4的时候结束内层循环，跳转到外层循环
        if col == 4:
            # break只能跳出它所在的循环(离他最近的循环)
            break
    # print()默认输出换行符
    print()
print('#'*100)