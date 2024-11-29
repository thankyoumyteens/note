# 函数运算

- `np.sin(arr)` 对 numpy 数组 arr 中每个元素取正弦
- `np.cos(arr)` 对 numpy 数组 arr 中每个元素取余弦
- `np.tan(arr)` 对 numpy 数组 arr 中每个元素取正切
- `np.arcsin(arr)` 对 numpy 数组 arr 中每个元素取反正弦
- `np.arccos(arr)` 对 numpy 数组 arr 中每个元素取反余弦
- `np.arctan(arr)` 对 numpy 数组 arr 中每个元素取反正切
- `np.exp(arr)` 对 numpy 数组 arr 中每个元素取以 e 为底数的指数函数(即 e 的多少次方)
- `np.sqrt(arr)` 对 numpy 数组 arr 中每个元素取平方根

```py
import numpy as np

arr1 = np.array([[1, 2, 3], [4, 5, 6]])

arr = np.sin(arr1)

# [[ 0.84147098  0.90929743  0.14112001]
#  [-0.7568025  -0.95892427 -0.2794155 ]]
print(arr)

arr = np.exp(arr1)

# [[  2.71828183   7.3890561   20.08553692]
#  [ 54.59815003 148.4131591  403.42879349]]
print(arr)
```
