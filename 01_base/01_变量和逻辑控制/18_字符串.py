'''
演示字符串基础逻辑
'''

'''
由单引号或者双引号，或者三个单引号，或者三个双引号括起来的都是字符串类型
'''

# 定义字符串
student_name1 = '黎明'
student_name2 = "李明"
print(student_name1, student_name2)
print(f'{type(student_name1)}, {type(student_name2)}')

# 可以使用三个双引号或者三个单引号括起来，就是字符串
str1 = '''
I love Python!
And you?
'''
str2 = """
I love Python!
And you?
"""
print(str1, str2)
print(type(str1), type(str2))

# 需求输出 It's a wonderful day
# 方式1，用双引号括起来这个单引号
msg = "It's a wonderful day"
print(msg)
# 方式2, 用转义字符\将'转化为普通字符
msg = 'It\'s a wonderful day'
print(msg)

# 需求输出 He said "It's a great"
# 思路1 用单引号将整个句子括起来，将内部的单引号通过\转义为普通的单引号
msg = 'He said "It\'s a great day"'
print(msg)

# 思路2 用双引号括起来整个句子，将内部的双引号用\转义为普通的双引号
msg = "He said \"It's a great day\""
print(msg)

'''
字符串的索引下标从0开始，到len-1结束
比如python这个字符串，下标就是从0开始，到5结束(长度为6)
'''
course = 'python'
print(course)
# 获取第一个字符
print(course[0])
# 获取h
print(course[3])

'''
演示切片操作
序列[start:end:step]
start表示开始的索引，end表示结束的索引，[start,end)左闭右开
1. 索引是从0开始的
2. 正索引从左到右，依次增加，0，1，2，3，4...
3. 负索引从右到左，绝对值依次增加，-1,-2,-3,-4,-5...
4. 步长正数就是从左向右，如果是负数就是从右向左
start可以省略，如果省略，并且step为正数，start就是从下标0开始
如果step为负数，start就是从下标-1开始
end可以省略，如果省略，并且step为正数，end就是最后一个元素的下标的下一个位置
如果step为负数，end就是第一个元素的前一个位置，所以也可以取到第一个元素。
step也可以省略，默认步长为1
'''
digits = '0123456789'
# 1. 从下标2开始到下标5结束，不包括下标5，步长为1
print(digits[2:5:1])
#2.只有结尾字符串切片，并且step为正数代表索引从0开始到结尾前一个位置
# start从0开始，stepe默认为1
print(digits[:5])
#3. 只有开头的字符串切片，step默认为1，end默认为结尾元素的下一个位置
print(digits[2:])
#4. 获取或者拷贝整个字符串,省略开始和结尾，步长也省略
print(digits[:])
print(digits[0::1])
# 调整步数，只截取偶数部分
print(digits[::2])
# 让字符串反转
print(digits[::-1])
# 从起始位置到结束位置都是负数
print(digits[-5:-1])
# 结束位置设置为-1，截取到最后一个元素的前面部分
print(digits[0:-1])

'''
案例2：给定一个图片的名称为"photo.jpg"，代码实现获取这个图片的名称(photo)以及这个图片的后缀(.jpg)。

分析：

  * ① 建议先获取点号的位置（目前还未学习，只能一个一个数）
  * ② 从开头切片到点号位置，得到的就是文件的名称
  * ③ 从点号开始切片，一直到文件的结尾，则得到的就是文件的后缀
'''
# 记录.的索引
index = 5
str = "photo.jpg"
# 文件名
name = str[:5]
# 后缀名
suffix = str[5:]
print(f"文件名为:{name},后缀名为{suffix}")

'''
字符串查找
索引 = 字符串.find(子串)
如果字符串中包含子串，则find返回子串在字符串中的位置(索引)
如果字符串中不包含子串，则find返回-1

索引 = 字符串.index(子串)
如果字符串中包含子串，则index返回子串在字符串中的位置(索引)
如果字符串中不包含子串，则index抛出异常，程序崩溃

'''
# 定义一个字符串
message = 'welcome to Python programming, Python is great'
# 查找Python子串是否出现在字符串中
sub_str = 'Pythons'
position = message.find(sub_str)
if position == -1:
    print(f'{sub_str} not in {message}')
else:
    print(f'{sub_str} in {message}, index is {position}')

'''
input输入一个文件名称，求.的索引下标
'''
# file_name = input('请输入文件名: ')
# dot_pos = file_name.find('.')
# if dot_pos == -1:
#     print('未找到., 文件格式有误')
# else:
#     print(f'找到.的位置{dot_pos}')
#     print(f'文件名: {file_name[:dot_pos]}')
#     print(f'后缀名: {file_name[dot_pos:]}')

fruits = 'apple, banana, orange'
# 判断apple是否出现在fruits中
pos = fruits.index('apple')
print(f'apple的位置: {pos}')

pos = fruits.index('orange')
print(f'orange的位置: {pos}')

# 找不到会抛出异常，ValueError
# pos = fruits.index('oranges')
# print(f'orange的位置: {pos}')

'''
字符串替换
1. 替换后的全部字符串 = 原来的字符串.replace(要替换的原子串,替换后的子串,替换的次数)
替换次数如果不传递，那么就全部替换
原来的字符串不会被修改，只是会返回一个新的修改后的字符串
'''
text = 'I love Java programming and Java is powerful'
# 把字符串中所有的Java替换成Python
new_text = text.replace('Java', 'Python')
print(new_text)
# 只替换1次
new_text2 = text.replace('Java', 'Python',1)
print(new_text2)
# 把and替换为&
new_text3 = text.replace('and', '&')
print(new_text3)

'''
字符串切割
列表 = 字符串.split(分隔符)
列表里存储的就是字符串按照分割符切割后的多个子串。
'''
# 示例：按照逗号分隔日期
date_str = '2024-03-15'
# 将data_str按照-切割，切割后的子串存储到列表中
date_list = date_str.split('-')
print(date_list)

# 邮箱切割
email = 'user@example.com'
parts = email.split('@')
print(f'用户名为{parts[0]}')
print(f'邮箱:{parts[1]}')

'''
拼接后的字符串 = 连接符.join(列表)
将列表中的每个元素按照连接符进行拼接，最后汇总为一个拼接后的字符串
'''
fruits = ['apple', 'banana', 'orange']
# 使用-连接列表中的内容，返回新的字符串
result = '-'.join(fruits)
print(result)

words = ['Hello','Python','World']
words = '.'.join(words)
print(words)

'''
案例需求
生成一个6位随机验证码，要求包含大写字母、小写字母和数字的组合。
思路:
1. 将所有的大写字母，小写字母，数字序列都拼成一个完整的字符串
2. 进行随机抽取，从完整的字符串中随机抽取一个字符
random.randint(开始数字，结束的数字) 可以从开始的数字到结束的数字之间随机抽取一个数字
范围为[开始数字，结束数字]
可以利用上面的函数随机出一个索引，再根据索引获取字符即可
3. 将字符拼接成结果字符串
'''
import random
# 获取最后验证码的长度
length = 6
# 定义一个变量存储最后的验证码
codestr = ''
# 所有的大写字母序列
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'

# 合并所有的字符串
all_charts = uppercase + lowercase + digits
# 获取字符串总长度
total_len = len(all_charts)
# 随机选取一个数字，作为索引，将来根据这个索引获取字符
rand_index = random.randint(0,total_len-1)
print(f'rand_index: {rand_index}')
# 根据索引获取字符
print(f'rand_char: {all_charts[rand_index]}')
# 通过for循环获取多个字符，每个字符进行拼接，作为最后的验证码
for i in range(6):
    # 随机选取一个数字，作为索引，将来根据这个索引获取字符
    rand_index = random.randint(0, total_len - 1)
    print(f'rand_index: {rand_index}')
    # 根据索引获取字符
    print(f'rand_char: {all_charts[rand_index]}')
    codestr += all_charts[rand_index]

print(f'验证码为{codestr}')