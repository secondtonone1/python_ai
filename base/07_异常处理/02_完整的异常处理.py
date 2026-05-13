with open('a3.txt', 'w', encoding='utf-8') as f:
    f.write('hello')
    f.write('你好')

def total_exp_deal(filename, mode, encoding='utf-8'):
    try:
        # 可能出错的代码
        with open(filename,mode,encoding=encoding) as f:
            content = f.read()
    # 单独捕获文件不存在的异常
    except FileNotFoundError:
        print('错误，文件不存在')
    # 异常处理，通用的异常处理
    except Exception as e:
        print(f'发生错误: {e}')
    # 正常处理
    else:
        # 只有在try成功执行时才运行
        print(f'读取的内容{content}')
        print(f'文件读取成功，内容长度:{len(content)}')
    # 最终处理
    finally:
        # 无论异常还是正常
        print('文件操作完成')

total_exp_deal('a2.txt','r')
total_exp_deal('a.txt','r')
total_exp_deal('a3.txt','r')