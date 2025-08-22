# 基本操作

## 读取图像

```py
import cv2

img = cv2.imread(filename='/tmp/a.jpg', flags=cv2.IMREAD_UNCHANGED)
```

flags 取值

| 常量                           | 值  | 含义                                                                                              |
| ------------------------------ | --- | ------------------------------------------------------------------------------------------------- |
| cv2.IMREAD_UNCHANGED           | -1  | 保持原格式不变                                                                                    |
| cv2.IMREAD_GRAYSCALE           | 0   | 将图像转换为单通道的灰度图像                                                                      |
| cv2.IMREAD_COLOR               | 1   | 将图像转换为三通道的 BGR 彩色图像(flags 的默认值)                                                 |
| cv2.IMREAD_ANYDEPTH            | 2   | 如果载入的图像深度是 16 或 32 位，则返回对应深度图像；如果不是 16 或 32 位，则统一转换为 8 位图像 |
| cv2.IMREAD_ANYCOLOR            | 4   | 以任何可能的颜色格式读取图像                                                                      |
| cv2.IMREAD_LOAD_GDAL           | 8   | 以 gdal 驱动程序加载图像                                                                          |
| cv2.IMREAD_REDUCED_GRAYSCALE_2 | -   | 将图像转换为单通道的灰度图像, 并将图像尺寸减小一半                                                |
| cv2.IMREAD_REDUCED_COLOR_2     | -   | 将图像转换为三通道的 BGR 彩色图像, 并将图像尺寸减小一半                                           |
| cv2.IMREAD_REDUCED_GRAYSCALE_4 | -   | 将图像转换为单通道的灰度图像, 并将图像尺寸减小到原来的 1/4                                        |
| cv2.IMREAD_REDUCED_COLOR_4     | -   | 将图像转换为三通道的 BGR 彩色图像, 并将图像尺寸减小到原来的 1/4                                   |
| cv2.IMREAD_REDUCED_GRAYSCALE_8 | -   | 将图像转换为单通道的灰度图像, 并将图像尺寸减小到原来的 1/8                                        |
| cv2.IMREAD_REDUCED_COLOR_8     | -   | 将图像转换为三通道的 BGR 彩色图像, 并将图像尺寸减小到原来的 1/8                                   |
| cv2.IMREAD_IGNORE_ORIENTATION  | -   | 不以 EXIF 的方向为标记旋转图像                                                                    |

## 显示图像

```py
# 创建指定名称的窗口
cv2.namedWindow(winname='window1')
# 把img显示在名为window1的窗口上
cv2.imshow(winname='window1', mat=img)

# 等待用户按键, 避免窗口立即关闭
key = cv2.waitKey(delay=0)
# 销毁所有窗口
cv2.destroyAllWindows()
```

也可以不创建窗口, 直接使用 imshow 显示图片, 这样 imshow 会自动创建一个窗口。

## 保存图像

```py
# 保存图像
is_success = cv2.imwrite(filename='./a.jpg', img=img)
```
