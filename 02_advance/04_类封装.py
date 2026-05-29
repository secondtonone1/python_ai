'''
演示类的封装
'''

class Student:
    def __init__(self, name, score):
        self.name = name
        # __score为对象的私有属性
        self.__score = score
    # 类的方法可以访问私有属性
    def get_score(self):
        return self.__score

    def set_score(self, score):
        if score < 0 or score > 100:
            print('分数非法')
            return None
        self.__score = score
    # 私有方法
    def __introduce(self):
        print(f'我叫{self.name}, 我的分数{self.__score}')

    # 公有方法调用私有方法
    # 判断如果分数大于90才自我介绍
    def introduce(self):
        if self.__score  > 90:
            self.__introduce()

# 创建对象
zs = Student('张三',90)
print(zs.get_score())
print('😔'*50)
ls = Student('李四',100)
print(ls.get_score())
# 设置李四的分数-200
ls.set_score(-200)
print(ls.get_score())
# 私有方法无法在类外访问，因为Python无法像C++那样做到真正的私有隔离
# 所以它只不过将__introduce私有方法改了一个名字
# zs.__introduce()
# 查看类的方法
print(Student.__dict__)
# 发现__introduce被改为_Student__introduce
zs._Student__introduce()
# 查看所有的属性
print(zs.__dict__)
# 发现__score 改为_Student__score
print(zs._Student__score)
# 无法在类外直接访问__score
# print(zs.__score)
# 可以通过公有方法调用
ls.introduce()
