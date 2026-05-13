'''
文件偏移量
'''

'''
演示文件偏移操作
'''
with open('./example.txt','r',encoding='utf-8') as f:
    # tell()获取当前文件指针的位置,这是按照字节统计的
    print(f'文件开始的偏移量', f.tell())
    # 读取10个字符
    content = f.read(10)
    print(f'读取的内容: {content}')
    # 中文可能是3~6个字节
    print(f'当前文件偏移量{f.tell()}')
    # 回到头部
    f.seek(0)
    # 读取10个字符
    content = f.read(10)
    print(f'读取的内容: {content}')
    # 从开头移动6字节
    f.seek(6,0)
    content = f.read(8)
    print(f'读取内容: {content}')
    # 将文件指针移动到末尾，2表示文件末尾，1表示当前位置
    f.seek(0,2)
    # 因为文件指针已经移动到末尾，所以f.tell获取的是文件的大小
    file_size = f.tell()
    print('文件总大小为：',file_size)
