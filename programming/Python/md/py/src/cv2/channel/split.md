# 拆分通道

```py
import cv2
import numpy as np

img = np.random.randint(0, 256, size=(600, 600, 3), dtype=np.uint8)

# 取出B通道
b = img[:, :, 0]
# 取出G通道
g = img[:, :, 1]
# 取出R通道
r = img[:, :, 2]

# 把B通道上的所有像素值设置为0
img[:, :, 0] = 0
# 把G通道上的所有像素值设置为0
img[:, :, 1] = 0
# 把R通道上的所有像素值设置为0
img[:, :, 2] = 0

# 此时图像是黑色的
cv2.imshow('window1', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## 使用函数拆分通道

```py
b, g, r = cv2.split(img)
```
