import numpy as np

# 1. 固定随机种子，生成100行3列的模拟特征数据（3个特征、100条样本）
np.random.seed(42)
feature_data = np.random.randn(100, 3) * 5 + 10  # 均值10，标准差5
print(f'feature_data:\n {feature_data}')
# 2. 数据标准化（Z-Score标准化，机器学习通用预处理）
mean = np.mean(feature_data, axis=0)  # 按列求均值（每个特征单独标准化）
std = np.std(feature_data, axis=0)    # 按列求标准差
norm_data = (feature_data - mean) / std
print(f'norm_data.shape: {norm_data.shape}')
print(f'norm_data: \n{norm_data}')

print("标准化后数据均值：", np.round(np.mean(norm_data, axis=0), 2))
print("标准化后数据标准差：", np.round(np.std(norm_data, axis=0), 2))

# 3. 3σ原则筛选异常值（绝对值大于3为异常）
outlier_mask = np.abs(norm_data) > 3
print(f'outlier_mask:\n {outlier_mask}')
outlier_count = np.sum(outlier_mask)
print(f"\n检测到异常值数量：{outlier_count}")

# 4. 剔除含异常值的样本
# any按照行或者列统计，只要有一个元素为True，结果就为True
row_outlier_mask = np.any(outlier_mask, axis=1)
'''
row_outlier_mask = 
     [False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False  True False False
 False False False False False False False False False False False False
 False False False  True False False False False False False False False
 False False False False]

统计outlier_mask每一行的每个特征，只要有一个特征为True，结果为True,否则为False
目的就是筛选出每个样本到底是异常样本还是正常样本
row_outlier_mask是一个100个元的一维列表，每个元素代表对应的样本是否异常。
比如row_outlier_mask[0]为True，那么第一个样本就是异常样本，将来要做清洗，将来要删掉样本
'''
print(f'row_outlier_mask.shape:\n {row_outlier_mask.shape}')
print(f'row_outlier_mask:\n {row_outlier_mask}')
# 对bool类型的数组取反，False变为True,True变为False
# 目的，将bool数组改为筛选数组(异常样本对应的bool值为False,正常的样本变为True)
# 将来这个筛选数组作为下标，去筛选样本，只保留正常样本，也就是为True的样本
row_outlier_mask = ~row_outlier_mask
'''
 [ True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True False  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True False  True  True  True  True  True  True  True  True
  True  True  True  True]
'''
print(f'row_outlier_mask:\n {row_outlier_mask}')
# 进行筛选，选出正常的样本，异常样本被过滤掉
clean_data = feature_data[row_outlier_mask]
print(f'clean_data.shape:\n {clean_data.shape}')
print(f"原始样本数：{feature_data.shape[0]}，清洗后样本数：{clean_data.shape[0]}")

# 5. 输出清洗后数据统计信息
print("\n清洗后数据统计：")
print(f"均值：{np.round(np.mean(clean_data, axis=0), 2)}")
print(f"最大值：{np.round(np.max(clean_data, axis=0), 2)}")
print(f"最小值：{np.round(np.min(clean_data, axis=0), 2)}")