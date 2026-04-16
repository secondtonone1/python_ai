'''
编写一个程序，计算嵌套元组中所有数字的总和。

例如：在嵌套元组 `((2,3,4),(3,5,7),(3,4,6))` 中，所有元素相加的结果为：

```
2+3+4+3+5+7+3+4+6 = 37
```

输出结果为：`37`
'''
# 嵌套元组
my_tuple = ((2,3,4),(3,5,7),(3,4,6))
# 定义一个变量用来存储总和
sum = 0
# 遍历
for cur in my_tuple:
    print(cur)
    for sub in cur:
        print(sub)
        sum += sub

print('累计求和的结果: ', sum)

'''
给定一个元组 `my_tuple`，里面包含 `2, 3, 4, 5, 6, 7, 8, 9, 10` 元素，
要求找出其中所有大于 5 的数字，并放入一个新列表中。

输出结果为：`[6, 7, 8, 9, 10]`
'''
print('*'*50)
my_tuple = (2, 3, 4, 5, 6, 7, 8, 9, 10)
res_list = []
for cur in my_tuple:
    #print(cur)
    if cur <= 5:
        continue
    res_list.append(cur)
print('res_list is : ', res_list)