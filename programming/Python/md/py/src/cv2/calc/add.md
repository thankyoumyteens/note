# 加法

可以通过加号运算符 `+` 对图像进行加法运算，也可以通过 cv2.add() 函数对图像进行加法运算。

## 加号运算符

加号运算符求和时, 如果发生溢出, 则结果超出 8 位的部分会被舍掉, 相当于 a + b = (a + b) % 2<sup>8</sup>。

```py
import cv2
import numpy as np

img1 = np.full(shape=(600, 600, 3), fill_value=100, dtype=np.uint8)
img2 = np.full(shape=(600, 600, 3), fill_value=100, dtype=np.uint8)

# 把图像的每个像素值都加上50
img1 = img1 + 50
# 灰色图片
cv2.imshow('img1', img1)

# 相加后的值超过了255, 实际的结果是 256 % 256 = 0
img2 = img2 + 156
# 黑色图片
cv2.imshow('img2', img2)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

## add 函数

加号运算符求和时, 如果发生溢出, 则使用所能表示范围的最大值(255)作为计算结果。该最大值，一般被称为图像的像素饱和值，所以函数 cv2.add() 的求和一般被称为饱和值求和。

```py
import cv2
import numpy as np

img1 = np.full(shape=(600, 600, 3), fill_value=100, dtype=np.uint8)
img2 = np.full(shape=(600, 600, 3), fill_value=100, dtype=np.uint8)

# 把图像的每个像素值都加上50
img1 = img1 + 50
# 灰色图片
cv2.imshow('img1', img1)

# 相加后的值超过了255, 实际的结果是 255
img2 = cv2.add(img2, 156)
# 白色图片
cv2.imshow('img2', img2)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
