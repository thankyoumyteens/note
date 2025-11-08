# 多目标匹配

当源图像中存在多个与模板相似的目标时，可通过设置阈值筛选出所有匹配度高于阈值的区域。

```py
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread('a.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread('b.jpg', 0)
h, w = template.shape[:2]
method = cv2.TM_CCOEFF_NORMED
result = cv2.matchTemplate(img_gray, template, method)

# 设定阈值（根据实际情况调整，如0.8表示匹配度≥80%）
threshold = 0.8

# 找到所有匹配度高于阈值的位置
locations = np.where(result >= threshold)

# 遍历所有匹配位置并绘制矩形
for pt in zip(*locations[::-1]):  # 转换坐标顺序为(x, y)
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)  # 红色边框

# 显示多目标匹配结果
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('result')
plt.show()
```
