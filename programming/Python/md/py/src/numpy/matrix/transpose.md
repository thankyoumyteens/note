# 矩阵转置

数组的转置。对于二维数组, 这相当于行列互换:

```py
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

# 1 2 3
# 4 5 6
print(arr)

transpose = arr.T

# 1 4
# 2 5
# 3 6
print(transpose)
```
