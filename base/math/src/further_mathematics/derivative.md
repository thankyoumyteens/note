# 求导工具

## 求导基本公式

<!--
\begin{align}
& 1. \; (常数)' = 0 \\
& 2. \; (x^{a})' = ax^{a - 1} \\
& \quad 2.1. \; (\sqrt{x})' = \frac{1}{2\sqrt{x}} \\
& \quad 2.2. \; (\frac{1}{x})' = - \frac{1}{x^{2}} \\
& 3. \; (a^{x})' = a^{x} \ln a \\
& \quad 3.1. \; (e^{x})' = e^{x} \\
& 4. \; (\log_{a}{x})' = \frac{1}{x \ln a} \\
& \quad 4.1. \; (\ln x)' = \frac{1}{x} \\
& 5. \; (\sin x)' = \cos x \\
& 6. \; (\cos x)' = - \sin x \\
& 7. \; (\tan x)' = \sec^{2} x \\
& 8. \; (\cot x)' = - \csc^{2} x \\
& 9. \; (\sec x)' = \sec x \tan x \\
& 10. \; (\csc x)' = - \csc x \cot x \\
& 11. \; (\arcsin x)' = \frac{1}{\sqrt{1 - x^{2}}} \\
& 12. \; (\arccos x)' = - \frac{1}{\sqrt{1 - x^{2}}} \\
& 13. \; (\arctan x)' = \frac{1}{1 + x^{2}} \\
& 14. \; (\operatorname{arccot} x)' = - \frac{1}{1 + x^{2}} \\
\end{align}
-->

![](../img/d1.jpg)

## 导数的四则运算法则

<!--
\begin{align}
& 1. \; (u \pm v)' = u' \pm v' \\
& 2. \; (u \cdot v)' = u'v + uv' \\
& 3. \; (ku)' = ku', k 为常数 \\
& 4. \; (u \cdot v \cdot w)' = u'vw + uv'w + uvw' \\
& 5. \; (\frac{u}{v})' = \frac{u'v + uv'}{v^{2}}, v \ne 0 \\
\end{align}
-->

![](../img/d2.jpg)

## 复合函数求导

<!--
\begin{align}
& \; y = f(u) 可导, u = \varphi (x) 可导, 且 \varphi '(x) \ne 0, \\
& 则 \frac{\mathrm{d} y}{\mathrm{d} x}
= \frac{\mathrm{d} y}{\mathrm{d} u} \cdot \frac{\mathrm{d} u}{\mathrm{d} x}
= f'(u) \cdot \varphi '(x) = f'[\varphi (x)] \varphi '(x) \\
\end{align}
-->

![](../img/d3.jpg)
