# 图像轮廓

图像轮廓通常指图像中前景目标与背景之间的边界线，是一个闭合曲线，可用像素点序列来表示。对于二值图像，轮廓是前景与背景的交界线；对于灰度图像，轮廓常通过边缘检测或阈值分割得到。

与边缘的区别：边缘是灰度强度发生显著变化的位置，可能是不连续的；而轮廓是物体的完整边界，更强调闭合性和结构性。

```py
# contours：轮廓列表，每个轮廓是一个 N×1×2 的 numpy 数组（存储轮廓点的坐标 (x,y)）
# hierarchy：轮廓层级数组（[Next, Previous, First_Child, Parent]），描述轮廓间的嵌套关系
contours, hierarchy = cv2.findContours(
    image,          # 输入图像（必须是二值图：黑白，0表示背景，255表示前景）
    mode,           # 轮廓检索模式（控制是否检测所有轮廓或仅外层轮廓）
    method          # 轮廓近似方法（控制轮廓点的存储方式：密集或精简）
)
```

- image 输入图像必须是二值图（通过阈值处理得到，cv2.threshold() 或 cv2.adaptiveThreshold()）
- mode 轮廓检索模式（决定提取哪些轮廓）：
  - cv2.RETR_EXTERNAL：只提取最外层轮廓（常用，过滤内部小轮廓）
  - cv2.RETR_LIST：提取所有轮廓，不建立层级关系
  - cv2.RETR_CCOMP：提取所有轮廓，建立两层层级（外层和内层）
  - cv2.RETR_TREE：提取所有轮廓，建立完整层级关系（如嵌套轮廓）
- method 轮廓近似方法（决定如何存储轮廓点）：
  - cv2.CHAIN_APPROX_NONE：存储所有轮廓点（精确但冗余）
  - cv2.CHAIN_APPROX_SIMPLE：只存储角点（如矩形只存 4 个顶点，精简高效，常用）

```py
import cv2
import numpy as np

# 读取图像并转为灰度图
img = cv2.imread("test.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 预处理：去噪 + 二值化（关键：确保前景为255，背景为0）
# （1）高斯滤波去噪（避免噪声导致虚假轮廓）
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
# （2）二值化（以固定阈值处理为例）
_, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)  # 超过127为白色（前景）

# 提取轮廓
# 模式：RETR_EXTERNAL（只取最外层），方法：CHAIN_APPROX_SIMPLE（精简存储）
contours, hierarchy = cv2.findContours(
    binary,
    cv2.RETR_EXTERNAL,  # 只检测外层轮廓
    cv2.CHAIN_APPROX_SIMPLE  # 精简轮廓点
)

# 绘制轮廓（在原图上绘制，方便可视化）
# 参数：图像、轮廓列表、轮廓索引（-1表示所有）、颜色（BGR）、线宽
img_with_contours = img.copy()  # 复制原图，避免修改原图
cv2.drawContours(
    img_with_contours,
    contours,
    -1,  # 绘制所有轮廓
    (0, 255, 0),  # 绿色（BGR格式）
    2  # 线宽2像素
)

# 计算并打印轮廓特征（可选，如面积、周长、质心）
for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)  # 面积（像素数）
    perimeter = cv2.arcLength(cnt, closed=True)  # 周长（closed=True表示闭合轮廓）
    # 质心（通过矩计算）
    M = cv2.moments(cnt)
    if M["m00"] != 0:  # 避免除零
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0
    print(f"轮廓 {i+1}：面积={area:.1f}, 周长={perimeter:.1f}, 质心=({cx},{cy})")

cv2.imshow("Original", img)
cv2.imshow("Binary Image", binary)
cv2.imshow("Contours", img_with_contours)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
