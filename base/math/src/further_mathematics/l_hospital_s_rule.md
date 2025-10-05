# 洛必达法则

## 定理 1

<!--
\begin{align}
& 用于求0比0型极限 \\
\\
& 如果函数 f(x) 和 g(x) 满足: \\
& \quad 1、 f(x) 和 g(x) 在 x = a 的去心邻域内可导， \\
& \quad\quad \;\; 且 f'(x) \ne 0 \\
& \quad 2、 \lim_{x \to a} f(x) = \lim_{x \to a} g(x) = 0 \\
& \quad 3、 \lim_{x \to a} \frac{g'(x)}{f'(x)} = A \\
& 则 \lim_{x \to a} \frac{g(x)}{f(x)} = A \\
\\
& 注意： \\
& 如果 \lim_{x \to a} \frac{g'(x)}{f'(x)} 不存在，\\
& 这不代表 \lim_{x \to a} \frac{g(x)}{f(x)} 不存在， \\
& 只代表洛必达法则不适用 \\
\end{align}
-->

![](../img/lhsr4.jpg)

例题

<!--
\begin{align}
& 求极限 \lim_{x \to 0} \frac{\arcsin x - x}{x^{2} \ln (1 + 2x)} \\
\\
& \;\,\;\,\;\,\, \lim_{x \to 0} \frac{\arcsin x - x}{x^{2} \ln (1 + 2x)} \\
& \;\, {\color{Green} // 分母是两个式子相乘, 可以用等价无穷小替换} \\
& \;\, = \lim_{x \to 0} \frac{\arcsin x - x}{x^{2} \times 2x} \\
& \;\, = \lim_{x \to 0} \frac{1}{2} \frac{\arcsin x - x}{x^{3}} \\
& \;\, {\color{Green} // 用洛必达法则} \\
& \;\, = \lim_{x \to 0} \frac{1}{2} \frac{\frac{1}{\sqrt{1 - x^{2}}} - 1}{3x^{2}} \\
& \;\, = \lim_{x \to 0} \frac{1}{2} \frac{(1 - x^{2})^{- \frac{1}{2}} - 1}{3x^{2}} \\
& \;\, {\color{Green} // 用等价无穷小替换 (1 + x)^{a} - 1 \sim ax} \\
& \;\, = \lim_{x \to 0} \frac{1}{2} \frac{- \frac{1}{2}(-x^{2})}{3x^{2}} \\
& \;\, = \lim_{x \to 0} \frac{1}{2} \frac{\frac{1}{2}x^{2}}{3x^{2}} \\
& \;\, = \lim_{x \to 0} \frac{1}{12} \\
\end{align}
-->

![](../img/lhsr5.jpg)

## 定理 2

<!--
\begin{align}
& 用于求无穷大比无穷大型极限 \\
\\
& 如果函数 f(x) 和 g(x) 满足: \\
& \quad 1、 f(x) 和 g(x) 在 x = a 的去心邻域内可导， \\
& \quad\quad \;\; 且 f'(x) \ne 0 \\
& \quad 2、 \lim_{x \to a} f(x) = \infty, \lim_{x \to a} g(x) = \infty \\
& \quad 3、 \lim_{x \to a} \frac{g'(x)}{f'(x)} = A \\
& 则 \lim_{x \to a} \frac{g(x)}{f(x)} = A \\
\\
& 注意： \\
& 如果 \lim_{x \to a} \frac{g'(x)}{f'(x)} 不存在，\\
& 这不代表 \lim_{x \to a} \frac{g(x)}{f(x)} 不存在， \\
& 只代表洛必达法则不适用 \\
\end{align}
-->

![](../img/lhsr6.jpg)

无穷大比无穷大型极限一般不用洛必达法则

例题

<!--
\begin{align}
& 求极限 \lim_{x \to + \infty} \frac{\ln ^{2} x}{2x^{2} + x + 3} \\
\\
& \;\,\;\,\;\,\, \lim_{x \to + \infty} \frac{\ln ^{2} x}{2x^{2} + x + 3} \\
& \;\, = \lim_{x \to + \infty} \frac{x^{2}}{2x^{2} + x + 3} \times \frac{\ln ^{2} x}{x^{2}} \\
& \;\, {\color{Green} // 左边是两个多项式相除的极限, m = n 时, 极限为最高次的系数相除} \\
& \;\, = \frac{1}{2} \lim_{x \to + \infty} \frac{\ln ^{2} x}{x^{2}} \\
& \;\, {\color{Green} // 趋于 +\infty 的速度: c^{x} > x^{b} > \ln ^{a} x} \\
& \;\, = \frac{1}{2} \times 0 \\
& \;\, = 0 \\
\end{align}
-->

![](../img/lhsr7.jpg)
