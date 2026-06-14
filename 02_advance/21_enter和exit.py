'''
演示enter和exit操作
'''

class MyContext:
    def __enter__(self):
        print('进入with代码块')
        return '资源对象'

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''

        :param exc_type: 异常类型
        :param exc_val: 异常值
        :param exc_tb:
        :return:
        '''
        print('退出 with')
        print('异常类型: ', exc_type)
        print('异常值: ', exc_val)

if __name__ == '__main__':
    with MyContext() as resource:
        print(resource)