# 拉格朗日中值定理

<!--
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB']
plt.rcParams['axes.unicode_minus'] = False


def f(x):
    return x ** 3 - 3 * x ** 2 + 2


# 曲线
x_start = -1
x_end = 3
x = np.linspace(x_start, x_end, 2000)  # x范围覆盖两个极值点，2000个点确保曲线平滑
y = f(x)

# 斜率
x1 = x_end
x0 = x_start
y1 = f(x1)
y0 = f(x0)
k = (y1 - y0) / (x1 - x0)

# 首尾连线
x_l = np.linspace(x_start, x_end, 2000)
y_l = k * x_l - k * x0 + y0

y_l2 = k * x_l + 2.1

# 创建画布
plt.figure(figsize=(8, 6))

# 绘制函数曲线
plt.plot(x, y, color='#2E86AB', linewidth=2.5)
plt.plot(x_l, y_l, color='#D2B48C', linewidth=1, linestyle='dashed')
plt.plot(x_l, y_l2, color='#CD853F', linewidth=2.5)
plt.plot(-0.1, 2, mfc='green', markersize=5.0, marker='o')
plt.text(-0.1, 2.2, r'$\xi$', fontsize=10, color='green')
plt.text(x_end-0.1, 0, '$L: y=f(x)$', fontsize=10, color='#333333')
plt.text(x_start - 0.2, f(x_start), 'A', fontsize=10, color='#333333')
plt.text(x_end + 0.1, f(x_end), 'B', fontsize=10, color='#333333')


# 坐标轴范围
plt.xlim(-3, 5)
plt.ylim(-3, 5)

# 添加注释线
plt.plot([x_start, x_start], [f(x_start), -3], color='#666666', linestyle='--', linewidth=1, alpha=0.7)
plt.plot([x_end, x_end], [f(x_end), -3], color='#666666', linestyle='--', linewidth=1, alpha=0.7)

# 不绘制坐标轴, 把左下边框作为坐标轴

# 设置刻度
plt.xticks([x_start, x_end], ['a', 'b'])
plt.yticks([f(x_start), f(x_end)], ['A', 'B'])
# 获取当前坐标轴对象
ax = plt.gca()
ax.spines['top'].set_visible(False)  # 隐藏顶部边框
ax.spines['right'].set_visible(False)  # 隐藏右侧边框

# 调整布局并显示
plt.tight_layout()
plt.show()
-->

![](../img/mvt5_1.png)

<!--
\begin{align}
& 设函数 f(x) 满足: \\
& \; 1. f(x) 在 [a, b] 上连续 \\
& \; 2. f(x) 在 (a, b) 内可导 \\
& 则存在 \xi \in (a, b), \\
& 使得 f'(\xi) = \frac{f(b) - f(a)}{b - a} \\
\\
& {\Large 几何意义}\\
& 存在 \xi \in (a, b), \\
& 函数f(x)在点(\xi,f(x))处的切线 \\
& 和(a,f(a))、(b,f(b))两点的连线平行 \\
\\
& {\Large 证明} \\
& 辅助函数: \\
& 1、L：y=f(x) \\
& 2、L_{AB}：y-f(a)=\frac{f(b)-f(a)}{b-a}(x-a) \\
& 即 L_{AB}：y=f(a)+\frac{f(b)-f(a)}{b-a}(x-a) \\
& 证明：\\
& 令 \varphi (x)=曲线-直线=f(x)-f(a)-\frac{f(b)-f(a)}{b-a}(x-a) \\
& {\color{Green} // 加、减、乘不会改变连续性和可导性} \\
& \varphi (x) 在 [a, b] 上连续、在 (a, b) 内可导 \\
& {\color{Green} // a、b是曲线和直线的交点，所以它们的函数值相等} \\
& \varphi (a)=\varphi (b)=0 \\
& 满足罗尔定理 \\
& 所以存在 \xi \in (a, b)，使\varphi '(\xi)=0 \\
& 而\varphi '(x)=f'(x)-\frac{f(b)-f(a)}{b-a} \\
& 所以 \varphi '(\xi) =f'(\xi)-\frac{f(b)-f(a)}{b-a} \\
& f'(\xi)=\frac{f(b)-f(a)}{b-a} \\
\end{align}
-->

![](../img/mvt5.jpg)

<!--
\begin{align}
& 当 f(a) = f(b) 时, 拉格朗日中值定理即为罗尔定理, 即罗尔定理是拉格朗日中值定理的特例 \\
& 拉格朗日中值定理的等价形式: \\
& \;\, 1. f(b) - f(a) = f'(\xi)(b - a) \\
& \;\, 2. f(b) - f(a) = f'[a + \theta(b - a)](b - a), \; 0 \lt \theta \lt 1 \\
\end{align}
-->

![](../img/mvt6.jpg)

### 例题

<!--
\begin{align}
& 设 f(x) 二阶可导, 且 f''(x) > 0, 判断 f'(0), f'(1), f(1) - f(0) 的大小 \\
\\
& \;\, {\color{Green} // 看到 f(b) - f(a), 使用拉格朗日定理} \\
& \;\, f(1) - f(0) = f'(c)(1 - 0) = f'(c), \; 0 < c < 1 \\
& 因为 f''(x) > 0, 所以 f'(x) 单调递增 \\
& 因为 0 < c < 1, 所以 f'(0) < f'(c) < f'(1) \\
& 所以 f'(0) < f(1) - f(0) < f'(1) \\
\end{align}
-->

![](../img/mvt7.jpg)

<!--
\begin{align}
& 设 f(x) 可导, 且 \lim_{x \to \infty} f'(x) = e, 求 \lim_{x \to \infty} [f(x + 2) - f(x - 1)] \\
\\
& \;\, {\color{Green} // 看到 f(b) - f(a), 使用拉格朗日定理} \\
& \;\, f(x + 2) - f(x - 1) = f'(c)(x + 2 - x + 1) = 3f'(c), \; x - 1 < c < x + 2 \\
& \;\, \lim_{x \to \infty} [f(x + 2) - f(x - 1)] = \lim_{x \to \infty} [3f'(c)]
= 3 \lim_{x \to \infty} f'(c) = 3e \\
\end{align}
-->

![](../img/mvt8.jpg)

<!--
\begin{align}
& 求 \lim_{x \to +\infty} x^{2}(\sin \frac{1}{x - 1} - \sin \frac{1}{x + 1}) \\
\\
& \;\, {\color{Green} // 看到 f(b) - f(a), 使用拉格朗日定理} \\
& 令 f(t) = \sin t, 则 f'(t) = \cos t \\
& 则 \sin \frac{1}{x - 1} - \sin \frac{1}{x + 1} = f(\frac{1}{x - 1}) - f(\frac{1}{x + 1}) \\
& \;\, f(\frac{1}{x - 1}) - f(\frac{1}{x + 1}) = f'(\xi)(\frac{1}{x - 1} - \frac{1}{x + 1}) \\
& \;\, = \frac{2}{x^{2} - 1} \cos \xi, \quad \frac{1}{x - 1} < \xi < \frac{1}{x + 1} \\
& \;\, \lim_{x \to +\infty} x^{2}(\sin \frac{1}{x - 1} - \sin \frac{1}{x + 1}) \\
& \;\, = \lim_{x \to +\infty} x^{2}(\frac{2}{x^{2} - 1} \cos \xi) \\
& \;\, = \lim_{x \to +\infty} \frac{2x^{2}}{x^{2} - 1} \cos \xi \\
& \;\, = 2 \lim_{x \to +\infty} \cos \xi \\
& \;\, x 趋于 +\infty 时, \frac{1}{x - 1} 和 \frac{1}{x + 1} 都趋于 0, 所以 \xi 也趋于 0 \\
& 所以 2 \lim_{x \to +\infty} \cos \xi = 2 \times 1 = 2 \\
\end{align}
-->

![](../img/mvt9.jpg)

<!--
\begin{align}
& 设 f(x) 二阶可导, \lim_{x \to 0} \frac{f(x) - 1}{x} = 1, f(1) = 2,
证明: 存在 \xi \in (0, 1), 使 f''(\xi) = 0 \\
\\
& \;\, \lim_{x \to 0} \frac{f(x) - 1}{x} = 1 \\
& \;\, x \to 0 时, 分母趋于 0, 而极限值是1, 所以分子一定也趋于 0 \\
& 所以 \lim_{x \to 0} [f(x) - 1] = 0 \\
& \;\, \lim_{x \to 0} f(x) = 1 \\
& 又因为 f(x) 二阶可导, 所以 f(x) 一阶可导, 所以 f(x) 连续, 极限值等于函数值 \\
& 所以 f(0) = 1 \\
& \;\, f'(0) = \lim_{x \to 0} \frac{f(x) - f(0)}{x - 0}
= \lim_{x \to 0} \frac{f(x) - 1}{x} = 1 \\
& \;\, {\color{Green} // f(0) = 1, f(1) = 2, 看到 f(a) \ne f(b), 使用拉格朗日中值定理} \\
& 存在 c \in (0, 1), 使 f'(c) = \frac{f(1) - f(0)}{1 - 0} = 1 \\
& 因为 f(x) 二阶可导, 所以一阶导数连续, 又因为 f'(0) = f'(c) = 1 \\
& \;\, {\color{Green} // 使用罗尔定理} \\
& 所以, 存在 \xi \in (0, c), 使 f''(\xi) = 0, \quad (0, 1) 包含 (0, c) \\
\end{align}
-->

![](../img/mvt10.jpg)
