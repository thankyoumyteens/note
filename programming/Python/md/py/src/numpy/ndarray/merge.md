# 合并数组

## 按行拼接

```py
import numpy as np

arr1 = np.array([[1, 2, 3], [4, 5, 6]])
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

# 按行拼接
arr = np.concatenate((arr1, arr2), axis=0)

# [[1 2 3]
#  [4 5 6]
#  [1 2 3]
#  [4 5 6]]
print(arr)
```

## 按列拼接

```py
import numpy as np

arr1 = np.array([[1, 2, 3], [4, 5, 6]])
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

# 按列拼接
arr = np.concatenate((arr1, arr2), axis=1)

# [[1 2 3 1 2 3]
#  [4 5 6 4 5 6]]
print(arr)
```

## 垂直堆叠

```py
import numpy as np

arr1 = np.array([[1, 2, 3], [4, 5, 6]])
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

# 垂直堆叠
arr = np.vstack((arr1, arr2))

# [[1 2 3]
#  [4 5 6]
#  [1 2 3]
#  [4 5 6]]
print(arr)
```

## 水平堆叠

```py
import numpy as np

arr1 = np.array([[1, 2, 3], [4, 5, 6]])
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

# 水平堆叠
arr = np.hstack((arr1, arr2))

# [[1 2 3 1 2 3]
#  [4 5 6 4 5 6]]
print(arr)
```

## 堆叠列向量

将一维数组作为列向量堆叠在一起, 形成一个新的二维数组。

```py
import numpy as np

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# 堆叠列向量
arr = np.column_stack((arr1, arr2))

# [[1 4]
#  [2 5]
#  [3 6]]
print(arr)
```
