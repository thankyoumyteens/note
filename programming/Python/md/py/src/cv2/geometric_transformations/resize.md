# 缩放

在 OpenCV 中，实现图像缩放主要使用 cv2.resize() 函数，该函数支持自定义缩放尺寸、缩放比例，以及多种插值算法（用于处理缩放后像素的取值，影响图像质量）。

```py
dst = cv2.resize(src, dsize, fx=0, fy=0, interpolation=cv2.INTER_LINEAR)
```

- src: 待缩放的原始图像
- dsize: 输出图像的尺寸，格式为 (宽度, 高度)。注意：与图像的 shape(高, 宽)相反。若设为 `(0,0)`，则通过 fx 和 fy 计算尺寸
- fx: 水平方向（宽度）的缩放比例（`fx>1` 放大，`0<fx<1` 缩小），若 dsize 非零，此参数可省略
- fy: 垂直方向（高度）的缩放比例，与 `fx` 对应
- interpolation: 插值算法。核心参数，决定缩放后图像的清晰度，尤其放大时影响明显

缩放的本质是通过算法计算新尺寸下的像素值，不同插值算法适用于不同场景：

| 插值算法            | 适用场景                 | 特点                                                                           |
| ------------------- | ------------------------ | ------------------------------------------------------------------------------ |
| `cv2.INTER_NEAREST` | 快速缩放（如实时处理）   | nearest-neighbor 插值，取最近像素值，速度最快，但放大后易出现锯齿边缘          |
| `cv2.INTER_LINEAR`  | 常规缩放（默认值）       | 双线性插值，基于周围 4 个像素加权计算，平衡速度和质量，适合大多数场景          |
| `cv2.INTER_CUBIC`   | 高质量放大（如细节保留） | 双三次插值，基于周围 16 个像素计算，放大后图像更平滑，细节保留更好，但速度较慢 |
| `cv2.INTER_AREA`    | 缩小图像（避免失真）     | 基于像素区域融合，缩小后图像更清晰，避免出现杂色（不适合放大）                 |

## 按指定尺寸缩放

```py
import cv2

# 读取原始图像
img = cv2.imread('a.png')

h, w = img.shape[:2]

# 设定目标尺寸（宽×高），例如缩放到 300×200
target_size = (300, 200)
# 缩放（使用默认双线性插值）
resized_img = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)

# 显示结果
cv2.imshow("Resized (300x200)", resized_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

## 按比例缩放

```py
import cv2

# 读取原始图像
img = cv2.imread('a.png')

h, w = img.shape[:2]

# 缩放比例：水平和垂直方向均缩小为 0.5 倍
fx = 0.5
fy = 0.5
# dsize设为(0,0)，表示通过fx/fy计算尺寸
# 缩小用INTER_AREA更清晰
resized_small = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_AREA)

# 放大为原图的 2 倍
fx = 20.0
fy = 2.0
# 放大用INTER_CUBIC更平滑
resized_large = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)

# 显示
cv2.imshow("Resized (0.5x)", resized_small)
cv2.imshow("Resized (2.0x)", resized_large)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
