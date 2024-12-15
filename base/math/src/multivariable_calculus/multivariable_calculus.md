# 多元函数微分学

<!--
\begin{align}
& 设 M_0 (x_0, y_0) 为 xOy 平面上的一点, \delta > 0, \\
& 称区域 \left \{ (x, y) | \sqrt{(x - x_0)^2 + (y - y_0)^2} < \delta \right \} \\
& 为点 M_0 的 \delta 邻域, 记为 U(M_0,\delta) \\
& 称区域 \left \{ (x, y) | 0 < \sqrt{(x - x_0)^2 + (y - y_0)^2} < \delta \right \} \\
& 为点 M_0 的 \delta 去心邻域, 记为 \mathring{U}(M_0,\delta) \\
\end{align}
-->

![](../img/mc1.jpg)

<!--
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.axisartist as AA

circle = plt.Circle((1, 2), 0.5, fill=True, facecolor='#CCCCCC', edgecolor='black', lw=1, ls='dotted')

x = np.linspace(1, 2, 1)
y = x * 2

fig = plt.figure()

# 添加一个坐标轴
ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8), axes_class=AA.Axes)
ax_main.set_xlim(left=0, right=5)
ax_main.set_ylim(bottom=0, top=5)
# 隐藏顶部及右侧坐的标轴
ax_main.axis["right"].set_visible(False)
ax_main.axis["top"].set_visible(False)
# 设置底部及左侧坐标轴的样式
ax_main.axis["bottom"].set_axisline_style("-|>", size=1.5)
ax_main.axis["left"].set_axisline_style("-|>", size=1.5)

# 设置x轴的刻度
ax_main.set_xticks([1])
# 设置每个刻度对应的标签
ax_main.set_xticklabels([r'$x_0$'])

# 设置y轴的刻度
ax_main.set_yticks([2])
# 设置每个刻度对应的标签
ax_main.set_yticklabels([r'$y_0$'])

# 绘制到x轴的注释线
ax_main.vlines(x=1, ymin=0, ymax=2, color='b', linestyles='dotted')
# 绘制到y轴的注释线
ax_main.hlines(y=2, xmin=0, xmax=1, color='b', linestyles='dotted')

# 绘制图像
ax_main.plot(x, y, ms=5, marker='o', color='b')
ax_main.text(1.1, 2, r'$M_0$', fontsize=12, color='black')

# 将圆形添加到坐标轴中
ax_main.add_artist(circle)
# 令x轴和y轴长度相同, 保证圆形的形状正确
ax_main.set_aspect('equal')

plt.show()
-->

![](../img/Figure_1.png)

## 二元函数的极限

<!--
\begin{align}
& 设二元函数 z = f(x, y) 在点 M_0(x_0, y_0) 的去心邻域内有定义, \\
& \;\, A 为常数，若对任意的 \varepsilon > 0, 总存在 \delta > 0, \\
& 当 0 < \sqrt{(x - x_0)^2 + (y - y_0)^2} < \delta 时, \\
& 有 | f(x, y) - A | < \varepsilon 成立, \\
& 则称函数 z = f(x, y) 当 (x, y) \to (x_0, y_0) 时以 A 为极限, \\
& 记为 \lim\limits_{\substack{x \to x_0 \\ y \to y_0}} f(x, y) = A \\
\end{align}
-->

![](../img/mc2.jpg)
