# 中值定理

极值点的导数要么等于 0 要么不存在。

费马定理

<!--
\begin{align}
& 设函数 f(x) 可导, 且在 x = a 处取极值, \\
& 则 f'(a) = 0, 反之不对 \\
\end{align}
-->

![](../img/mvt1.jpg)

## 罗尔定理

<!--
\begin{align}
& 设函数 f(x) 满足: \\
& \; 1. f(x) 在 [a, b] 上连续 \\
& \; 2. f(x) 在 (a, b) 内可导 \\
& \; 3. f(a) = f(b) \\
& 则存在 \xi \in (a, b), 使得 f'(\xi) = 0 \\
\end{align}
-->

![](../img/mvt2.jpg)

例题 1

<!--
\begin{align}
& 验证函数 f(x) = x^{2} - 2x + 4 在 [0, 2] 上满足罗尔定理的条件, 并求驻点 \xi \\
\\
& \;\, // 驻点是导数等于0的点 \\
& \;\, f(x)是多项式, 多项式函数不仅在每一点连续, 而且在任何有限区间上都可导 \\
& \;\, f(0) = f(2) = 4 \\
& 所以存在 \xi \in (0, 2), 使 f'(\xi) = 0 \\
& f'(x) = 2x - 2 \\
& 所以 \xi = 1 \\
\\
& 多项式的格式: \\
& \;\, p(x) = a_n x^n + a_{n-1} x^{n-1} + \ldots + a_2 x^2 + a_1 x + a_0 \\
& 其中 a_n, a_{n-1}, \ldots, a_1, a_0 是常数, n 是非负整数。\\
\end{align}
-->

![](../img/mvt3.jpg)

例题 2

<!--
\begin{align}
& 设 f(x) 在 [0, 2] 上连续, 在 (0, 2) 内可导, 且 f(0) = 1, f(1) + f(2) = 2, \\
& 证明: 存在 \xi \in (0, 2), 使得 f'(\xi) = 0 \\
\\
& \;\, // 闭区间连续, 函数值相加 \Rightarrow 使用介值定理 \\
& 因为 f(x) 在 [0, 2] 上连续, 所以存在最大值 M 和最小值 m \\
& \;\, 2m \le f(1) + f(2) \le 2M \\
& 因为 f(1) + f(2) = 2 \\
& 所以 2m \le 2 \le 2M \Rightarrow m \le 1 \le M \\
& 所以 1 是介值 \\
& 所以存在 c \in [1, 2], 使 f(c) = 1 \\
& 因为 f(0) = 1 \\
& 所以 f(0) = f(c) \\
& 而 c \ne 0 \\
& 根据罗尔定理, 存在 \xi \in (0, c), 使 f'(\xi) = 0 \\
\end{align}
-->

![](../img/mvt4.jpg)

## 拉格朗日中值定理

<!--
\begin{align}
& 设函数 f(x) 满足: \\
& \; 1. f(x) 在 [a, b] 上连续 \\
& \; 2. f(x) 在 (a, b) 内可导 \\
& 则存在 \xi \in (a, b), \\
& 使得 f'(\xi) = \frac{f(b) - f(a)}{b - a} \\
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

例题 1

<!--
\begin{align}
& 设 f(x) 二阶可导, 且 f''(x) > 0, 判断 f'(0), f'(1), f(1) - f(0) 的大小 \\
\\
& \;\, // 看到 f(b) - f(a), 使用拉格朗日定理 \\
& \;\, f(1) - f(0) = f'(c)(1 - 0) = f'(c), \; 0 < c < 1 \\
& 因为 f''(x) > 0, 所以 f'(x) 单调递增 \\
& 因为 0 < c < 1, 所以 f'(0) < f'(c) < f'(1) \\
& 所以 f'(0) < f(1) - f(0) < f'(1) \\
\end{align}
-->

![](../img/mvt7.jpg)

例题 2

<!--
\begin{align}
& 设 f(x) 可导, 且 \lim_{x \to \infty} f'(x) = e, 求 \lim_{x \to \infty} [f(x + 2) - f(x - 1)] \\
\\
& \;\, // 看到 f(b) - f(a), 使用拉格朗日定理 \\
& \;\, f(x + 2) - f(x - 1) = f'(c)(x + 2 - x + 1) = 3f'(c), \; x - 1 < c < x + 2 \\
& \;\, \lim_{x \to \infty} [f(x + 2) - f(x - 1)] = \lim_{x \to \infty} [3f'(c)]
= 3 \lim_{x \to \infty} f'(c) = 3e \\
\end{align}
-->

![](../img/mvt8.jpg)

例题 3

<!--
\begin{align}
& 求 \lim_{x \to +\infty} x^{2}(\sin \frac{1}{x - 1} - \sin \frac{1}{x + 1}) \\
\\
& \;\, // 看到 f(b) - f(a), 使用拉格朗日定理 \\
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
