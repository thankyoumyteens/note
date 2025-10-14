# 方框滤波

方框滤波（Box Filtering）是均值滤波的扩展形式，核心通过计算像素邻域内的像素值总和（可选择是否归一化）来平滑图像。与均值滤波相比，它提供了 “是否归一化” 的选项，灵活性更高，归一化 = 均值滤波，不归一化 = 高亮增强。

方框滤波的逻辑与均值滤波类似，但增加了 “归一化开关”：

1. 定义一个矩形滤波核（如 3×3、5×5，奇数大小）
2. 计算核覆盖区域内所有像素的总和
3. 若选择归一化（默认）：替换值 = 总和 ÷ 核内像素数量（即均值滤波，平滑图像）
4. 若选择不归一化：直接使用总和替换（可能超过 255，导致像素值截断，形成高亮效果）

```py
import cv2
import numpy as np

img = cv2.imread("test.jpg")
# 手动添加轻度随机噪声
h, w = img.shape[:2]
noise = np.random.randint(-20, 20, (h, w, 3), dtype=np.int16)  # -20~20的随机噪声
noisy_img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# （1）归一化方框滤波（等价于均值滤波）
box_norm = cv2.boxFilter(
    noisy_img,
    ddepth=-1,  # 与输入图像深度一致
    ksize=(5, 5),  # 5×5核
    normalize=True  # 归一化（总和÷25）
)

# （2）不归一化方框滤波（总和直接作为像素值，可能超过255）
box_no_norm = cv2.boxFilter(
    noisy_img,
    ddepth=-1,
    ksize=(5, 5),
    normalize=False  # 不归一化（直接用总和）
)
# 注意：不归一化可能导致像素值超过255，OpenCV会自动截断为255（白色）

cv2.imshow("Noisy Image", noisy_img)
cv2.imshow("Box Filter (Normalized, 5x5)", box_norm)
cv2.imshow("Box Filter (No Normalization, 5x5)", box_no_norm)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
