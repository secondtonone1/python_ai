def safe_read_file(filename):
    '''
    完整的安全读取文件的函数
    :param filename: 文件名
    :return: 返回读取的内容，可能为None
    '''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
    except FileNotFoundError:
        print(f'错误，文件{filename}不存在')
        return None
    except PermissionError:
        print(f'权限错误，没有读取文件的权限{filename}')
        return None
    except UnicodeDecodeError:
        print(f'错误，文件编码错误，尝试使用GBK编码')
        try:
            with open(filename, 'r', encoding = 'gbk') as f:
                content = f.read()
            return content
        except :
            return None
    except Exception as e:
        print(f'错误处理，错误为{e}')
        return None

print(safe_read_file('test.txt'))
print(safe_read_file('a.txt'))

def safe_write_file(filename, content):
    '''
    完整的安全文件写入函数
    :param filename: 文件名
    :param content: 写入的内容
    :return: True/False
    '''
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'写入成功{filename}')
        return True
    except PermissionError:
        print('权限不足')
        return False
    except Exception as e:
        print('错误，写入失败')
        return False

print(safe_write_file('C:\\Program Files (x86)\\VMwaretest.txt','hello world'))