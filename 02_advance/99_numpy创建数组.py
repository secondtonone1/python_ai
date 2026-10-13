import numpy as np

def create_array():
    # 基于列表创建数组
    arr1 = np.array([1,2,3,4], dtype = np.int64)
    print(f'arr1: {arr1}')
    print(f'arr1.shape: {arr1.shape}')
    print(f'arr1.ndim: {arr1.ndim}')
    print(f'arr1.size: {arr1.size}')
    print(f'arr1.dtype: {arr1.dtype}')
    print(f'arr1.itemsize: {arr1.itemsize}')
    print(f'arr1.data: {arr1.data}')

    arr2 = np.array([[1,2,3],[4,5,6]], dtype = np.int64)
    print(f'arr2: {arr2}')
    print(f'arr2.shape: {arr2.shape}')
    print(f'arr2.ndim: {arr2.ndim}')
    print(f'arr2.size: {arr2.size}')
    print(f'arr2.dtype: {arr2.dtype}')
    print(f'arr2.itemsize: {arr2.itemsize}')
    print(f'arr2.data: {arr2.data}')

    # 创建全零数组
    arr3 = np.zeros((2,3))
    print(f'arr3: {arr3}')

    # 创建全1数组
    arr4 = np.ones((2,3))
    print(f'arr4: {arr4}')
    # 填充指定数据的数组
    arr5 = np.full((2,3),fill_value = 5)
    print(f'arr5: {arr5}')
    # 创建单位矩阵
    arr6= np.eye(3)
    print(f'arr6: {arr6}')
    # 创建空数组
    arr7 = np.empty((2,2))
    print(f'arr7: {arr7}')

    # 根据序列创建数组
    arr8 = np.arange(0,10,2)
    print(f'arr8: {arr8}')
    # 创建线性数组
    arr9 = np.linspace(0,1,5)
    print(f'arr9: {arr9}')

    # 随机数组创建
    # 设置随机种子
    np.random.seed(42)
    # 均匀分布[0,1)
    arr10 = np.random.rand(2,3)
    print(f'arr10: {arr10}')
    # 创建正态分布
    arr11 = np.random.randn(3,3)
    print(f'arr11: {arr11}')

    # 创建随机整数构成的数组,[0,10)区间选择随机整数
    arr12 = np.random.randint(0,10,size=(2,3))
    print(f'arr12: {arr12}')


def slice_array():
    arr = np.array([[1,2,3],[4,5,6],[7,8,9]])
    # 获取第0维度的第一个元素，相当于获取第0行
    print(f'arr: {arr[0]}')
    # 获取第0维度第0个元素和第1维度第1个元素
    # 相当于获取第0行第1列
    print(f'arr[0,1]: {arr[0,1]}')
    # 等价写法
    print(f'arr[0][1]: {arr[0][1]}')
    # 切片操作，获取第0维度中下标从0开始到2结束不包括2
    # 获取第1维度中下标从1开始，到所有元素结束
    # 相当于获取行0~1, 列1到末尾
    print(f'arr[0:2,1:]: {arr[0:2,1:]}')
    # 获取所有行，第0列的数据
    print(f'arr[:,0]: {arr[:,0]}')
    # 布尔索引, 将arr转化为mask布尔数组
    mask = arr > 5
    print(f'mask: {mask}')
    # 根据bool数组筛选指定元素，True的才能筛选出来
    print(f'arr[mask]: {arr[mask]}')

    # 花式索引
    # 获取第0行第1列的元素，以及第2行第0列的元素构成数组
    print(f'arr[[0,2],[1,0]]: {arr[[0,2],[1,0]]}')

# 广播机制
def broad_cast():
    a = np.array([1,2,3])
    b = np.array([4,5,6])

    # 逐个元素计算
    print(f'a + b: {a + b}')
    print(f'a * b: {a * b}')
    print(f'a / b: {a / b}')
    print(f'a // b: {a // b}')
    print(f'a - b: {a - b}')
    print(f'a ** 2: {a ** 2}')
    '''
    1. `*`：**元素对元素**，形状必须一模一样；
    2. `@`：
       - 一维向量：**点积求和**，长度相等即可；
       - 二维矩阵：**标准矩阵乘法**，前列 = 后行。
    '''
    # 矩阵乘法
    print(f'a @ b: {a @ b}')
    # shape(2,3)
    c = np.array([[1,2,3],[4,5,6]])
    # shape(2,3)
    d = np.array([[1,2,3],[4,5,6]])
    # 对于2维数组，无法进行矩阵相乘，因为形状不匹配
    # print(f'c @ d: {c @ d}')
    d2 = d.reshape(3,2)
    print(f'd2:\n{d2}')
    # 矩阵相乘, shape(2,3) @ shape(3,2) = shape(2,2)
    print(f'c@d2: {c@d2}')
    # shape(2,3)
    arr1 = np.array([[1,2,3],[4,5,6]], dtype = np.int64)
    # shape(1,3)
    arr2 = np.array([[1,2,3]],dtype = np.int64)
    print(f'arr1+arr2: {arr1+arr2}')

def reshape_array():
    arr = np.arange(6)
    print(f'arr: {arr}')
    print(f'arr.shape: {arr.shape}')
    print(f'arr.reshape((2,3)):\n{arr.reshape((2,3))}')
    arr1 = arr.reshape((2,3))
    print(f'arr1: {arr1}')
    arr2 = arr1.flatten()
    print(f'arr2: {arr2}')
    arr3 = arr1.ravel()
    print(f'arr3: {arr3}')

    # 转置
    arr4 = arr1.T
    arr5 = np.transpose(arr4)
    print(f'arr5: {arr5}')
    print(f'arr4: {arr4}')

    # 拼接

    a = np.array([[1,2],[3,4]])
    print(f'a: {a}')
    b = np.array([[5,6]])
    # 按照第0维拼接，相当于按照行拼接
    c = np.concatenate((a,b),axis = 0)
    print(f'c: {c}')
    # 按照第1维度拼接，相当于按照列拼接
    d = np.concatenate((a,b.T), axis = 1)
    print(f'd: {d}')

    # 按照none展平后拼接
    e = np.concatenate((a,b), axis = None)
    print(f'e: {e}')

    # 垂直堆叠
    f = np.vstack((a,b))
    print(f'f: {f}')

    # 水平堆叠
    g = np.hstack((a,b.T))
    print(f'g: {g}')

    # 分割
    h = np.split(arr,3)
    print(f'h: {h}')

def math_array():
    arr = np.array([[1, 2], [3, 4]])
    # 按照第0维求和
    arr1 = np.sum(arr, axis = 0)
    print(f'arr1: {arr1}')

    # 按照列求和，第1维求和
    arr2 = np.sum(arr, axis = 1)
    print(f'arr2: {arr2}')

    # 求均值
    # 先按照第0维度求和，也就是垂直相加再求平均值
    arr3 = np.mean(arr, axis = 0)
    print(f'arr3: {arr3}')
    # 按照列求平均值
    arr4 = np.mean(arr, axis = 1)
    print(f'arr4: {arr4}')

    # 求所有元素的平均值
    arr5 = np.mean(arr)
    print(f'arr5: {arr5}')

    print(f'np.std(arr):{np.std(arr)}')  # 标准差
    print(f'np.var(arr):{np.var(arr)}')
    print(f'np.max(arr)/np.min(arr):{np.max(arr)/np.min(arr)}')
    print(f'np.argmax(arr):{np.argmax(arr)}')
    print(f'np.argmin(arr):{np.argmin(arr)}')
    np.var(arr)  # 方差
    np.max(arr) / np.min(arr)
    np.argmax(arr)  # 最大值索引
    np.argmin(arr)

def save_load():
    arr = np.array([[1, 2], [3, 4]])
    # 保存读取二进制npy
    np.save("data.npy", arr)
    arr_load = np.load("data.npy")
    print(f'arr_load: {arr_load}')
    # 文本csv
    np.savetxt("arr.txt", arr, delimiter=",")
    arr_txt = np.loadtxt("arr.txt", delimiter=",")
    print(f'arr_txt: {arr_txt}')

if __name__ == '__main__':
    # create_array()
    # slice_array()
    # broad_cast()
    # reshape_array()
    # math_array()
    save_load()
