# 形态学操作

形态学操作（Morphological Operations）是基于图像形状的处理技术，通过结构元素（Structuring Element） 与图像进行卷积，实现对目标形状的调整（如膨胀、腐蚀、开运算、闭运算等）。核心应用包括：去除噪声、分离独立元素、连接相邻物体、提取目标边界等，广泛用于图像预处理和分割。

1. 结构元素（Kernel）：一个小型矩阵（如 3×3、5×5 的矩形或圆形），作为 “模板” 决定形态学操作的范围和形状。OpenCV 中常用 cv2.getStructuringElement() 生成，支持矩形（MORPH_RECT）、十字形（MORPH_CROSS）、椭圆形（MORPH_ELLIPSE）
2. 基本操作：形态学操作的基础是膨胀（Dilation） 和腐蚀（Erosion），其他操作（开、闭、梯度等）均由这两种组合而成
