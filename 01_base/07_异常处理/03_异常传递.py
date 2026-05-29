'''
异常会传递，如果不捕获，就会从最内层传递到最外层
'''
def func2():
    return 1/0

def func1():
    func2()

def main():
    try:
        func1()
    except Exception as e:
        print(f"异常为: {e}")
main()