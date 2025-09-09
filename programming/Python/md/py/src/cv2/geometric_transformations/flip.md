# 翻转

```py
dst = cv2.flip(src, flipCode)
```

参数说明：

- src：输入的原始图像
- flipCode：翻转模式，决定翻转方向：
- flipCode = 1：水平翻转（左右翻转）
- flipCode = 0：垂直翻转（上下翻转）
- flipCode = -1：水平和垂直方向同时翻转（相当于旋转 180 度）

```py
import cv2

img = cv2.imread('a.png')

# 水平翻转
flip_horizontal = cv2.flip(img, 1)

# 垂直翻转
flip_vertical = cv2.flip(img, 0)

# 水平垂直同时翻转
flip_both = cv2.flip(img, -1)

cv2.imshow('Horizontal Flip', flip_horizontal)
cv2.imshow('Vertical Flip', flip_vertical)
cv2.imshow('Both Flips', flip_both)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
