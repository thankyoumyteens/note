# 分部积分法

分部积分公式

<!--
\begin{align}
& 因为 (uv)' = u'v + uv' \\
& 两边同时积分 uv = \int u'v \mathrm{d}x + \int uv' \mathrm{d}x \\
& \qquad\qquad\qquad\,\,\,\, = \int v \mathrm{d}u + \int u \mathrm{d}v \\
& 所以 \int u \mathrm{d}v = uv - \int v \mathrm{d}u \\
\end{align}
-->

![](../img/ii3_1.jpg)

使用场景 1: 幂函数乘指数函数

<!--
\begin{align}
& \;\;\;\; \int x^2 e^x \mathrm{d}x \\
& {\color{Green} // 幂函数乘指数函数, 使用分部积分} \\
& {\color{Green} // 令 x^2 作为 u, e^x 作为 v} \\
& {\color{Green} // 把 e^x 放到 d 后面} \\
& = \int x^2 \mathrm{d}(e^x) \\
& {\color{Green} // \int u \mathrm{d}v = uv - \int v \mathrm{d}u} \\
& = x^2 e^x - \int e^x \mathrm{d}(x^2) \\
& = x^2 e^x - \int 2xe^x \mathrm{d}x \\
& = x^2 e^x - 2 \int xe^x \mathrm{d}x \\
& {\color{Green} // 右边还是幂函数乘指数函数, 继续使用分部积分} \\
& {\color{Green} // 令 x 作为 u, e^x 作为 v} \\
& = x^2 e^x - 2 \int x \mathrm{d}(e^x) \\
& = x^2 e^x - 2 (x e^x - \int e^x \mathrm{d}x) \\
& = x^2 e^x - 2 x e^x + 2 e^x \\
\end{align}
-->

![](../img/ii3_2.jpg)

使用场景 2: 幂函数乘对数函数

<!--

-->
