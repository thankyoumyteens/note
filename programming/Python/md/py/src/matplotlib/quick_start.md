# 基本使用

```py
import math

import matplotlib.pyplot as plt
import numpy as np

# 创建0到2π之间的数据，间隔为0.05
x = np.arange(0, math.pi * 2, 0.05)
# 计算数组每个元素的sin值, 作为y轴的数据
y = np.sin(x)
# 绘制图形
plt.plot(x, y)
# 展示图像
plt.show()
```
