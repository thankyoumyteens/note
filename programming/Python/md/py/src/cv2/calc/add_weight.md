# 加权和

OpenCV中提供了函数cv2.addWeighted()，用来实现图像的加权和（混合、融合）。


```py
dst = addWeighted(src1, alpha, src2, beta, gamma)
```

参数gamma用来调节亮度，它的值可以是正数、负数或0。函数的效果是：结果图像=图像1×权重1+图像2×权重2+亮度调节量。


```py
import cv2
import numpy as np

img1 = cv2.imread('a.jpg')
h, w, c = img1.shape
img2 = np.random.randint(0, 255, (h, w, c), dtype=np.uint8)

# 加权和
img1 = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)

cv2.imshow('1', img1)

cv2.waitKey()
```
