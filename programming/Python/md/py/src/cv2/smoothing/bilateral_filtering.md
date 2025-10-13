# 双边滤波

双边滤波（Bilateral Filtering）是一种非线性平滑滤波算法，核心通过空间距离权重和像素值相似度权重的乘积计算加权平均，在平滑噪声的同时能有效保留图像边缘（这是其与高斯滤波的最大区别）。它解决了传统滤波（如高斯滤波）过度模糊边缘的问题，适合需要保留边缘的图像美化、降噪场景。

双边滤波的加权核由两部分组成，共同决定邻域像素的权重：

1. 空间距离权重（高斯核）：与高斯滤波相同，距离中心像素越近，权重越高（控制空间平滑范围）
2. 像素值相似度权重（范围核）：中心像素与邻域像素的灰度值差异越小，权重越高（控制边缘保留 —— 边缘处像素值差异大，权重低，避免被平滑）

最终权重 = 空间距离权重 × 像素值相似度权重，确保：

- 平坦区域（像素值差异小）：权重高，平滑效果强（去噪彻底）
- 边缘区域（像素值差异大）：权重低，平滑效果弱（边缘保留）

```py
import cv2

img = cv2.imread("portrait.jpg")
# 添加高斯噪声（模拟轻微拍摄噪声）
h, w = img.shape[:2]
gauss_noise = cv2.randn(np.zeros_like(img, dtype=np.int16), 0, 15)  # 均值0，标准差15的噪声
noisy_img = cv2.addWeighted(img, 1.0, gauss_noise.astype(np.uint8), 1.0, 0)

# 双边滤波（d=5，sigmaColor=50，sigmaSpace=50）
bilateral = cv2.bilateralFilter(noisy_img, d=5, sigmaColor=50, sigmaSpace=50)

cv2.imshow("Noisy Image", noisy_img)
cv2.imshow("Bilateral Filter (d=5, sigmaC=50, sigmaS=50)", bilateral)  # 边缘清晰，噪声去除

cv2.waitKey(0)
cv2.destroyAllWindows()
```
