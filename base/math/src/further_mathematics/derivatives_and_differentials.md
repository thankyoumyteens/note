# 导数与微分

## 导数

<!--
\begin{align}
& 设 y = f(x), x \in D, x_{0} \in D, 在点 x_{0} 处取一个增量 \Delta x, \\
& 则 \Delta y = f(x_{0} + \Delta x) - f(x_{0}) \\
& 若极限 \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x} = \lim_{\Delta x \to 0} \frac{f(x_{0} + \Delta x) - f(x_{0})}{\Delta x} 存在 \\
& 则称函数 f(x) 在点 x_{0} 处可导, 极限值称为函数 f(x) 在点 x_{0} 处的导数, \\
& 记为 f'(x_{0}) 或 \frac{\mathrm{d} y}{\mathrm{d} x} \bigg| _{x = x_{0}}
\end{align}
-->

![](../img/dad1.jpg)

<!--
\begin{align}
& 1. \; f(x) 在 x_{0} 处可导的等价定义: f'(x_{0}) = \lim_{x \to x_{0}} \frac{f(x) - f(x_{0})}{x - x_{0}} \\
& 2. \; 左导数: f'_{-}(x_{0}) = \lim_{x \to x_{0}^{-}} \frac{f(x) - f(x_{0})}{x - x_{0}} \\
& 3. \; 右导数: f'_{+}(x_{0}) = \lim_{x \to x_{0}^{+}} \frac{f(x) - f(x_{0})}{x - x_{0}} \\
& 4. \; f(x) 在 x_{0} 处可导的充分必要条件是: 左右导数都存在且相等 \\
& 5. \; 若 f(x) 在 x_{0} 处可导, 则 f(x) 在 x_{0} 处连续, 反之不对 \\
\end{align}
-->

![](../img/dad2.jpg)

例题 1

<!--
\begin{align}
& 函数 f(x) = \begin{cases}
\frac{x \cdot 2^{\frac{1}{x}}}{1 + 2^{\frac{1}{x}}}, & x \ne 0 \\
0, & x = 0 \\
\end{cases}, 求 f'(0) 是否存在 \\
\\
& f'(x) = \lim_{x \to 0} \frac{f(x) - f(0)}{x - 0}
= \lim_{x \to 0} \frac{x \cdot 2^{\frac{1}{x}}}{1 + 2^{\frac{1}{x}}} \cdot \frac{1}{x}
= \lim_{x \to 0} \frac{2^{\frac{1}{x}}}{1 + 2^{\frac{1}{x}}} \\
& f'_{-}(0) = \lim_{x \to 0^{-}} \frac{2^{\frac{1}{x}}}{1 + 2^{\frac{1}{x}}} = 0 \\
& f'_{+}(0) = \lim_{x \to 0^{+}} \frac{2^{\frac{1}{x}}}{1 + 2^{\frac{1}{x}}} = 1 \\
& f'(0) 不存在 \\
\end{align}
-->

![](../img/dad3.jpg)
