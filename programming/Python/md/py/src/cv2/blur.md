# 处理图片的噪点

```py
import cv2

img = cv2.imread('a.jpg')

# 高斯滤波器
# 参数: 图像, 核大小, 标准差
gauss = cv2.GaussianBlur(img, (5, 5), 0)
# 均值滤波器
# 参数: 图像, 核大小
median = cv2.medianBlur(img, 5)

cv2.imshow("original", img)
cv2.imshow("gauss", gauss)
cv2.imshow("median", median)

cv2.waitKey(0)  # 等待按键（0 表示无限等待）
cv2.destroyAllWindows()
```
