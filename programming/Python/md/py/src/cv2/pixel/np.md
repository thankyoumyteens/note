# 使用 numpy 处理像素

numpy.array 提供了 item() 和 itemset() 函数来访问和修改像素值。这两个函数都是经过优化的，能够更大幅度地提高处理效率。在访问及修改像素点的值时，利用 numpy.array 提供的函数比直接使用索引要快得多。

```py
import cv2
import numpy as np

# 生成一个600×600×3大小的数组，数组的元素类型为无符号8位整数
# 每个元素的值是随机的, 随机数范围是[0, 256)
img = np.random.randint(0, 256, size=(600, 600, 3), dtype=np.uint8)

# 获取数组的第1行第2列的第0个通道的像素值
pixel = img.item(1, 2, 0)
print(pixel)

# 把数组的第1行第2列的第0个通道的像素值设置为255
img.itemset((1, 2, 0), 255)

# 显示图像
cv2.imshow('window1', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
