# 设置坐标轴箭头

```py
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA

fig = plt.figure()

# 添加一个axisartist提供的坐标轴
ax = fig.add_axes((0.1, 0.1, 0.8, 0.8), axes_class=AA.Axes)

# 隐藏顶部及右侧坐的标轴
ax.axis["right"].set_visible(False)
ax.axis["top"].set_visible(False)

# 设置底部及左侧坐标轴的样式
# "-|>"代表实心箭头："->"代表空心箭头
ax.axis["bottom"].set_axisline_style("-|>", size=1.5)
ax.axis["left"].set_axisline_style("-|>", size=1.5)

plt.show()
```
