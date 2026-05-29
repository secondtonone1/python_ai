'''
演示文件读写
'''

'''
1. file = open(文件路径, 模式, 编码)
file是文件对象，里面包含了文件描述符
模式 r 只读，如果文件不存在则报错
w 只写，如果文件不存在则创建，存在则清空并且覆盖写
a 追加，如果文件不存在则创建，存在则追加

2. file.read() 读取  file.write(内容)
3. file.close()
'''

'''
相对路径: 以.或者..开始的路径表示相对路径
.表示当前目录, ..表示上一级目录
./a.txt 表示当前目录下的a.txt文件
../b.txt 表示上一级目录的b.txt文件
绝对路径： linux环境下以/(根目录开始)的路径，就是绝对路径
/home/zack/a.txt 这个就是以/目录开始,home文件夹下zack文件夹下的a.txt
windows的绝对路径是以盘符开始的路径
"D:\\workspace\\github\\python_ai\\base\\06_文件\\01_文件读写.py"
'''
# 创建文件对象
with open('./example2.txt','w',encoding='utf-8') as f:
    f.write('我是恋恋风辰zack\n我的地球号1017234088，欢迎加群一起学习')

# 读取文件内容
with open('./example2.txt','r',encoding='utf-8') as f:
    # 读取所有行，每一行数据是列表的一个元素
    data_list = f.readlines()
    print(data_list)

# 读取文件
with open('./example2.txt','r',encoding='utf-8') as f:
    while True:
        # 按行读取，一次读取一行
        data = f.readline()
        if data:
            print(f'data is : {data}')
            continue
        # 走到这里说明读取的数据为空
        break

# 读取文件循环读取
with open('./example2.txt','r',encoding='utf-8') as f:
    # for 循环从文件中一次读取一行
    for line in f:
        print(f'data_line is : {line}')

# 按照列表多行写入
with open('./example3.txt','w',encoding='utf-8') as f:
    # 准备数据
    datas = ['llfc.club\n','gitbookcpp.llfc.club\n','代码理性到底，文字感性入骨\n']
    f.writelines(datas)
