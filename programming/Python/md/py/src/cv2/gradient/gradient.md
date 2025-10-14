# 图像梯度

图像梯度（Image Gradient）是描述图像像素值变化率的核心概念，本质是通过计算相邻像素的灰度差异，定位图像中的 “边缘区域”（像素值突变处）。在 OpenCV 中，图像梯度是边缘检测、特征提取、图像分割的基础，常用算法包括 Sobel、Scharr、Laplacian 等。

OpenCV 提供三种核心梯度计算函数，适用于不同场景：

1. Sobel: 基于 3×3 卷积核，计算水平 / 垂直梯度，速度快
   - 适用场景: 常规边缘检测，对噪声有一定鲁棒性
2. Scharr: 优化的 Sobel 核（更陡峭），梯度精度更高
   - 适用场景: 需更高边缘精度，替代 Sobel
3. Laplacian: 基于二阶导数，检测所有方向边缘，无方向性
   - 适用场景: 快速边缘提取，对噪声敏感

关键参数:

1. Sobel/Scharr 核心参数
   - ddepth：输出图像深度，必须设为 cv2.CV_64F（64 位浮点型），原因是：像素从亮到暗的变化会产生负梯度值，uint8（0~255）会截断负值，导致边缘丢失；用 CV_64F 保存负值后，通过 convertScaleAbs 取绝对值，才能完整保留边缘
   - dx/dy：导数阶数，dx=1, dy=0 计算水平梯度，dx=0, dy=1 计算垂直梯度（不可同时为 0）
   - ksize：卷积核大小，Sobel 支持 1、3、5、7（1 表示用 1×3/3×1 核），Scharr 仅支持 3×3 核
2. Laplacian 核心参数
   - ksize：核大小（必须为奇数），默认 1（用 3×3 核），核越大，边缘越平滑，但细节越少

```py
import cv2
import numpy as np

# 读取图像并转为灰度图（梯度计算对灰度图效果最佳）
img = cv2.imread("test.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Sobel梯度（水平+垂直）
# Sobel函数参数：src, ddepth（输出深度）, dx（x方向导数阶数）, dy（y方向导数阶数）, ksize（核大小）
# dx=1, dy=0 → 水平梯度（Gx，检测垂直边缘）
sobel_x = cv2.Sobel(gray, cv2.CV_64F, dx=1, dy=0, ksize=3)
# dx=0, dy=1 → 垂直梯度（Gy，检测水平边缘）
sobel_y = cv2.Sobel(gray, cv2.CV_64F, dx=0, dy=1, ksize=3)
# 注意：Sobel计算会产生负数值（表示像素值从亮到暗的变化），需取绝对值并转为uint8
sobel_x_abs = cv2.convertScaleAbs(sobel_x)
sobel_y_abs = cv2.convertScaleAbs(sobel_y)
# 合并水平和垂直梯度（加权求和，增强边缘效果）
sobel_combined = cv2.addWeighted(sobel_x_abs, 0.5, sobel_y_abs, 0.5, 0)

# Scharr梯度（优化的Sobel，仅支持3×3核）
# 用法与Sobel一致，ksize可省略（默认3）
scharr_x = cv2.Scharr(gray, cv2.CV_64F, dx=1, dy=0)
scharr_y = cv2.Scharr(gray, cv2.CV_64F, dx=0, dy=1)
scharr_x_abs = cv2.convertScaleAbs(scharr_x)
scharr_y_abs = cv2.convertScaleAbs(scharr_y)
scharr_combined = cv2.addWeighted(scharr_x_abs, 0.5, scharr_y_abs, 0.5, 0)

# Laplacian梯度（无方向，检测所有边缘）
# 参数：src, ddepth, ksize（核大小，默认1，推荐3/5）
laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
laplacian_abs = cv2.convertScaleAbs(laplacian)

cv2.imshow("Original Gray", gray)
cv2.imshow("Sobel Combined (3x3)", sobel_combined)
cv2.imshow("Scharr Combined (3x3)", scharr_combined)  # 边缘更锐利
cv2.imshow("Laplacian (3x3)", laplacian_abs)  # 边缘更密集

cv2.waitKey(0)
cv2.destroyAllWindows()
```

![](../../img/gradient.jpg)
