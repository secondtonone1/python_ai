'''
同一个变量能存储不同类型的数据
'''
age = 100
print(type(age))
age = 3.14
print(type(age))
age = 'hello world'
print(type(age))

'''
int(x)   ---->将x转化为整数
float(x) ---->将x转化为浮点数
str(x)   ---->将x转化为字符串
eval(x)  ---->执行x字符串表达式，将x转化为对应的类型
'''
'''
需求：
提示用户输入商品名称，商品单价，商品数量
最后计算出总价，并且格式化输出
'''
product_name = input('请输入商品名称: ')
price_str = input('请输入商品单价: ')
count_str = input('请输入商品数量: ')
# 类型转换
price = float(price_str)
count = int(count_str)
# 计算总价
total_price = price * count
# 格式化输出结果
print(f'您购买了{product_name}, 单价为{price:.2f}元,'
      f'数量为{count}件,总价为:{total_price:.2f}')

'''
1. 字符串没办法和数值类型的数据进行加减除运算
2. 字符串和数值做乘法运算，不是做计算，而是将字符串复制n份拼接起来
'''
# name = 'zack'
# age = 38
# sum = name + age
print('*'*20)
print('1'*20)