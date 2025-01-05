# 画圆

```py
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D

# 创建圆形对象: 圆心在(1, 1), 半径为 1
# fill=True 使用颜色填充
# facecolor 指定填充颜色
# edgecolor 边框颜色
circle = plt.Circle((1, 1), 1, fill=False, fill=True, facecolor='blue', edgecolor='red', linewidth=2)

fig = plt.figure()

ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8))
ax_main.set_xlim(left=0, right=5)
ax_main.set_ylim(bottom=0, top=5)

transform = Affine2D().scale(1, 1)
# 将圆形添加到坐标轴中
ax_main.add_artist(circle)
# 令x轴和y轴长度相同, 保证圆形的形状正确
ax_main.set_aspect('equal')

plt.show()
```
