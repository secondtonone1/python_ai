def read_file(filename):
    '''
    读取文件
    :param filename: 文件名
    :return: 返回读取的结果
    '''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print('读取文件异常, e is ', e)
        return None