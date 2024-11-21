# 定积分的几何应用

<!--
\begin{align}
& 设平面区域 D 由 L: r = r(\theta) 及射线 \theta = \alpha, \theta = \beta 围成, \\
& 则区域 D 的面积为: A = \frac{1}{2} \int_{\alpha}^{\beta} r^2(\theta) \mathrm{d} \theta \\
\end{align}
-->

例题

<!--
\begin{align}
& 求 L: (x^2 + y^2)^2 = 4(x^2 - y^2) 围成的面积 \\
& {\color{Green} // 遇到 x^2 + y^2 就转换成极坐标} \\
& 令 \begin{cases}
x = r \cos \theta \\
y = r \sin \theta \\
\end{cases}, \\
& {\color{Green} // L: (r^2 \cos ^2 \theta + r^2 \sin ^2 \theta)^2 = 4(r^2 \cos ^2 \theta - r^2 \sin ^2 \theta)} \\
& {\color{Green} // L: r^4 = 4 r^2(\cos ^2 \theta - \sin ^2 \theta)} \\
& {\color{Green} // L: r^2 = 4(\cos ^2 \theta - \sin ^2 \theta)} \\
& {\color{Green} // L: r^2 = 4 \cos 2 \theta} \\
& 则 L: r^2 = 4 \cos 2 \theta \\
& {\color{Green} // L 是双纽线, 四个象限的面积相等, 求第一象限的面积再乘4即可} \\
& {\color{Green} // A = \frac{1}{2} \int_{\alpha}^{\beta} r^2(\theta) \mathrm{d} \theta} \\
& A = \frac{1}{2} \int_{0}^{\frac{\pi}{4}} r^2(\theta) \mathrm{d} \theta \\
& \;\;\, = \frac{1}{2} \int_{0}^{\frac{\pi}{4}} 4 \cos 2 \theta \mathrm{d} \theta \\
& \;\;\, = \int_{0}^{\frac{\pi}{4}} 2 \cos 2 \theta \mathrm{d} \theta \\
& \;\;\, = \int_{0}^{\frac{\pi}{4}} \cos 2 \theta \mathrm{d}(2 \theta) \\
& \;\;\, = \int_{0}^{\frac{\pi}{2}} \cos \theta \mathrm{d} \theta \\
& \;\;\, = 1 \\
& 整个的面积: 4A = 4 \\
\end{align}
-->

![](../img/di6_1.jpg)
