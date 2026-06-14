'''
演示多继承隐患
'''

'''
需求:
1. 定义一个汽车Car基类，构造方法__init__接受汽车的名字和颜色

2. 定义GasolineCar类，继承自Car, 实现__init__方法，接受参数名字，颜色
    以及充能方式
    实现run方法，输出耗油运行
    实现energy方法，输出默认使用燃油

3. 定义ElectricCar类, 实现__init__方法，接受参数名字，颜色
    以及充能方式
    继承自Car，实现run方法，输出耗电运行
    实现energy方法，输出默认使用电能

4. 定义HybridCar类，同时继承自ElectricCar,GasolineCar，
实现run方法，油电混动运行

5.  实例化一个HybridCar对象，调用energy以及run方法，看看输出

'''
# 1. 定义一个汽车Car基类，构造方法__init__接受汽车的名字和颜色
class Car(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color

# 2. 定义GasolineCar类，继承自Car, 实现__init__方法，接受参数名字，颜色
#     以及充能方式
class GasolineCar(Car):
    def __init__(self, name, color,energy_type):
        super().__init__(name, color)
        self.energy_type = energy_type

    def run(self):
        print('耗油运行')

    def energy(self):
        print('默认使用燃油')

# 3. 定义ElectricCar类, 实现__init__方法，接受参数名字，颜色
#     以及充能方式

class ElectricCar(Car):
    def __init__(self, name, color, energy_type):
        super().__init__(name, color)
        self.energy_type = energy_type

    def run(self):
        print('耗电运行')

    def energy(self):
        print('默认使用电能')

# 4. 定义HybridCar类，同时继承自ElectricCar,GasolineCar
class HybridCar(ElectricCar, GasolineCar):
    def __init__(self, name, color, energy_type):
        self.name = name
        self.color = color
        self.energy_type = energy_type

    def run(self):
        print('油电混动运行')


if __name__ == '__main__':
    # gc = GasolineCar('宝马','白色','燃油')
    # gc.run()
    # gc.energy()
    #
    # ec = ElectricCar('比亚迪','黑色','电能')
    # ec.run()
    # ec.energy()
    print(HybridCar.__mro__)
    hy_car = HybridCar('比亚迪','黑色','油电混动')
    hy_car.run()
    hy_car.energy()