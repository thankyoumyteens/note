# 透视

在 OpenCV 中，透视变换（Perspective Transformation）通过 `cv2.getPerspectiveTransform()` 计算透视矩阵，再用 `cv2.warpPerspective()` 应用变换，核心是通过**4 对不共线的对应点**（原始图像 4 点 + 目标图像 4 点），将图像从“透视视角”转为“正视视角”（如将倾斜的文档矫正为正视图）。以下是详细实现步骤、代码示例及场景应用：

透视变换适用于**图像矫正**（如倾斜文档、车牌矫正）或**视角转换**（如从侧面视角转为正面视角）。实现需两个关键步骤：

1. 选 4 对对应点：原始图像中选 4 个不共线的点（如倾斜文档的 4 个角），目标图像中对应 4 个点（如正矩形的 4 个角）；
2. 计算透视矩阵：通过 `cv2.getPerspectiveTransform(原始4点, 目标4点)` 生成 3×3 的透视矩阵（仿射变换是 2×3 矩阵，透视变换维度更高，支持更复杂的视角转换）；
3. 应用透视变换：用 `cv2.warpPerspective(图像, 透视矩阵, 目标尺寸)` 得到矫正后的图像。

```python
import cv2
import numpy as np

# 读取原始图像（倾斜的文档）
img = cv2.imread("tilted_document.jpg")

h, w = img.shape[:2]

# 原始图像4点：手动选取倾斜文档的4个角（
pts1 = np.float32([
    [50, 60],    # 原始点1：文档左上角
    [w-50, 50],  # 原始点2：文档右上角
    [w-30, h-40],# 原始点3：文档右下角
    [40, h-30]   # 原始点4：文档左下角
])

# 目标图像4点：定义矫正后的正矩形（如宽度400，高度500，根据需求调整）
target_w = 400  # 矫正后文档宽度
target_h = 500  # 矫正后文档高度
pts2 = np.float32([
    [0, 0],          # 目标点1：正矩形左上角
    [target_w, 0],   # 目标点2：正矩形右上角
    [target_w, target_h],  # 目标点3：正矩形右下角
    [0, target_h]    # 目标点4：正矩形左下角
])

# 3. 计算3×3的透视矩阵
M = cv2.getPerspectiveTransform(pts1, pts2)
print("透视变换矩阵 M:\n", M)

# 4. 应用透视变换（核心函数 cv2.warpPerspective）
# 参数说明：
# - img：原始图像
# - M：透视矩阵
# - (target_w, target_h)：目标图像尺寸（与pts2定义的正矩形一致）
# - borderMode=cv2.BORDER_CONSTANT：边界填充方式（黑色填充超出区域）
perspective_img = cv2.warpPerspective(
    img,
    M,
    (target_w, target_h),
    borderMode=cv2.BORDER_CONSTANT,
    borderValue=(0, 0, 0)  # 填充颜色：黑色（BGR格式）
)

cv2.imshow("Perspective Corrected Image", perspective_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
