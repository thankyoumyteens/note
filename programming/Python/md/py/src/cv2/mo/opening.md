# 组合形态学操作

基于腐蚀和膨胀的组合，可实现更复杂的形态学操作：

1. 开运算（Opening）
   - 定义：先腐蚀，后膨胀（opening = dilate(erode(img))）
   - 效果：去除图像中小于结构元素的噪声，同时基本保持目标形状和大小不变（适合预处理去噪）
2. 闭运算（Closing）
   - 定义：先膨胀，后腐蚀（closing = erode(dilate(img))）
   - 效果：填补目标中小于结构元素的孔洞，连接邻近的小目标（适合修复目标内部缺陷）
3. 形态学梯度（Morphological Gradient）
   - 定义：膨胀 - 腐蚀（gradient = dilate(img) - erode(img)）
   - 效果：提取目标的边缘轮廓（边缘处膨胀和腐蚀的差异最大）
4. 顶帽（Top Hat）
   - 定义：原始图像 - 开运算结果（tophat = img - opening）
   - 效果：突出图像中比周围亮且小于结构元素的区域（如小亮点）
5. 黑帽（Black Hat）
   - 定义：闭运算结果 - 原始图像（blackhat = closing - img）
   - 效果：突出图像中比周围暗且小于结构元素的区域（如小黑点）

```py
# 生成结构元素（3×3矩形核）
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# 1. 开运算（去噪）
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# 2. 闭运算（填洞）
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# 3. 形态学梯度（边缘提取）
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

# 4. 顶帽（突出亮斑）
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

# 5. 黑帽（突出暗斑）
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
```
