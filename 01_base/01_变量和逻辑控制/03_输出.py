'''
格式化输出
通过字符串拼接变量值的方式，进行输出，就叫做格式化输出
方式1 f-string
print(f'字符串{变量名}')
方式2 format模式
print('字符串{}'.format(变量名))
方式3 %占位符输出
print('字符串%格式' % 变量)
'''
name = 'zack'
age = 38
score = 95.555
num = 1
# 基础用法
print(f'姓名为:{name},年龄为:{age},学分为:{score}')
# 对小数进行控制，保留两位小数
print(f'姓名为:{name},年龄为:{age},学分为:{score:.2f}')
# 对整数进行补0,控制整数位数
print(f'姓名为:{name},学号为:{num:06d},年龄为:{age},学分为:{score:.2f}')

# format输出
print('姓名:{},年龄:{}'.format(name,age))
# format指定输出位置
print('年龄:{1},姓名:{0}'.format(name,age))
# format控制小数位数
print('成绩:{:.2f}'.format(score))

# %占位符
print('姓名:%s,年龄:%d,分数:%f' % (name,age,score))
print('姓名:%s,年龄:%d,分数:%.2f' % (name,age,score))

r'''
转义字符
\n 表示换行
\t 表示tab,制表符，表示4个空格
\  表示转义
" 表示字符串，注意不能被其他的双引号包裹，否则出错
' 表示字符串，注意不能被其他单引号包裹
'''
print('hello ,我是zack\n我爱编程')
print('hello ,我是zack\t我爱编程')
# 输出hello I'm zack
# 因为'是特殊字符，如果被单引号包裹，需要\进行转义
print('hello I\'m zack')
# 或者外部就用双引号包裹
print("hello I'm zack")
# 输出我爱"C++"
print('我爱"C++"')
# 用\转义
print("我爱\"C++\"")