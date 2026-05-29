from setuptools import setup, find_packages
import os
setup(
    name='datatools',
    version='1.0.0',
    description='数据处理工具包',
    author='zack',
    author_email='secondtonone1@163.com',
    url='https://github.com/secondtonone1/python_ai/tree/master/base/08_%E5%8C%85%E5%92%8C%E6%A8%A1%E5%9D%97/%E5%8C%85%E7%9A%84%E7%94%A8%E6%B3%95/datatools',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.19.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)