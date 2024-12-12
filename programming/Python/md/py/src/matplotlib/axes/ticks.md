# 设置坐标轴刻度

```py
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 10)
y = x * 2

fig = plt.figure()

# 添加一个坐标轴
ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8))

# 设置x轴的刻度
ax_main.set_xticks([0, 2, 4, 6, 8, 10])
# 设置每个刻度对应的标签
ax_main.set_xticklabels(['zero', 'two', 'four', 'six', 'eight', 'ten'])

# 设置y轴的刻度
ax_main.set_yticks([0, 4, 8, 12, 16, 20])
# 设置每个刻度对应的标签
ax_main.set_yticklabels(['zero', 'four', 'eight', 'twelve', 'sixteen', 'twenty'])

# 绘制图像
ax_main.plot(x, y)
ax_main.set_title('Main Axes')

plt.show()
```
