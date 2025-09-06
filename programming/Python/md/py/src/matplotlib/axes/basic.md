# 绘制坐标轴

```py
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB']
plt.rcParams['axes.unicode_minus'] = False

# 创建画布
plt.figure()

# 设置坐标轴范围
x_min, x_max = 0, 10  # x轴刻度范围0到10
y_min, y_max = 0, 8  # y轴刻度范围0到8
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

# 绘制坐标轴
plt.axhline(y=0, color='k', linewidth=1.5)  # x轴（水平线，y=0）
plt.axvline(x=0, color='k', linewidth=1.5)  # y轴（垂直线，x=0）

# 隐藏顶部和右侧的边框（让坐标轴更整洁）
ax = plt.gca()
ax.spines['top'].set_visible(False)  # 隐藏顶部边框
ax.spines['right'].set_visible(False)  # 隐藏右侧边框

# 调整布局并显示
plt.tight_layout()
plt.show()
```

效果:

![](../../img/axes_basic.png)
