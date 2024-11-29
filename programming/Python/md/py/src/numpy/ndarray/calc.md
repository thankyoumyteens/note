# 基本运算

- `+` 两个 numpy 数组对应元素相加
- `-` 两个 numpy 数组对应元素相减
- `*` 两个 numpy 数组对应元素相乘
- `/` 两个 numpy 数组对应元素相除，如果都是整数则取商
- `%` 两个 numpy 数组对应元素相除后取余数
- `**n` 单个 numpy 数组每个元素都取 n 次方

```py
import numpy as np

arr1 = np.array([[1, 2, 3], [4, 5, 6]])
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

arr = arr1 + arr2

# [[ 2  4  6]
#  [ 8 10 12]]
print(arr)

arr = arr1**2

# [[ 1  4  9]
#  [16 25 36]]
print(arr)
```
