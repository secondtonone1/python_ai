import numpy
import pandas as pd
import numpy as np

def create_series():
    s = pd.Series([10,20,30],index=['a','b','c'],name='value')
    print(f's is \n{s}')
    print(f's["a"] is \n{s["a"]}')

def create_dataframe():
    df = pd.DataFrame(
        data = {
            'name':['Alice','Bob'],
            'age':[10,20],
            'score':[88,92]
        },
        index = ['line1','line2']
    )
    print(f'df is \n{df}')
    print(f'df.index is \n{df.index}')
    print(f'df.columns is \n{df.columns}')
    print(f'df.values is \n{df.values}')
    print(f'df.shape is \n{df.shape}')
    print(f'df.dtypes is \n{df.dtypes}')
    print(f'df.info is \n{df.info()}')
    print(f'df.describe() is \n{df.describe()}')


def create_data_frame():
    df1 = pd.DataFrame({
        'id':[1,2,3],
        'product': ['A','B','C'],
    })
    print(f'df1 is \n{df1}')

    arr = np.random.rand(2,3)
    df2 = pd.DataFrame(arr, index=['line1','line2'],columns=['col1','col2','col3'])
    print(f'df2 is \n{df2}')

    df3 = pd.DataFrame([[1,2],[3,4]],columns=['x','y'])
    print(f'df3 is \n{df3}')

def df_load_save():
    df1 = pd.DataFrame({
        'id': [1, 2, 3],
        'product': ['A', 'B', 'C'],
    })
    df1.to_csv('out.csv',index=False,encoding='utf-8')
    df2 = pd.read_csv('out.csv',encoding='utf-8',sep=',',header=0)
    print(f'df2 is \n{df2}')


def df_loc():
    df = pd.DataFrame(
        data={
            'name': ['Alice', 'Bob','Zack','Ray'],
            'age': [10, 20,38,35],
            'score': [88, 92,99,100]
        },
    )

    print(f'df is \n{df}')

    print(f'df.loc[0,"name"] is \n{df.loc[0,"name"]}')
    print(f'df.loc[df["age"]>23,["name","age"] is \n{df.loc[df["age"]>23,["name","age"]]}')

    print(f'df["age"] is \n{df["age"]}')
    print(f'df[["name","age"]] is \n{df[["name","age"]]}')

    df2 = df[(df["age"] > 20) & (df["score"] > 80)]
    print(f'df2 is \n{df2}')

def df_clean():
    df = pd.DataFrame(
        data={
            'name': ['Alice', 'Bob', 'Zack', 'Ray'],
            'age': [10, 20, 38, numpy.NaN],
            'score': [88, 92, 99, 100]
        },
    )

    print(f'df is \n{df}')
    # all 表示axis=0，也就是按照行删除，只有所有行都为NaN才删除
    df.dropna(how='all',axis=0,inplace=True)
    print(f'df is \n{df}')
    # any 表示任意值为空值则删除
    # df.dropna(how='any',axis=0,inplace=True)
    # print(f'df is \n{df}')

    df2 = df.dropna(how='any',axis=0,inplace=False)
    print(f'df is \n{df}')
    print(f'df2 is \n{df2}')

def df_group_by():
    df = pd.DataFrame(
        data={
            'product': ['Apple', 'Pear', 'Peach', 'Grape','Apple'],
            'age': [10, 20, 38, 38,25],
            'score': [88, 92, 99, 100,25]
        },
    )

    g = df.groupby('product')
    res = g['score'].agg(['mean','max','count'])
    print(f'res is \n{res}')

    res2 = g.agg(avg_score=('score','mean'))
    print(f'res2 is \n{res2}')

def df_merge_concat():
    df1 = pd.DataFrame({
        'id': [1, 2, 3],
        'product': ['A', 'B', 'C'],
    })

    df2 = pd.DataFrame({
        'id': [2, 5, 6],
        'product': ['A2', 'B2', 'C2'],
    })

    res = pd.merge(df1,df2,on='id',how='left')
    print(f'res is \n{res}')

    res2 = pd.concat([df1,df2],axis=0)
    print(f'res2 is \n{res2}')

    res3 = pd.concat([df1,df2],axis=1)
    print(f'res3 is \n{res3}')

def df_date():
    # 生成时间索引
    indexes = pd.date_range(start="2026-01-01", periods=10, freq="D")
    print(f'df is \n{indexes}')

    df = pd.DataFrame({
        'id': [1, 2, 3],
        'time': ['2026-01-01', '2026-01-02', '2026-01-03'],
    })

    # 转为datetime类型
    df["time"] = pd.to_datetime(df["time"])
    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month

    print(f'df is \n{df}')

def pandas_demo():
    data = {
        "name": ["张三", "李四", "王五", "赵六"],
        "department": ["技术", "产品", "技术", "运营"],
        "salary": [12000, 15000, 13000, 11000],
        "age": [28, 32, 26, 30]
    }

    df = pd.DataFrame(data)
    print(f'df is \n{df}')
    print(f'df.info()is {df.info()}')

    print(f'df.describe() is :\n', df.describe())

    print(f"df['department'] is:\n{df['department']}" )

    res = df['department'] == '技术'
    print(f'res is \n{res}')

    tech_df = df[res]
    print(f'tech_df is \n{tech_df}')

    res2 = df.groupby('department')['salary'].agg(['mean','max','count'])
    print(f'res2 is \n{res2}')

if __name__ == '__main__':
    # create_series()
    # create_dataframe()
    # create_data_frame()
    # df_load_save()
    # df_loc()
    # df_clean()
    # df_group_by()
    # df_merge_concat()
    # df_date()
    pandas_demo()