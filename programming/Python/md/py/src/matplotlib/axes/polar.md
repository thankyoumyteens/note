# 创建极坐标

```py
import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0, 2 * np.pi, 100)
# r = cos 2θ
r = np.cos(2 * theta)

fig = plt.figure()

# 添加一个极坐标轴
ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8), polar=True)

# 在坐标轴上绘图
ax_main.plot(theta, r)

plt.show()
```
