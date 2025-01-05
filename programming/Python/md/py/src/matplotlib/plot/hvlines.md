# 数据点到坐标轴的注释线

hlines 函数用于绘制水平直线, vlines 函数用于绘制垂直直线。

```py
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 10, 10)
y = x * 2

fig = plt.figure()

ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8))
ax_main.set_xlim(left=0, right=10)
ax_main.set_ylim(bottom=0, top=20)

# 绘制点(3, 6)到x轴的注释线
ax_main.vlines(x=3, ymin=0, ymax=6, color='b', linestyles='dotted')
# 绘制点(3, 6)到y轴的注释线
ax_main.hlines(y=6, xmin=0, xmax=3, color='b', linestyles='dotted')

ax_main.plot(x, y, ms=5, ls='None', marker='o')
plt.show()
```
