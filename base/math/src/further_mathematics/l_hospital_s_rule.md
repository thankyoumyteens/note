# 洛必达法则

<!--
\begin{align}
& (1) f(b) - f(a) 或者 f(a) \ne f(b), 解法: 使用拉格朗日 \\
& (2) 见到类似于 \xi f'(\xi) + 2f(\xi) 这种只有中值 \xi 且导数差一阶, 解法: \\
& \quad 1、 把 \xi 换成 x \Rightarrow x f'(x) + 2f(x) \\
& \quad 2、 构造成分子比分母多一阶导数的形式 \Rightarrow \frac{f'(x)}{f(x)} + ... = 0 \\
& \quad 3、 导数还原 \Rightarrow [\ln f(x)]' + (...)' = 0 \\
& \quad 4、 把两项合成一项, 取\ln 内部 作为 \varphi (x) \Rightarrow \varphi (x) = ... \\
& (3) 有中值 \xi, 有边界 a 和 b, 且 \xi 和 a, b 可以分开, 解法: \\
& \quad 1、 把 \xi 和 a, b 分开 \\
& \quad 2、 如果 a, b 这一侧可以变形成 \frac{f(b) - f(a)}{b - a}, 则使用拉格朗日定理 \\
& \quad 3、 如果 a, b 这一侧可以变形成 \frac{f(b) - f(a)}{g(b) - g(a)}, 则使用柯西定理 \\
\end{align}
-->

![](../img/lhsr1.jpg)

<!--
\begin{align}
& 当 x 趋于 +\infty 时, 下列函数也趋于 +\infty \\
& \;\, (1) \ln ^{a} x \quad (a > 0) \\
& \;\, (2) x^{b} \quad (b > 0) \\
& \;\, (3) c^{x} \quad (c > 1) \\
& 这三个函数趋于 +\infty 的速度: c^{x} > x^{b} > \ln ^{a} x \\
\\
& 例1, 求 \lim_{x \to + \infty} \frac{\ln ^{80} x}{\sqrt{x}} \\
& 因为趋于 +\infty 的速度 x^{b} > \ln ^{a} x \\
& 所以极限 \lim_{x \to + \infty} \frac{\ln ^{80} x}{\sqrt{x}} = 0 \\
\\
& 例2, 求 \lim_{x \to + \infty} \frac{x^{60}}{2^{x}} \\
& 因为趋于 +\infty 的速度 c^{x} > x^{b} \\
& 所以极限 \lim_{x \to + \infty} \frac{x^{60}}{2^{x}} = 0 \\
\end{align}
-->

![](../img/lhsr2.jpg)

<!--

-->

<!--
在计算 \frac{0}{0} 型及 \frac{\infty}{\infty} 型函数极限时, 可以用洛必达法则
-->
