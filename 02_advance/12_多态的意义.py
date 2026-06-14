'''
演示多态的意义
'''

'''
抽象方法，就是方法中没有具体实现，只写pass
抽象类，就是这个类中只有抽象方法
'''
# 抽象类
class NoteBook:
    # 笔记本显示功能
    def show(self):
        pass
    # 笔记本利用cpu计算
    def cpu_compute(self):
        pass
    # 笔记本利用gpu计算
    def gpu_compute(self):
        pass
    # 笔记本风扇散热
    def fan_heating(self):
        pass

# 子类继承抽象了
class ASUSNoteBook(NoteBook):
    def show(self):
        print('华硕电脑高清屏幕显示')
    def cpu_compute(self):
        print('华硕电脑CPU计算能力强悍')
    def gpu_compute(self):
        print('华硕电脑GPU计算能力强悍')
    def fan_heating(self):
        print('华硕电脑风扇散热能力强悍')

# 定义测试平台的测试函数
def work_test_note_book(note_book : NoteBook):
    # 测试show方法是否实现
    note_book.show()
    # 测试cpu_compute方法是否实现
    note_book.cpu_compute()
    # 测试gpu_compute方法是否实现
    note_book.gpu_compute()
    # 测试fan_heating方法是否实现
    note_book.fan_heating()

class ZackNoteBook(NoteBook):
    def show(self):
        print('Zack电脑屏幕高清显示')

if __name__ == '__main__':
    asus = ASUSNoteBook()
    work_test_note_book(asus)
    print('😀'*50)
    zack_note_book = ZackNoteBook()
    work_test_note_book(zack_note_book)