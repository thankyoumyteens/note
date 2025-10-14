# 基本形态学操作

1. 腐蚀（Erosion）
   - 原理：结构元素在图像上滑动，若结构元素完全被目标（白色区域）覆盖，则中心像素保留为白色，否则变为黑色（“侵蚀” 目标边界，使目标缩小）
   - 效果：去除小噪声、断开目标连接、缩小目标尺寸
2. 膨胀（Dilation）
   - 原理：结构元素在图像上滑动，若结构元素与目标（白色区域）有重叠，则中心像素变为白色（“扩张” 目标边界，使目标增大）
   - 效果：填补目标孔洞、连接邻近目标、增大目标尺寸

```py
import cv2
import numpy as np

img = cv2.imread("binary_image.jpg", 0)

# 生成结构元素（3×3矩形核）
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# 腐蚀操作（ iterations=1 表示腐蚀1次，次数越多腐蚀越强）
eroded = cv2.erode(img, kernel, iterations=1)

# 膨胀操作（ iterations=1 表示膨胀1次）
dilated = cv2.dilate(img, kernel, iterations=1)

cv2.imshow("Original", img)
cv2.imshow("Eroded (3x3)", eroded)
cv2.imshow("Dilated (3x3)", dilated)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
