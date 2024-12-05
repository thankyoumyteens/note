# 双轴图

```py
import matplotlib.pyplot as plt
import numpy as np

# 创建数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)  # 主坐标轴数据
y2 = 100 * np.cos(x)  # 次坐标轴数据

# 创建图形和主坐标轴
fig, ax1 = plt.subplots()

# 绘制主坐标轴数据
color = 'tab:red'
ax1.set_xlabel('X轴')
ax1.set_ylabel('Y1轴 (sin)', color=color)
ax1.plot(x, y1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# 创建一个与主坐标轴共享 x 轴但具有独立 y 轴的次坐标轴
ax2 = ax1.twinx()

# 绘制次坐标轴数据
color = 'tab:blue'
ax2.set_ylabel('Y2轴 (cos)', color=color)
ax2.plot(x, y2, color=color)
ax2.tick_params(axis='y', labelcolor=color)

# 设置标题
fig.suptitle('双轴图示例')

# 调整布局
fig.tight_layout()

plt.show()
```
