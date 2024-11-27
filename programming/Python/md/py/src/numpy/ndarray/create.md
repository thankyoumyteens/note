# 创建 numpy 数组

1. **从列表或元组创建**：
   ```python
   import numpy as np
   a = np.array([1, 2, 3])
   b = np.array([[1, 2], [3, 4]])
   ```
2. **使用特定值填充数组**：
   ```python
   # 创建一个3x4的二维数组, 所有元素都是0
   zeros_array = np.zeros((3, 4))
   # 创建一个3x4的二维数组, 所有元素都是1
   ones_array = np.ones((2, 3))
   # 创建一个3x4的二维数组, 所有元素都是9
   full_array = np.full((2, 2), 9)
   ```
3. **创建范围数组**：
   ```python
   # 创建范围[0,10), 且步长为2的数组
   # [0 2 4 6 8]
   range_array = np.arange(0, 10, 2)
   # 创建范围[0,1], 且元素个数为5的均匀分布的数组
   # [0.   0.25 0.5  0.75 1.  ]
   linspace_array = np.linspace(0, 1, 5)
   ```
4. **随机数生成**：
   ```python
   # 创建一个2x3的二维数组, 元素均匀分布且随机
   random_uniform = np.random.rand(2, 3)
   # 创建一个2x3的二维数组, 元素服从标准正态分布
   random_normal = np.random.randn(2, 3)
   # 创建一个2x3的二维数组, 元素为0到10之间的随机整数
   random_integers = np.random.randint(0, 10, (2, 3))
   ```
5. **从文件加载数据**：
   ```python
   # 从文本文件加载数据
   data_from_file = np.loadtxt('data.txt')
   ```
6. **根据给定的函数和形状创建数组**：
   ```python
   # 接受与 shape 参数相同长度的参数列表
   # 每个参数对应一个轴上的索引
   def func(x, y):
       return x + y
   # 创建一个2x3的二维数组
   # 返回的数组:
   # [
   #   [0 1 2]
   #   [1 2 3]
   # ]
   # 元素的值是通过调用 func 函数计算得到的
   # 比如，元素 array_from_function[0][0] 的值是 func(0, 0) = 0
   array_from_function = np.fromfunction(function=func, shape=(2, 3), dtype=int)
   ```
7. **空数组**：
   ```python
   # 创建一个2x3的未初始化的二维数组
   empty_array = np.empty((2, 2))  # 创建一个2x2的未初始化数组
   ```
