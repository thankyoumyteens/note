# 坐标轴刻度

```py
import matplotlib.pyplot as plt
import numpy as np

# 创建数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘制图形
plt.plot(x, y)

# 设置 x 轴刻度
# 参数: 刻度位置、刻度上显示的内容
plt.xticks([0, 2, 4, 6, 8, 10], ['zero', 'two', 'four', 'six', 'eight', 'ten'])

# 设置 y 轴刻度
plt.yticks([-1, 0, 1], ['min', 'zero', 'max'])

plt.show()
```
