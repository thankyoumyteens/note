# 数学表达式

Matplotlib 支持使用 LaTeX 标记来显示数学表达式。

```py
import numpy as np
import matplotlib.pyplot as plt

# 创建数据
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)

# 设置标题与标签, 包含LaTeX数学表达式
ax.set_title(r'$\alpha_i > \beta_i$', fontsize=20, color='blue')
ax.set_xlabel(r'$\Delta_i(j)$', fontsize=20)
ax.set_ylabel(r'some numbers')

# 添加带有数学表达式的文本
textstr = r'an equation: $E=mc^2$'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

# 在图中标记一个点并添加注释
ax.annotate('local max', xy=(0.5, 1), xytext=(0.8, 0.8),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )

plt.show()
```
