# 异常捕获
try:
    # 创建文件对象
    file_r = open('./example.txt', 'r', encoding='utf-8')
    # read()默认读取所有内容，也可以指定读取的大小read(1024)
    data = file_r.read()
    print(data)
    # 关闭文件
    file_r.close()
except ZeroDivisionError:
    print('文件不存在')
except Exception as e:
    print('兜底捕获异常')

# 做除法
def safe_divide(a,b):
    try:
        result = a / b
    except ZeroDivisionError:
        print('错误：不能除以0')
        # 异常返回的值
        return None
    # 正常返回的值
    return result

print(safe_divide(10,2))
print(safe_divide(10,0))

with open('a.txt','w',encoding='gbk') as f:
    f.write('hello world')
    f.write('你好')

# 捕获多个异常
def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print('错误，文件不存在')
    except PermissionError:
        print('错误，没有权限')
    except UnicodeDecodeError:
        print('错误，编码错误')

read_file('a.txt')

# 一次捕获多个异常，共同处理
def read_file2(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError):
        print('错误:文件访问失败')

read_file2('ab.txt')
read_file2('a.txt')

# 具体查看异常信息
def read_file3(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f'异常的类型为：{type(e)}')
        print(f'异常信息：{e}')

read_file3('a.txt')






