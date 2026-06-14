'''
演示like继承
'''

class Bird:
    def fly(self):
        print("i can fly")
# is 方式继承，Angle一定是Bird
class Angle(Bird):
    def fly(self):
        print('鹰会飞')
# like 方式继承， Go语言特性interface
class Plane:
    def fly(self):
        print('飞机也会飞')

def func_test_bird(bird:Bird):
    bird.fly()

if __name__ == '__main__':
    angle = Angle()
    func_test_bird(angle)
    plane = Plane()
    func_test_bird(plane)