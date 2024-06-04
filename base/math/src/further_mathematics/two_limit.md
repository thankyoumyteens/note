# 两个重要极限

<!--
\begin{align}
& (1) \; \lim_{\Delta \to 0} (1 + \Delta)^{\frac{1}{\Delta}} = e, \quad \Delta 可以替换为任意表达式 \\
& \quad \;\, 比如: \lim_{x \to 0} (1 + x)^{\frac{1}{x}} = e \\
& (2) \; \lim_{\Delta \to 0} \frac{\sin \Delta}{\Delta} = 1, \quad \Delta 可以替换为任意表达式 \\
& \quad \;\, 比如: \lim_{x \to 0} \frac{\sin x}{x} = 1 \\
\end{align}
-->

![](../img/tl1.jpg)

例题 1

<!--
\begin{align}
& 求极限: \\
& \quad\;\; \lim_{x \to 0} \frac{1 - \cos ^{3} x}{x \ln (1 + 2x)} \\
& \; \, \; // 分母是两个无穷小相乘的话, 用等价无穷小替换 \\
& \; \, \; // \ln (1 + 2x) 替换成 2x \\
& \; \, = \lim_{x \to 0} \frac{1 - \cos ^{3} x}{x \cdot 2x} \\
& \; \, = \frac{1}{2} \lim_{x \to 0} \frac{1 - \cos ^{3} x}{x^{2}} \\
& \; \, \; // 使用立方差公式 \\
& \; \, = \frac{1}{2} \lim_{x \to 0} (1 + \cos x + \cos ^{2} x) \frac{1 - \cos x}{x^{2}} \\
& \; \, \; // 分子用等价无穷小替换 \\
& \; \, = \frac{1}{2} \lim_{x \to 0} (1 + \cos x + \cos ^{2} x) \frac{\frac{1}{2}x^{2}}{x^{2}} \\
& \; \, = \frac{1}{4} \lim_{x \to 0} (1 + \cos x + \cos ^{2} x) \\
& \; \, = \frac{1}{4} \lim_{x \to 0} (1 + 1 + 1) \\
& \; \, = \frac{3}{4} \\
\end{align}
-->

![](../img/tl2.jpg)

例题 2
