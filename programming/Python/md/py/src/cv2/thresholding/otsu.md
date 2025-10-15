# Otsu 阈值处理

Otsu 阈值处理（大津法）是 OpenCV 中自动计算最优阈值的经典算法，无需手动设定阈值，核心是通过最大化 “前景与背景像素的类间方差” 找到最佳分割阈值，尤其适合前景与背景灰度差异明显的图像。

Otsu 处理无需额外函数，只需在 cv2.threshold() 中添加 cv2.THRESH_OTSU 标志位，算法会自动计算最优阈值并返回。

```py
import cv2

# 读取灰度图像（Otsu仅支持单通道灰度图）
# 选择前景背景差异明显的图像（如文档、车牌）
gray = cv2.imread("test_gray.jpg", 0)  # 0表示直接读取为灰度图

# Otsu自动阈值（thresh设为0，添加THRESH_OTSU标志位）
ret_otsu, otsu_thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# 输出算法找到的最优阈值
print(f"Otsu自动计算的最优阈值：{ret_otsu}")

cv2.imshow('Original', img)
cv2.imshow(f"Otsu Threshold ({ret_otsu})", otsu_thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
