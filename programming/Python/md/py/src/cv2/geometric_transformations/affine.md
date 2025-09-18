# 仿射

在 OpenCV 中，实现仿射变换（Affine Transformation）的核心是 cv2.warpAffine() 函数，其关键是先通过 3 对对应点计算出仿射变换矩阵（描述平移、旋转、缩放、剪切的组合关系），再用该矩阵对图像进行变换。

```py
import cv2
import numpy as np

# 读取原始图像
img = cv2.imread("a.png")

h, w = img.shape[:2]  # 获取图像高度、宽度（高×宽）

# 定义3对对应点（原始图像点 → 目标图像点）
# 原始点：选图像中易识别的3个不共线点（如左上角、右上角、左下角）
pts1 = np.float32([
    [50, 50],    # 原始点1（左上角附近）
    [w-50, 50],  # 原始点2（右上角附近）
    [50, h-50]   # 原始点3（左下角附近）
])
# 目标点：定义变换后这3个点的新位置（此处模拟“旋转+轻微平移”效果）
pts2 = np.float32([
    [100, 80],   # 目标点1（比原始点1右移50、下移30）
    [w-80, 60],  # 目标点2（比原始点2左移30、下移10）
    [70, h-60]   # 目标点3（比原始点3右移20、上移10）
])

# 计算仿射变换矩阵（2×3矩阵）
M = cv2.getAffineTransform(pts1, pts2)
print("仿射变换矩阵 M:\n", M)  # 矩阵包含线性变换（前2×2）和平移（最后1列）

# 应用仿射变换（核心函数 cv2.warpAffine）
# 参数说明：
# - img：原始图像
# - M：仿射变换矩阵
# - (w, h)：输出图像尺寸（与原始图像一致，可按需调整）
# - borderMode=cv2.BORDER_CONSTANT：边界填充方式（此处用黑色填充变换后超出原图的区域）
# - value=(0,0,0)：边界填充颜色（BGR格式，黑色）
affine_img = cv2.warpAffine(
    img,
    M,
    (w, h),
    borderMode=cv2.BORDER_CONSTANT,
    borderValue=(0, 0, 0)
)

cv2.imshow("Affine Transformed Image", affine_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## 平移、旋转、缩放、剪切

```py
import cv2
import numpy as np

def translate_image(image, dx, dy):
    """
    图像平移
    :param image: 输入图像
    :param dx: 水平方向平移像素数
    :param dy: 垂直方向平移像素数
    :return: 平移后的图像
    """
    h, w = image.shape[:2]
    # 定义平移矩阵 [1, 0, dx; 0, 1, dy]
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    # 应用平移变换
    translated = cv2.warpAffine(
        image,
        M,
        (w, h),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)  # 白色填充
    )
    return translated

def rotate_image(image, angle, center=None, scale=1.0):
    """
    图像旋转
    :param image: 输入图像
    :param angle: 旋转角度（度），正值为逆时针
    :param center: 旋转中心，默认为图像中心
    :param scale: 缩放比例
    :return: 旋转后的图像
    """
    h, w = image.shape[:2]

    # 如果未指定旋转中心，则使用图像中心
    if center is None:
        center = (w // 2, h // 2)

    # 获取旋转矩阵
    M = cv2.getRotationMatrix2D(center, angle, scale)
    # 应用旋转变换
    rotated = cv2.warpAffine(
        image,
        M,
        (w, h),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)  # 白色填充
    )
    return rotated

def scale_image(image, fx, fy):
    """
    图像缩放
    :param image: 输入图像
    :param fx: 水平方向缩放比例
    :param fy: 垂直方向缩放比例
    :return: 缩放后的图像
    """
    # 使用双线性插值进行缩放
    scaled = cv2.resize(
        image,
        (0, 0),
        fx=fx,
        fy=fy,
        interpolation=cv2.INTER_LINEAR
    )
    return scaled

def shear_image(image, shear_factor_x=0, shear_factor_y=0):
    """
    图像剪切
    :param image: 输入图像
    :param shear_factor_x: 水平剪切因子
    :param shear_factor_y: 垂直剪切因子
    :return: 剪切后的图像
    """
    h, w = image.shape[:2]

    # 定义剪切矩阵
    # [1, shear_factor_x, 0; shear_factor_y, 1, 0]
    M = np.float32([
        [1, shear_factor_x, 0],
        [shear_factor_y, 1, 0]
    ])

    # 应用剪切变换
    sheared = cv2.warpAffine(
        image,
        M,
        (w + int(h * abs(shear_factor_x)), h + int(w * abs(shear_factor_y))),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)  # 白色填充
    )
    return sheared
```
