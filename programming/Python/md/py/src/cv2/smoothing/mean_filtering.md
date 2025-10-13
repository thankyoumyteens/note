# 均值滤波

均值滤波（Mean Filtering）是 OpenCV 中最简单的图像平滑算法，核心通过计算像素邻域内所有像素的算术平均值来替换中心像素值，从而达到去除噪声、平滑图像的效果。它实现简单、计算快速，适合处理轻度随机噪声，但会模糊图像边缘（这是其主要缺点）。

均值滤波的本质是 “邻域平均”：

1. 定义一个固定大小的矩形滤波核（如 3×3、5×5，必须是奇数，确保有中心像素）
2. 将核的中心对准图像中的每个像素
3. 计算核覆盖区域内所有像素的算术平均值
4. 用该平均值替换中心像素的原始值，实现平滑

例如，3×3 核的计算方式：对于像素 (x,y)，其新值 = （周围 8 个像素 + 自身）的总和 ÷ 9。

```py
import cv2

img = cv2.imread("test.jpg")
# 手动添加轻度随机噪声
h, w = img.shape[:2]
noise = np.random.randint(-20, 20, (h, w, 3), dtype=np.int16)  # -20~20的随机噪声
noisy_img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# 不同核大小的均值滤波
# （1）3×3核（轻度平滑）
blur_3x3 = cv2.blur(noisy_img, (3, 3))
# （2）5×5核（中度平滑）
blur_5x5 = cv2.blur(noisy_img, (5, 5))
# （3）7×7核（重度平滑，图像明显模糊）
blur_7x7 = cv2.blur(noisy_img, (7, 7))

# 显示结果（对比原始图、噪声图和不同核的滤波结果）
cv2.imshow("Noisy Image", noisy_img)
cv2.imshow("Mean Blur (3x3)", blur_3x3)
cv2.imshow("Mean Blur (5x5)", blur_5x5)
cv2.imshow("Mean Blur (7x7)", blur_7x7)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
