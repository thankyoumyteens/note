# 一阶微分方程

## 可分离变量的微分方程

<!--
\begin{align}
& 对一阶微分方程 \frac{\mathrm{d}y}{\mathrm{d}x} = f(x, y), \\
& 若 f(x, y) = \varphi _1(x) \varphi _2(y), 且 \varphi _2(y) \ne 0, \\
& 则称 \frac{\mathrm{d}y}{\mathrm{d}x} = f(x, y) 为可分离变量的微分方程 \\
\\
& 解法: 将 \frac{\mathrm{d}y}{\mathrm{d}x} = f(x, y) 化为 \frac{\mathrm{d}y}{\mathrm{d}x} = \varphi _1(x) \varphi _2(y), \\
& 把变量分离得到 \frac{\mathrm{d}y}{\varphi _2(y)} = \varphi _1(x) \mathrm{d}x \\
& 两边同时积分得到 \int \frac{\mathrm{d}y}{\varphi _2(y)} = \int \varphi _1(x) \mathrm{d}x + C \\
\end{align}
-->

![](../img/de2_1.jpg)

例题 1

<!--
\begin{align}
& 求微分方程 \frac{\mathrm{d}y}{\mathrm{d}x} = 2x(1 + y^2) 的通解 \\
\\
& \frac{\mathrm{d}y}{1 + y^2} = 2x \mathrm{d}x\\
& \int \frac{\mathrm{d}y}{1 + y^2} = \int 2x \mathrm{d}x + C \\
& \arctan y = x^2 + C \\
& y = \tan (x^2 + C) \\
\end{align}
-->

![](../img/de2_2.jpg)

例题 2

<!--
\begin{align}
& 求微分方程 \frac{\mathrm{d}y}{\mathrm{d}x} = 2xy 的通解 \\
\\
& 情况1: y = 0 \\
& y = 0 是方程的解 \\
\\
& 情况2: y \ne 0 \\
& \frac{\mathrm{d}y}{y} = 2x \mathrm{d}x\\
& \int \frac{\mathrm{d}y}{y} = \int 2x \mathrm{d}x + C_0 \\
& \ln |y| = x^2 + C_0 \\
& {\color{Green} // 对等式两边同时取 e 的幂} \\
& e^{\ln |y|} = e^{x^2 + C_0} \\
& {\color{Green} // e^{\ln a} = a} \\
& |y| = e^{x^2 + C_0} \\
& y = \pm e^{x^2 + C_0} \\
& y = \pm e^{C_0}e^{x^2} \\
& 令 \pm e^{C_0} = C \\
& {\color{Green} // C_0 \in (- \infty, + \infty), 所以 e^{C_0} \in (0, + \infty)} \\
& {\color{Green} // 所以 \pm e^{C_0} \in (- \infty, 0) \cup (0, + \infty)} \\
& y = Ce^{x^2} \quad (C \ne 0) \\
& 所以通解为 两种情况合到一起:  y = Ce^{x^2} \quad (C为任意常数)\\
\end{align}
-->

![](../img/de2_3.jpg)

## 齐次微分方程

<!--
\begin{align}
& 对一阶微分方程 \frac{\mathrm{d}y}{\mathrm{d}x} = f(x, y), \\
& 若 f(x, y) = \varphi (\frac{y}{x}), \\
& 则称 \frac{\mathrm{d}y}{\mathrm{d}x} = f(x, y) 为齐次微分方程 \\
\\
& 解法: 将 \frac{\mathrm{d}y}{\mathrm{d}x} = f(x, y) 化为 \frac{\mathrm{d}y}{\mathrm{d}x} = \varphi (\frac{y}{x}), \\
& 令 u = \frac{y}{x}, 则 y = ux, 则 \frac{\mathrm{d}y}{\mathrm{d}x} = (xu)' = u + x \frac{\mathrm{d}u}{\mathrm{d}x} \\
& 代入得到 x \frac{\mathrm{d}u}{\mathrm{d}x} = \varphi (u) - u, \\
& 变量分离后积分得到 \int \frac{\mathrm{d}u}{\varphi (u) - u} = \int \frac{\mathrm{d}x}{x} + C, \\
& 再将 u = \frac{y}{x} 代入即可得到原方程的通解 \\
\end{align}
-->

![](../img/de2_4.jpg)

例题 1

<!--
\begin{align}
& 求微分方程 \frac{\mathrm{d}y}{\mathrm{d}x} - \frac{2}{x}y = 1 的通解 \\
\\
& \frac{\mathrm{d}y}{\mathrm{d}x} = 2 \frac{y}{x} + 1 \\
& 令 u = \frac{y}{x}, \frac{\mathrm{d}y}{\mathrm{d}x} = u + x \frac{\mathrm{d}u}{\mathrm{d}x} \\
& 代入 u + x \frac{\mathrm{d}u}{\mathrm{d}x} = 2 u + 1 \\
& 整理得到 \frac{\mathrm{d}u}{u + 1} = \frac{\mathrm{d}x}{x} \\
& 两边积分 \int \frac{\mathrm{d}u}{u + 1} = \int \frac{\mathrm{d}x}{x} + C \\
& {\color{Green} // 上面的例题2已经讨论过了, \ln 的绝对值可以去掉} \\
& \ln (u + 1) = \ln x + \ln C \\
& \ln (u + 1) = \ln Cx \\
& u + 1 = Cx \\
& \frac{y}{x} + 1 = Cx \\
& y = Cx^2 - x \quad (C为任意常数)\\
\end{align}
-->

![](../img/de2_5.jpg)

## 一阶齐次线性微分方程

<!--
\begin{align}
& 形如 \frac{\mathrm{d}y}{\mathrm{d}x} + P(x)y = 0 的微分方程, 称为一阶齐次线性微分方程 \\
\\
& 解法: 将 \frac{\mathrm{d}y}{\mathrm{d}x} + P(x)y = 0 化为 \frac{\mathrm{d}y}{\mathrm{d}x} = - P(x)y, \\
& 令显然 y = 0 为微分方程的一个解 \\
& 当 y \ne 0 时, 原方程化为: \frac{\mathrm{d}y}{y} = - P(x) \mathrm{d}x \\
& 等号两边积分: \int \frac{\mathrm{d}y}{y} = - \int P(x) \mathrm{d}x + C_0
\Rightarrow y = \pm e^{C_0} e^{- \int P(x) \mathrm{d}x} \\
& 令 \pm e^{C_0}, 则 y = C e^{- \int P(x) \mathrm{d}x} \quad (C \ne 0) \\
& 所以通解为: y = C e^{- \int P(x) \mathrm{d}x} \quad (C 为任意常数) \\
\end{align}
-->

![](../img/de2_6.jpg)

例题 1

<!--
\begin{align}
& 求微分方程 y' + 2xy = 0 的通解 \\
\\
& \frac{\mathrm{d}y}{\mathrm{d}x} + 2xy = 0 \\
& 是一阶齐次线性微分方程, 直接代公式:  \\
& y = C e^{- \int P(x) \mathrm{d}x} \quad (C 为任意常数) \\
& y = C e^{- \int 2x \mathrm{d}x} \quad (C 为任意常数) \\
& y = C e^{- x^2} \quad (C 为任意常数) \\
\end{align}
-->

![](../img/de2_7.jpg)

## 一阶非齐次线性微分方程

<!--
\begin{align}
& 形如 \frac{\mathrm{d}y}{\mathrm{d}x} + P(x)y = Q(x) \quad (Q(x) \ne 0) 为一阶非齐次线性微分方程 \\
\\
& 解法: 公式为 y = \left [ \int Q(x) e^{\int P(x) \mathrm{d}x} \mathrm{d}x + C \right ] e^{- \int P(x) \mathrm{d}x} \quad (C 为任意常数) \\
\end{align}
-->

![](../img/de2_8.jpg)

例题 1

<!--
\begin{align}
& 求微分方程 \frac{\mathrm{d}y}{\mathrm{d}x} - \frac{2}{x} y = -1 的通解 \\
\\
& 是一阶非齐次线性微分方程, P(x) = - \frac{2}{x} , Q(x) = -1, 直接代公式:  \\
& y = \left [ \int Q(x) e^{\int P(x) \mathrm{d}x} \mathrm{d}x + C \right ] e^{- \int P(x) \mathrm{d}x} \quad (C 为任意常数) \\
& y = \left [ \int (-1) e^{- \int \frac{2}{x} \mathrm{d}x} \mathrm{d}x + C \right ] e^{\int \frac{2}{x} \mathrm{d}x} \quad (C 为任意常数) \\
& y = \left [ \int (-1) e^{- \int \frac{2}{x} \mathrm{d}x} \mathrm{d}x + C \right ] e^{2 \ln x} \quad (C 为任意常数) \\
& y = \left [ \int (-1) e^{- \int \frac{2}{x} \mathrm{d}x} \mathrm{d}x + C \right ] e^{\ln x^2} \quad (C 为任意常数) \\
& y = \left [ \int (-1) e^{- \int \frac{2}{x} \mathrm{d}x} \mathrm{d}x + C \right ] x^2 \quad (C 为任意常数) \\
& y = \left [ \int (-1) (- \frac{1}{x^2}) \mathrm{d}x + C \right ] x^2 \quad (C 为任意常数) \\
& y = (\int \frac{1}{x^2} \mathrm{d}x + C) x^2 \quad (C 为任意常数) \\
& y = (\frac{1}{x} + C) x^2 \quad (C 为任意常数) \\
& y = C x^2 + x \quad (C 为任意常数) \\
\end{align}
-->

![](../img/de2_9.jpg)

## 可降阶的高阶微分方程

<!--
\begin{align}
& y^{(n)} = f(x) \quad (n \ge 2) 型微分方程 \\
\\
& 解法: 将 y^{(n)} = f(x) 进行 n 次不定积分, \\
& 即可得到该微分方程的通解 \\
\end{align}
-->

![](../img/de2_10.jpg)

例题 1

<!--
\begin{align}
& 设 y'' = x e^{2x}, 求该方程的通解 \\
\\
& y' = \int x e^{2x} \mathrm{d}x + C_1 \\
& \;\;\, = \frac{1}{2} \int x \mathrm{d}(e^{2x}) + C_1 \\
& \;\;\, = \frac{1}{2} x e^{2x} - \frac{1}{2} \int e^{2x} \mathrm{d}x + C_1 \\
& \;\;\, = \frac{1}{2} x e^{2x} - \frac{1}{4} e^{2x} + C_1 \\
& y = \int (\frac{1}{2} x e^{2x} - \frac{1}{4} e^{2x} + C_1) \mathrm{d}x + C_2 \\
& \;\;\, = \frac{1}{2} \int x e^{2x} \mathrm{d}x -
\frac{1}{4} \int e^{2x} \mathrm{d}x +
\frac{1}{2} \int C_1 \mathrm{d}x + C_2 \\
& \;\;\, = \frac{1}{2} \int x e^{2x} \mathrm{d}x -
\frac{1}{4} \int e^{2x} \mathrm{d}x +
\frac{1}{2} C_1x + C_2 \\
& \;\;\, = \frac{1}{2} \int x e^{2x} \mathrm{d}x - \frac{1}{8} e^{2x} + C_1x + C_2 \\
& \;\;\, = \frac{1}{2} (\frac{1}{2} x e^{2x} - \frac{1}{4} e^{2x}) -
\frac{1}{8} e^{2x} + C_1x + C_2 \\
& \;\;\, = \frac{1}{4} x e^{2x} - \frac{1}{8} e^{2x} -
\frac{1}{8} e^{2x} + C_1x + C_2 \\
& \;\;\, = \frac{1}{4} x e^{2x} - \frac{1}{4} e^{2x} + C_1x + C_2 \\
\end{align}
-->

![](../img/de2_11.jpg)

<!--
\begin{align}
& f(x, y', y'') = 0 缺 y 型微分方程 \\
\\
& 解法: 令 y' = p, 则 y'' = \frac{\mathrm{d} p}{\mathrm{d} x}, \\
& 代入得 f(x, p, \frac{\mathrm{d} p}{\mathrm{d} x}) = 0 \\
& 解出 p = \varphi (x, C_1), 即 y' = \varphi (x, C_1) \\
& 则 y = \int y' \mathrm{d} x + C_2 = \int \varphi (x, C_1) \mathrm{d} x + C_2 \\
\end{align}
-->

![](../img/de2_12.jpg)

例题 1

<!--
\begin{align}
& 设 y'' + y' = 2 e^x, 求该方程的通解 \\
\\
& 令 y' = p, 则 y'' = \frac{\mathrm{d} p}{\mathrm{d} x} \\
& \; \frac{\mathrm{d} p}{\mathrm{d} x} + p = 2 e^x \\
& 变成了一阶非齐次线性微分方程 P(x) = 1, Q(x) = 2 e^x \\
& \; p = \left [ \int 2 e^x e^{\int 1 \mathrm{d}x} \mathrm{d}x + C_1 \right ] e^{- \int 1 \mathrm{d}x} \\
& \; p = \left [ \int 2 e^x e^{x} \mathrm{d}x + C_1 \right ] e^{- x} \\
& \; p = ( \int 2 e^{2x} \mathrm{d}x + C_1 ) e^{- x} \\
& \; p = ( 2 \times \frac{1}{2} e^{2x} + C_1 ) e^{- x} \\
& \; p = ( e^{2x} + C_1 ) e^{- x} \\
& \; p = C_1 e^{- x} + e^x \\
& \; y' = C_1 e^{- x} + e^x \\
& \; y = \int (C_1 e^{- x} + e^x) \mathrm{d}x + C_2 \\
& \; y = \int (C_1 e^{- x} + e^x) \mathrm{d}x + C_2 \\
& \; y = - C_1 e^{- x} + e^x + C_2 \\
\end{align}
-->

![](../img/de2_13.jpg)

<!--
\begin{align}
& f(y, y', y'') = 0 缺 x 型微分方程 \\
\\
& 解法: 令 y' = p, 则 y'' = \frac{\mathrm{d} p}{\mathrm{d} x} =
\frac{\mathrm{d} y}{\mathrm{d} x} \frac{\mathrm{d} p}{\mathrm{d} y} =
p \frac{\mathrm{d} p}{\mathrm{d} y}, \\
& 代入得 f(y, p, p \frac{\mathrm{d} p}{\mathrm{d} y}) = 0 \\
& 解出 p = \varphi (y, C_1), 即 y' = \frac{\mathrm{d} y}{\mathrm{d} x} = \varphi (y, C_1) \\
& 变量分离得 \frac{\mathrm{d} y}{\varphi (y, C_1)} = \mathrm{d} x \\
& 两边积分得 \int \frac{\mathrm{d} y}{\varphi (y, C_1)} = x + C_2 \\
\end{align}
-->

![](../img/de2_14.jpg)

例题 1

<!--
\begin{align}
& 求微分方程 y y'' - y'^2 = 0 满足初值条件 y(0) = y'(0) = 1 的特解 \\
\\
& 令 y' = p, 则 y'' = p \frac{\mathrm{d} p}{\mathrm{d} y} \\
& \; y p \frac{\mathrm{d} p}{\mathrm{d} y} - p^2 = 0 \\
& 因为 y'(0) = 1, 所以 p \ne 0 \\
& \; \frac{1}{p} (y p \frac{\mathrm{d} p}{\mathrm{d} y} - p^2) = \frac{1}{p} \times 0 \\
& \; y \frac{\mathrm{d} p}{\mathrm{d} y} - p = 0 \\
& 因为 y(0) = 1, 所以 y \ne 0 \\
& \; \frac{\mathrm{d} p}{\mathrm{d} y} - \frac{1}{y} p = 0 \\
& 变成了一阶齐次线性微分方程 P(x) = - \frac{1}{y} \\
& \; p = C_1 e^{- \int (- \frac{1}{y}) \mathrm{d}x} \\
& \; p = C_1 e^{\int \frac{1}{y} \mathrm{d}x} \\
& \; p = C_1 e^{\ln |y|} \\
& 因为 y(0) = 1, 所以 y \ne 0 \\
& \; p = C_1 e^{\ln y} \\
& \; p = C_1 y \\
& \; y' = C_1 y \\
& 因为 y(0) = y'(0) = 1, 所以 C_1 = 1 \\
& 所以 y' - y = 0 \\
& \; \frac{\mathrm{d} y}{\mathrm{d} x} - y = 0 \\
& 也是一阶齐次线性微分方程 \\
& \; y = C_2 e^{- \int (-1) \mathrm{d}x} \\
& \; y = C_2 e^x \\
& 因为 y(0) = C_2 e^0 = 1, 所以 C_2 = 1 \\
& 所以 y = e^x \\
\end{align}
-->

![](../img/de2_15.jpg)
