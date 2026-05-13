# 从datatools导出processor, reader函数
from datatools import processor, reader, writer

def main():
    write_lens = writer.write_file('data.txt', '这是全栈式学习资料文档:\n'
                                              'https://www.yuque.com/lianlianfengchen-cvvh2')
    # 写入失败直接返回
    if not write_lens:
        return

    # 写入成功
    print('写如成功')
    # 读取文件
    data = reader.read_file('data.txt')
    if not data:
        print('读取文件失败')
        return

    print('读取成功，读取的数据为', data)

if __name__ == '__main__':
    main()



