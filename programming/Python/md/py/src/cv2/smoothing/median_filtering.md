# 中值滤波

中值滤波（Median Filtering）是一种非线性平滑滤波算法，核心通过取像素邻域内所有像素值的中值（排序后中间位置的值）来替换中心像素值。与均值滤波、高斯滤波的 “加权平均” 不同，它能有效去除椒盐噪声（图像中的孤立黑白点），同时最大程度保留图像边缘（这是其最显著的优势）。

中值替换

1. 定义一个奇数大小的滤波核（如 3×3、5×5）
2. 将核的中心对准图像中的每个像素，收集核内所有像素的灰度值
3. 对这些灰度值排序（从小到大或从大到小）
4. 取排序后的中间值（若核内有 9 个像素，取第 5 个值）替换中心像素的原始值

例如，3×3 核内像素值为 10, 200, 15, 5, 255, 20, 25, 30, 35，排序后为 5, 10, 15, 20, 25, 30, 35, 200, 255，中值为 25，用 25 替换中心像素值 —— 孤立的噪声点（200、255）被排除，边缘得以保留。

```py
import cv2
import numpy as np

img = cv2.imread("test.jpg")
# 添加椒盐噪声（5%的噪声比例）
h, w = img.shape[:2]
salt_pepper = np.random.rand(h, w)  # 0~1的随机数
salt = salt_pepper < 0.025  # 2.5%的白点
pepper = salt_pepper > 0.975  # 2.5%的黑点
noisy_img = img.copy()
noisy_img[salt] = 255  # 白点（BGR均为255）
noisy_img[pepper] = 0   # 黑点（BGR均为0）

# （1）3×3中值滤波（针对性去椒盐噪声）
median_3x3 = cv2.medianBlur(noisy_img, 3)
# （2）5×5中值滤波（更强去噪，可能轻微模糊）
median_5x5 = cv2.medianBlur(noisy_img, 5)

cv2.imshow("Noisy Image (Salt & Pepper)", noisy_img)
cv2.imshow("Median Blur (3x3)", median_3x3)  # 噪声基本去除，边缘清晰
cv2.imshow("Median Blur (5x5)", median_5x5)  # 噪声完全去除，轻微模糊

cv2.waitKey(0)
cv2.destroyAllWindows()
```
