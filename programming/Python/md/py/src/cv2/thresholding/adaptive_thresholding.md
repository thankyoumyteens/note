# 自适应阈值处理

自适应阈值处理（Adaptive Thresholding）是解决图像亮度不均匀（如存在阴影、反光）时固定阈值失效的关键技术。它通过计算每个像素局部邻域的亮度动态生成阈值，而非使用全局固定值，能在复杂光照下更准确地分割前景与背景。

1. 以当前像素为中心，取一个小的局部邻域（如 11×11 的方块）
2. 计算该邻域的亮度统计值（平均值或高斯加权平均值）
3. 用统计值减去一个常数 C，得到当前像素的阈值
4. 根据像素值与局部阈值的比较，将像素分为黑 / 白（二值化）

```py
dst = cv2.adaptiveThreshold(src, maxval, adaptiveMethod, thresholdType, blockSize, C)
```

- `src` 输入图像（必须是单通道灰度图，不能直接用彩色图）
- `maxval` 阈值处理后的最大值（通常设为 255，即白色）
- `adaptiveMethod` 局部阈值计算方法（二选一）：
  - cv2.ADAPTIVE_THRESH_MEAN_C：邻域内所有像素的平均值 - C
  - cv2.ADAPTIVE_THRESH_GAUSSIAN_C：邻域内像素的高斯加权平均值 - C（中心像素权重更高，边缘像素权重低，效果更优）
- `thresholdType` 二值化类型（仅支持两种）：
  - cv2.THRESH_BINARY：像素 > 局部阈值 → 255（白），否则 → 0（黑）
  - cv2.THRESH_BINARY_INV：像素 > 局部阈值 → 0（黑），否则 → 255（白）
- `blockSize` 局部邻域的大小（必须是奇数，如 3、5、7、11...）：
  - 数值越大：邻域范围越广，阈值越平滑（适合模糊图像）
  - 数值越小：对局部细节越敏感（适合清晰图像，但易受噪声影响）
- `C` 从局部平均值中减去的常数（整数，通常取 2~10）：
  - C 越大：阈值越低（更多像素被判定为白色）
  - C 越小：阈值越高（更多像素被判定为黑色），可抑制噪声

```py
import cv2

gray = cv2.imread("shadow_document.jpg", 0)  # 0表示直接读取为灰度图

# 自适应阈值处理（两种方法）
# （1）均值法自适应阈值（blockSize=11，C=2）
mean_thresh = cv2.adaptiveThreshold(
    gray,
    255,  # 最大值255
    cv2.ADAPTIVE_THRESH_MEAN_C,  # 局部均值法
    cv2.THRESH_BINARY,  # 二值化类型
    blockSize=11,  # 邻域大小11（奇数）
    C=2  # 减去常数2
)

# （2）高斯法自适应阈值（效果更优，推荐）
gaussian_thresh = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # 高斯加权均值法
    cv2.THRESH_BINARY,
    blockSize=11,
    C=2
)

cv2.imshow("Adaptive Mean (block=11)", mean_thresh)
cv2.imshow("Adaptive Gaussian (block=11)", gaussian_thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
