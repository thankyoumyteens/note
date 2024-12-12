# 创建直角坐标

```py
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 10)
y = x * 2

fig = plt.figure()

# 添加一个坐标轴
ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8))

# 在坐标轴上绘图
ax_main.plot(x, y)

plt.show()
```
