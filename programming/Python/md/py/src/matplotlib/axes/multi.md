# 创建多个坐标轴

```py
import matplotlib.pyplot as plt

fig = plt.figure()

# 添加一个主坐标轴, 占据图形的大部分区域
ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8))
ax_main.plot([1, 2, 3, 4], [1, 4, 9, 16])
ax_main.set_title('Main Axes')

# 添加一个小的子坐标轴, 位于主坐标轴的左上角
ax_inset = fig.add_axes((0.2, 0.6, 0.2, 0.2))
ax_inset.plot([1, 2, 3, 4], [1, 4, 9, 16])
ax_inset.set_title('Inset Axes')

plt.show()
```
