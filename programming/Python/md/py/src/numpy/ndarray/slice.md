# 切片

```py
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

# 取第一行的所有元素
print(arr[:1, :])

# 取前两行的所有元素
print(arr[:2, :])

# 取第一列的所有元素
print(arr[:, :1])

# 取前两列的所有元素
print(arr[:, :2])

# 取第二列的所有元素
print(arr[:, 1:2])

# 取大于2的元素, 返回一个一维数组
print(arr[arr > 2])
```
