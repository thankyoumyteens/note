# 换元积分法

例题 1

<!--
\begin{align}
& \;\;\;\; \int_{0}^{4} \frac{x + 1}{\sqrt{2x + 1}} \mathrm{d}x \\
& 方法1 \\
& {\color{Green} // 分子分母同乘2} \\
& = \int_{0}^{4} \frac{2x + 2}{2\sqrt{2x + 1}} \mathrm{d}x \\
& = \frac{1}{2} \int_{0}^{4} \frac{2x + 1 + 1}{\sqrt{2x + 1}} \mathrm{d}x \\
& = \frac{1}{4} \int_{0}^{4} \frac{2x + 1 + 1}{\sqrt{2x + 1}} \mathrm{d}(2x + 1) \\
& = \frac{1}{4} \int_{0}^{4} \frac{2x + 1}{\sqrt{2x + 1}} \mathrm{d}(2x + 1) +
\frac{1}{4} \int_{0}^{4} \frac{1}{\sqrt{2x + 1}} \mathrm{d}(2x + 1) \\
& = \frac{1}{4} \int_{0}^{4} \sqrt{2x + 1} \mathrm{d}(2x + 1) +
\frac{1}{2} \int_{0}^{4} \frac{1}{2\sqrt{2x + 1}} \mathrm{d}(2x + 1) \\
& = \frac{1}{4} \int_{0}^{4} (2x + 1)^{\frac{1}{2}} \mathrm{d}(2x + 1) +
\frac{1}{2} \int_{0}^{4} \frac{1}{2\sqrt{2x + 1}} \mathrm{d}(2x + 1) \\
& = \frac{1}{4} \times \frac{2}{3} (2x + 1)^{\frac{3}{2}} \big|_{0}^{4} +
\frac{1}{2} \int_{0}^{4} \frac{1}{2\sqrt{2x + 1}} \mathrm{d}(2x + 1) \\
& {\color{Green} // \int \frac{1}{2\sqrt{x}} \mathrm{d}x = \sqrt{x} + C} \\
& = \frac{1}{4} \times \frac{2}{3} (2x + 1)^{\frac{3}{2}} \big|_{0}^{4} +
\frac{1}{2} \sqrt{2x + 1}  \big|_{0}^{4} \\
& = \frac{16}{3} \\
\\
& 方法2 \\
& {\color{Green} // 令 \sqrt{2x + 1} = t, 则 x = \frac{1}{2}(t^2 - 1)} \\
& {\color{Green} // 0到4是x的积分上下限, 需要换成t的} \\
& {\color{Green} // x取0时 t = \sqrt{2 \times 0 + 1} = 1} \\
& {\color{Green} // x取4时 t = \sqrt{2 \times 4 + 1} = 3} \\
& = \int_{1}^{3} \frac{\frac{1}{2}(t^2 - 1) + 1}{\sqrt{2 \frac{1}{2}(t^2 - 1) + 1}}
\mathrm{d}[\frac{1}{2}(t^2 - 1)] \\
& = \int_{1}^{3} \frac{\frac{1}{2}(t^2 + 1)}{t} \mathrm{d}[\frac{1}{2}t^2 - \frac{1}{2}] \\
& = \int_{1}^{3} \frac{\frac{1}{2}(t^2 + 1)}{t} t \mathrm{d}t \\
& = \frac{1}{2} \int_{1}^{3} (t^2 + 1) \mathrm{d}t \\
& = \frac{1}{2} \int_{1}^{3} t^2 \mathrm{d}t + \frac{1}{2} \int_{1}^{3} 1 \mathrm{d}t \\
& = \frac{1}{2} \frac{t^3}{3} \big|_{1}^{3} + \frac{1}{2} t \big|_{1}^{3} \\
& = \frac{16}{3} \\
\end{align}
-->

![](../img/di2_1.jpg)

例题 2

<!--
\begin{align}
& \;\;\;\; \int_{0}^{2} x e^{-x^2} \mathrm{d}x \\
& = \frac{1}{2} \int_{0}^{2}e^{-x^2} \mathrm{d}x(x^2) \\
& {\color{Green} // 令 x^2 = t} \\
& {\color{Green} // 0到2是x的积分上下限, 需要换成t的} \\
& {\color{Green} // x取0时 t = 0} \\
& {\color{Green} // x取2时 t = 4} \\
& = \frac{1}{2} \int_{0}^{4}e^{-t} \mathrm{d}xt \\
& = - \frac{1}{2} e^{-t} \big|_{0}^{4} \\
& = \frac{1}{2} (1 - e^{-4}) \\
\end{align}
-->

![](../img/di2_2.jpg)

例题 3

<!--
\begin{align}
& \;\;\;\; f(x) 连续, f(0) = 0, f'(0) = 4,
求 \lim_{x \to 0} \frac{\int_{0}^{x} tf(x^2 - t^2) \mathrm{d}t}{x^4} \\
& {\color{Green} // 被积函数中有x, 需要处理掉} \\
& {\color{Green} // \;\;\;\; \int_{0}^{x} tf(x^2 - t^2) \mathrm{d}t} \\
& {\color{Green} // = \frac{1}{2} \int_{0}^{x} f(x^2 - t^2) \mathrm{d}(t^2)} \\
& {\color{Green} // = - \frac{1}{2} \int_{0}^{x} f(x^2 - t^2) \mathrm{d}(-t^2)} \\
& {\color{Green} // 对于这个积分, x算常数, d里面可以随意加减} \\
& {\color{Green} // = - \frac{1}{2} \int_{0}^{x} f(x^2 - t^2) \mathrm{d}(x^2 - t^2)} \\
& {\color{Green} // 令 x^2 - t^2 = u} \\
& {\color{Green} // t取0时 u = x^2} \\
& {\color{Green} // t取2时 u = 0} \\
& {\color{Green} // = - \frac{1}{2} \int_{x^2}^{0} f(u) \mathrm{d}u} \\
& {\color{Green} // 去掉负号, 需要把积分限对调} \\
& {\color{Green} // = \frac{1}{2} \int_{0}^{x^2} f(u) \mathrm{d}u} \\
& {\color{Green} // 现在被积函数没有 x 了, 用洛必达法则对 x 求导} \\
& = \lim_{x \to 0} \frac{(\frac{1}{2} \int_{0}^{x^2} f(u) \mathrm{d}u)'}{4x^3} \\
& = \lim_{x \to 0} \frac{\frac{1}{2} f(x^2) \cdot 2x}{4x^3} \\
& = \frac{1}{4} \lim_{x \to 0} \frac{xf(x^2)}{x^3} \\
& = \frac{1}{4} \lim_{x \to 0} \frac{f(x^2)}{x^2} \\
& {\color{Green} // f(0) = 0, 用导数的定义} \\
& {\color{Green} // x \to 0 \Rightarrow x^2 \to 0} \\
& = \frac{1}{4} \lim_{x^2 \to 0} \frac{f(x^2) - f(0)}{x^2 - 0} \\
& = \frac{1}{4} f'(0) \\
& = 1 \\
\end{align}
-->

![](../img/di2_3.jpg)
