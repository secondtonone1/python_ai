'''
演示图书管理系统开发
'''

'''
思路:
1. 定义图书类，属性 书名，作者，编号，数量
2. 定义图书管理类，管理图书，将图书放入字典中，
key为图书编号，value为这个字典
3. 在图书管理类中添加各种方法
4. 将图书信息写入文件
5. 将文件内容加载到内存中
'''
import json
import os

class Book:
    def __init__(self,title,author,price,isbn,count):
        self.title = title
        self.author = author
        self.price = price
        self.isbn = isbn
        self.count = count

    def to_dict(self):
        return {
            'book_id': self.isbn,
            'name': self.title,
            'author': self.author,
            'price': self.price,
            'count': self.count
        }
    @staticmethod
    def from_dict(book_dict):
        return Book(
            title=book_dict['name'],
            author=book_dict['author'],
            price=book_dict['price'],
            isbn=book_dict['book_id'],
            count=book_dict['count']
        )

class BookManager:
    instance = None
    def __new__(cls,file_path):
        if BookManager.instance is None:
            BookManager.instance = super().__new__(cls)
        return BookManager.instance

    def __init__(self,file_path):
        self.books = {}
        self.file_path = file_path
        self.__load_from_file()

    def __load_from_file(self):
        if not os.path.exists(self.file_path):
            print('文件不存在，暂无数据')
            return
        with open(self.file_path,'r',encoding='utf-8') as f:
            # data是一个列表，每个元素是字典
            data = json.load(f)

        self.books = {item['book_id']:Book.from_dict(item) for item in data}
        print('图书信息已经加载')

    def showmenu(self):
        while True:
            print('*'*10,'图书馆里系统','*'*10)
            print('1.添加图书')
            print('2.删除图书')
            print('3.修改图书信息')
            print('4.根据编号查看图书信息')
            print('5.将图书信息存储到本地')
            print('6.通过页码查看图书列表')
            print('7.输入quit退出系统')
            input_num = input('请输入您的操作编号: ')
            if input_num == '7' or input_num == 'quit':
                print(f'系统退出')
                break

            if input_num == '1':
                self.add_book()
                continue

            if input_num == '2':
                self.del_book()
                continue

            if input_num == '3':
                self.modify_book()
                continue

            if input_num == '4':
                self.check_book()
                continue

            if input_num == '5':
                self.save_to_file()
                continue

            if input_num == '6':
                self.show_list()
                continue

            print('非法操作，请继续!!!')

    def add_book(self):
        book_id = input('请输入图书编号: ')
        count = int(input('请输入录入数量: '))
        name = input('请输入书名: ')
        author = input('请输入作者: ')
        price = float(input('请输入价格: '))
        book = Book(title=name,author=author,
                    price=price,isbn=book_id,count=count)
        self.books[book_id] = book
        print('图书添加成功!!!')

    def __find_book_by_id(self,book_id):
        if book_id not in self.books:
            print('没有找到该图书!')
            return None
        return self.books[book_id]

    def del_book(self):
        book_id = input('请输入要删除的图书编号: ')
        book = self.__find_book_by_id(book_id)
        if not book:
            return
        del_count = int(input('请输入删除的数量: '))
        if del_count < book.count:
            book.count -= del_count
            print('图书数量删除成功')
            return

        del self.books[book_id]
        print('该图书已经全部删除')

    def check_book(self):
        book_id = input('请输入要删除的图书编号: ')
        book = self.__find_book_by_id(book_id)
        if not book:
            return

        print(f'图书信息:\n书名:{book.title}\n'
              f'作者:{book.author}\n'
              f'价格:{book.price}\n'
              f'编号:{book.isbn}\n'
              f'数量:{book.count}')

    def modify_book(self):
        book_id = input('请输入要删除的图书编号: ')
        book = self.__find_book_by_id(book_id)
        if not book:
            return

        new_name = input('请输入要改成的名字: ')
        new_price = float(input('请输入要改成的价格: '))
        new_author = input('请输入图书的作者: ')
        new_count = int(input('请输入图书的数量: '))
        book.title = new_name
        book.author = new_author
        book.price = new_price
        book.count = new_count
        print(f'图书信息修改成功:\n')

    def show_list(self):
        if not self.books:
            print('暂无图书信息')
            return

        page = int(input('请输入查看的页码: '))
        page_size = 5
        start = (page-1)*page_size
        end = start+page_size
        book_list = list(self.books.values())
        page_books = book_list[start:end]
        if not page_books:
            print('该页没有数据')
            return

        for book in page_books:
            print(
                f"编号：{book.isbn} | "
                f"书名：{book.title} | "
                f"作者：{book.author} | "
                f"价格：{book.price} | "
                f"数量：{book.count}"
            )

    def save_to_file(self):
        data = [book.to_dict() for book in self.books.values()]
        print(data)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            # 参1必须是列表，字典，字符串，正数，浮点，bool，None Python自带的内置类型
            # 参2是要写入的文件
            # 参3是中文是否需要转义
            # 参4 是否格式化json，美观输出
            json.dump(data,f,ensure_ascii=False,indent=4)
        print('图书信息已保存')



if __name__ == '__main__':
    m = BookManager('./book_datas/books.json')
    m.showmenu()
    #m2 = BookManager()
    #print(f'm is m2 : {m is m2}')



