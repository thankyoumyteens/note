# 图例

```py
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# 创建数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# 创建图形和坐标轴
fig = plt.figure()
ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))

# 绘制曲线
line1, = ax.plot(x, y1, color='blue')
line2, = ax.plot(x, y2, color='red')

# 创建自定义图例项
custom_lines = [
    Line2D([0], [0], color='blue', lw=2),
    Line2D([0], [0], color='red', lw=2)
]

# 添加图例
# handles: 图例项, 它包含了所有线型的实例
# labels：图例的标签
# loc：图例的位置
ax.legend(handles=custom_lines, labels=['sin(x)', 'cos(x)'], loc='upper left')

# 显示图形
plt.show()
```
