# 数组元素替换

```py
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

# 把第一行的所有元素改为0
arr[:1, :] = 0
print(arr)

# 把前两行的所有元素改为1
arr[:2, :] = 1
print(arr)

# 把第一列的所有元素改为2
arr[:, :1] = 2
print(arr)

# 把前两列的所有元素改为3
arr[:, :2] = 3
print(arr)

# 把第二列的所有元素改为4
arr[:, 1:2] = 4
print(arr)

# 把大于2的元素改为5
arr[arr > 2] = 5
print(arr)
```
