# 位运算

- 与: cv2.bitwise_and(img1, img2)
- 或: cv2.bitwise_or(img1, img2)
- 非: cv2.bitwise_not(img1, img2)
- 异或: cv2.bitwise_xor(img1, img2)

```py
import cv2
import numpy as np

img1 = cv2.imread('a.jpg')
h, w, c = img1.shape
img2 = np.zeros((h, w, c), dtype=np.uint8)
# 第330行到第470行，第110列到第225列的部分的值设为255(11111111)
img2[330:470, 110:225] = 255

# 保留img1中第330行到第470行，第110列到第225的部分
# 其它部分置为0(黑色)
img3 = cv2.bitwise_and(img1, img2)

cv2.imshow('1', img1)
cv2.imshow('2', img2)
cv2.imshow('r', img3)

cv2.waitKey()
```
