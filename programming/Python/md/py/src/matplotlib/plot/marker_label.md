# 绘制数据点的标签

```py
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 10, 10)
y = x * 2

fig = plt.figure()

ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8))
ax_main.set_xlim(left=0, right=10)
ax_main.set_ylim(bottom=0, top=20)

# 绘制点(3, 6)的标签
# 3.2是向右偏移一点, 以免挡住数据点
ax_main.text(3.2, 6, r'$P_1$', fontsize=12, color='red')

ax_main.plot(x, y, ms=5, ls='None', marker='o')
plt.show()
```
