'''
演示静态方法
'''
class MathTool:
    @staticmethod
    def add(a,b):
        return a+b

print(MathTool.add(1,2))