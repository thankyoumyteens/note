# 读取图片

```py
import cv2

# img是一个numpy数组
# 数组的shape是(height, width, channels)
# height是图片的高度
# width是图片的宽度
# channels是图片的通道数
# 通道数为3表示图片是彩色图片
# 通道数为1表示图片是灰度图片
img = cv2.imread('a.jpg')

# 打印图片的shape
print(img.shape)
# 输出 (250, 250, 3)
# 图片的高度是250
# 图片的宽度是250
# 图片的通道数是3

# 显示图片
# 参数1: 窗口名称
# 参数2: 图片数组
cv2.imshow('image1', img)

# 等待键盘输入, 避免窗口一闪而过
cv2.waitKey()
```
