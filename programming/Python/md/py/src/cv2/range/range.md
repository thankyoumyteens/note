# 区域操作

可以通过 NumPy 数组的切片操作方便地编辑图像。

```py
import cv2
import numpy as np
from networkx.algorithms.isomorphism.matchhelpers import tmpdoc

# 生成一个600×600大小的图像
img = np.random.randint(0, 256, size=(600, 600, 3), dtype=np.uint8)

# 把第100行到第199行, 与第100列到第199列的交叉区域设置为白色(255, 255, 255)
img[100:200, 100:200, 0] = 255
img[100:200, 100:200, 1] = 255
img[100:200, 100:200, 2] = 255

# 把第300行到第399行, 与第300列到第399列的交叉区域设置为白色(255, 255, 255)
# 用一行代码实现
img[300:400, 300:400,] = 255

# 把第300行到第399行, 与第300列到第399列的交叉区域
# 复制到第500行到第599行, 与第500列到第599列的交叉区域
tmp = img[300:400, 300:400, :]
img[500:600, 500:600, :] = tmp

# 显示图像
cv2.imshow('window1', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
