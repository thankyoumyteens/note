# 彩色图片转为灰度图

```py
import cv2

img = cv2.imread('a.jpg')

# 彩色图片转为灰度图
# 参数1: 图片数组
# 参数2: 转换类型
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('gray', img)

# 等待键盘输入, 避免窗口一闪而过
cv2.waitKey()
```
