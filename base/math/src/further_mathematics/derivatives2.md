# 导数的应用

## 渐近线

<!--
\begin{align}
& 水平渐近线: 设曲线 L: y = f(x), 若 \lim_{x \to \infty} f(x) = A, \\
& 则称直线 y = A 为曲线 L 的水平渐近线 \\
\\
& 铅直渐近线: 设曲线 L: y = f(x), \\
& 若下列任意情况成立 \begin{cases}
\lim_{x \to a} f(x) = \infty \\
\lim_{x \to a^-} f(x) = \infty \\
\lim_{x \to a^+} f(x) = \infty \\
\end{cases} \\
& 则称直线 x = a 为曲线 L 的铅直渐近线 \\
\\
& 斜渐近线: 设曲线 L: y = f(x), 若 \lim_{x \to \infty} \frac{f(x)}{x} = a (a \ne 0, a \ne \infty), \\
& \lim_{x \to \infty} [f(x) - ax] = b, \\
& 则称直线 y = ax + b 为曲线 L 的斜渐近线 \\
\end{align}
-->

![](../img/d2_14.jpg)

![](../img/d2_15.jpg)

例题 1

<!--
\begin{align}
& 求曲线 y = \frac{x^2 - 3x + 2}{x^2 - 1} e^{\frac{1}{x}} 的水平渐近线和铅直渐近线 \\
\\
& \;\,\;\, \;\, \;\, \lim_{x \to \infty} \frac{x^2 - 3x + 2}{x^2 - 1} e^{\frac{1}{x}} \\
& \;\, {\color{Green} // 两个多项式相除的极限, m = n 时, 极限为最高次的系数相除} \\
& \;\, = 1 \times \lim_{x \to \infty} e^{\frac{1}{x}} \\
& \;\, = 1 \times 1 \\
& \;\, = 1 \\
& 所以 y = 1 是曲线的水平渐近线 \\
\\
& 找出 y 间断的地方: x = 1 或 x = -1 或 x = 0 时间断 \\
& \;\,\;\, \;\, \;\, \lim_{x \to -1} \frac{x^2 - 3x + 2}{x^2 - 1} e^{\frac{1}{x}} \\
& \;\, {\color{Green} // 分子趋于6, 分母趋于0} \\
& \;\, = \infty \\
& 所以 x = -1 是曲线的铅直渐近线 \\
\\
& \;\,\;\, \;\, \;\, \lim_{x \to 0^+} \frac{x^2 - 3x + 2}{x^2 - 1} e^{\frac{1}{x}} \\
& \;\, = - \infty \\
& 所以 x = 0 是曲线的铅直渐近线 \\
\\
& \;\,\;\, \;\, \;\, \lim_{x \to 1} \frac{x^2 - 3x + 2}{x^2 - 1} e^{\frac{1}{x}} \\
& \;\, = \lim_{x \to 1} \frac{(x - 1)(x - 2)}{(x + 1)(x - 1)} e^{\frac{1}{x}} \\
& \;\, = \lim_{x \to 1} \frac{x - 2}{x + 1} e^{\frac{1}{x}} \\
& \;\, = - \frac{1}{2} \\
& 所以 x = 1 不是铅直渐近线 \\
\end{align}
-->

![](../img/d2_16.jpg)

例题 2

<!--
\begin{align}
& 求曲线 y = \frac{2x^2 - x + 3}{x + 1} 的斜渐近线 \\
\\
& \;\,\;\, \;\, \;\, \lim_{x \to \infty} \frac{2x^2 - x + 3}{x + 1} \\
& \;\, {\color{Green} // 两个多项式相除的极限, m > n 时, 极限为 \infty} \\
& \;\, = \infty \\
& 所以曲线没有水平渐近线 \\
\\
& 找出 y 间断的地方: x = -1 时间断 \\
& \;\,\;\, \;\, \;\, \lim_{x \to -1} \frac{2x^2 - x + 3}{x + 1} \\
& \;\, {\color{Green} // 分子趋于6, 分母趋于0} \\
& \;\, = \infty \\
& 所以 x = -1 是曲线的铅直渐近线 \\
\\
& \;\,\;\, \;\, \;\, \lim_{x \to \infty} \frac{f(x)}{x} \\
& \;\, = \lim_{x \to \infty} \frac{2x^2 - x + 3}{x^2 + x} \\
& \;\, {\color{Green} // 两个多项式相除的极限, m = n 时, 极限为最高次的系数相除} \\
& \;\, = 2 \\
& \;\,\;\, \;\, \;\, \lim_{x \to \infty} [f(x) - 2x] \\
& \;\, = \lim_{x \to \infty} \frac{- 3x + 3}{x + 1} \\
& \;\, = -3 \\
& 所以 y = 2x - 3 是曲线的斜渐近线 \\
\end{align}
-->

![](../img/d2_17.jpg)

例题 3

<!--
\begin{align}
& 求曲线 y = \sqrt{x^2 + 4x + 8} - x 的所有渐近线 \\
\\
& \;\,\;\, \;\, \;\, \lim_{x \to - \infty} \sqrt{x^2 + 4x + 8} - x \\
& \;\, = + \infty \\
& \;\,\;\, \;\, \;\, \lim_{x \to + \infty} \sqrt{x^2 + 4x + 8} - x \\
& \;\, = \lim_{x \to + \infty} \frac{4x + 8}{\sqrt{x^2 + 4x + 8} + x} \\
& \;\, {\color{Green} // 两个多项式相除的极限, m = n 时, 极限为最高次的系数相除} \\
& \;\, = \lim_{x \to + \infty} \frac{4}{2} \\
& \;\, = 2 \\
& 所以 y = 2 是曲线的水平渐近线 \\
\\
& \;\, y = \sqrt{x^2 + 4x + 8} - x 没有间断点 \\
& 所以曲线没有铅直渐近线 \\
\\
& 由于右侧有水平渐近线, 所以右侧没有斜渐近线, 只考虑左侧 \\
& \;\,\;\, \;\, \;\, \lim_{x \to - \infty} \frac{f(x)}{x} \\
& \;\, = \lim_{x \to - \infty} \frac{\sqrt{x^2 + 4x + 8} - x}{x} \\
& \;\, {\color{Green} // 两个多项式相除的极限, m = n 时, 极限为最高次的系数相除} \\
& \;\, = \lim_{x \to + \infty} \frac{-2}{1} \\
& \;\, = -2 \\
& \;\,\;\, \;\, \;\, \lim_{x \to - \infty} [f(x) + 2x] \\
& \;\, = \lim_{x \to - \infty} \sqrt{x^2 + 4x + 8} + x \\
& \;\, = \lim_{x \to - \infty} \frac{4x + 8}{\sqrt{x^2 + 4x + 8} - x} \\
& \;\, {\color{Green} // 两个多项式相除的极限, m = n 时, 极限为最高次的系数相除} \\
& \;\, = \lim_{x \to - \infty} \frac{4}{-2} \\
& \;\, = -2 \\
& 所以 y = =2x - 2 是曲线的斜渐近线 \\
\end{align}
-->

![](../img/d2_18.jpg)
