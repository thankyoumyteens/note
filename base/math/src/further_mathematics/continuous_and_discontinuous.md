# 连续与间断

## 连续

函数在一点上连续

<!--
\begin{align}
& 函数 f(x) 在 x = a 的邻域内有定义, 若\lim_{x \to a} f(x) = f(a), 则函数 f(x) 在 x = a 处连续 \\
\\
& 1. 函数 f(x) 在 x = a 处连续的充要条件: \lim_{x \to a^{-}} f(x) = \lim_{x \to a^{+}} f(x) = f(a) \\
& 2. 初等函数在定义域内皆连续 \\
\end{align}
-->

![](../img/cad1.jpg)

函数在闭区间上连续

<!--
\begin{align}
& 函数 f(x) 在闭区间 [a, b] 内有定义, 若: \\
& \quad (1) \; f(x) 在 (a, b) 内每一个点都连续 \\
& \quad (2) \; \lim_{x \to a^{+}} f(x) = \lim_{x \to b^{-}} f(x) = f(a) \\
& 则函数 f(x) 在闭区间 [a, b] 内连续 \\
\end{align}
-->

![](../img/cad2.jpg)

## 间断

<!--
\begin{align}
& 函数 f(x) 在 x = a 的去心邻域内有定义, 若\lim_{x \to a} f(x) \ne f(a), \\
& 则函数 f(x) 在 x = a 处间断, a 点称为 f(x) 的间断点 \\
\end{align}
-->

![](../img/cad3.jpg)

间断点的分类

<!--
\begin{align}
& 函数 f(x) 在 x = a 处间断: \\
& \quad (1) \; 第一类间断点 \quad \lim_{x \to a^{-}} f(x) 和 \lim_{x \to a^{+}} f(x) 都存在 \\
& \quad \quad 1) \; 若 \lim_{x \to a^{-}} f(x) = \lim_{x \to a^{+}} f(x), 则 a 称为可去间断点 \\
& \quad \quad 2) \; 若 \lim_{x \to a^{-}} f(x) \ne \lim_{x \to a^{+}} f(x), 则 a 称为跳跃间断点 \\
\\
& \quad (2) \; 第二类间断点 \quad \lim_{x \to a^{-}} f(x) 和 \lim_{x \to a^{+}} f(x) 至少有一个不存在 \\
\end{align}
-->

![](../img/cad4.jpg)

例题 1

<!--
\begin{align}
& 设函数 f(x) = \begin{cases}
\frac{\sin ax + e^{2x} - 1}{x}, & x \lt 0 \\
4, & x = 0 \\
\frac{b\arctan x + \ln (1 - x)}{x}, & x \gt 0
\end{cases}, 在 x= 0 处连续, 求常数 a, b 的值 \\
\\
& \;\;\;\; \lim_{x \to 0^{-}} f(x) \\
& = \lim_{x \to 0^{-}} \frac{\sin ax}{x} + \lim_{x \to 0^{-}} \frac{e^{2x} - 1}{x} \\
& \;\;\;\; {\color{Green} // 等价无穷小替换} \\
& = \lim_{x \to 0^{-}} \frac{ax}{x} + \lim_{x \to 0^{-}} \frac{2x}{x} \\
& = a + 2 \\
\\
& \;\;\;\; f(0) = 0 \\
\\
& \;\;\;\; \lim_{x \to 0^{+}} f(x) \\
& = b \lim_{x \to 0^{+}} \frac{\arctan x}{x} + \lim_{x \to 0^{+}} \frac{\ln (1 - x)}{x} \\
& \;\;\;\; {\color{Green} // 等价无穷小替换} \\
& = b \lim_{x \to 0^{+}} \frac{x}{x} + \lim_{x \to 0^{+}} \frac{-x}{x} \\
& = b - 1 \\
\\
& 因为 f(x) 在 x= 0 处连续, 所以 \lim_{x \to 0^{-}} f(x) = \lim_{x \to 0^{+}} f(x) = f(0) \\
& \;\, a + 2 = b - 1 = 4 \\
& \;\, a = 2, b = 5 \\
\end{align}
-->

![](../img/cad5.jpg)

例题 2

<!--
\begin{align}
& 设 f(x) = \frac{x^{2} + x - 2}{x^{2} - 1} e^{\frac{1}{x}}, 求函数 f(x) 的间断点并分类 \\
\\
& \;\, x = -1, x = 0, x = 1 时 分母为0, 所以 -1, 0, 1 是间断点 \\
\\
& \lim_{x \to -1} f(x) 时, 分母趋于0, 分子趋于 -2, \lim_{x \to -1} e^{\frac{1}{x}} 是个正数 \\
& \lim_{x \to -1} f(x) = \infty, 极限不存在, -1 是第二类间断点 \\
\\
& \lim_{x \to 0} f(x) 时, e^{\frac{1}{0}} 不存在, 要分左右极限 \\
& \lim_{x \to 0^{-}} f(x) = 2\lim_{x \to 0^{-}} e^{\frac{1}{x}} = 0 \\
& \lim_{x \to 0^{+}} f(x) = 2\lim_{x \to 0^{+}} e^{\frac{1}{x}} = + \infty \\
& 所以 0 是第二类间断点 \\
\\
& \lim_{x \to 1} f(x) = \lim_{x \to 1} \frac{(x - 1)(x + 2)}{(x - 1)(x + 1)} e^{\frac{1}{x}} \\
& \qquad \quad \;\;\, = \lim_{x \to 1} \frac{x + 2}{x + 1} e^{\frac{1}{x}} \\
& \qquad \quad \;\;\, = \frac{3}{2} e \\
& 左右极限存在且相等, 1 是可去间断点 \\
\end{align}
-->

![](../img/cad6.jpg)

例题 3

<!--
\begin{align}
& 设 f(x) = \frac{\ln |x|}{x^{2} - 1}, 求 f(x) 的间断点 \\
\\
& 间断点是 -1, 0, 1 \\
\\
& \lim_{x \to -1} f(x) = \lim_{x \to -1} \frac{1}{x - 1} \times \frac{\ln -x}{x + 1} \\
& \qquad\qquad\; = - \frac{1}{2} \lim_{x \to -1} \frac{\ln -x}{x + 1} \\
& \qquad\qquad\; = - \frac{1}{2} \lim_{x \to -1} \frac{\ln [1 - (x + 1)]}{x + 1} \\
& \qquad\qquad\; = - \frac{1}{2} \lim_{x \to -1} \frac{- (x + 1)}{x + 1} \\
& \qquad\qquad\; = \frac{1}{2} \\
& 左右极限存在且相等, -1 是可去间断点 \\
\\
& \lim_{x \to 0} f(x), 分母趋于 -1, 分子: 由于 |x| 趋于0^{+}, 所以 ln|x| 趋于 - \infty \\
& 所以 \lim_{x \to 0} f(x) = + \infty \\
& 极限不存在, 0 是第二类间断点 \\
\\
& \lim_{x \to 1} f(x) = \lim_{x \to -1} \frac{1}{x + 1} \times \frac{\ln x}{x - 1} \\
& \qquad\qquad\; = \frac{1}{2} \lim_{x \to -1} \frac{\ln x}{x - 1} \\
& \qquad\qquad\; = \frac{1}{2} \lim_{x \to -1} \frac{\ln [1 + (x - 1)]}{x - 1} \\
& \qquad\qquad\; = \frac{1}{2} \lim_{x \to -1} \frac{x - 1}{x - 1} \\
& \qquad\qquad\; = \frac{1}{2} \\
& 左右极限存在且相等, 11 是可去间断点 \\
\end{align}
-->

![](../img/cad7.jpg)

## 闭区间上连续函数的性质

<!--
\begin{align}
& (1) 最小值与最大值定理: 设 f(x) 在 [a, b] 上连续, 则 f(x) 在 [a, b] 上可以取到最小值和最大值 \\
& (2) 有界定理: 设 f(x) 在 [a, b] 上连续, 则 f(x) 在 [a, b] 上有界 \\
& (3) 零点定理: 设 f(x) 在 [a, b] 上连续, 且 f(a) \cdot f(b) \lt 0, 则至少存在一点 c \in (a, b), 使 f(c) = 0 \\
& (4) 介值定理: 设 f(x) 在 [a, b] 上连续, f(x) 在 [a, b] 范围的最小值是 m, 最大值是 M, \\
& \qquad\qquad\quad 则, 任取 \eta \in [m, M], 都存在 \xi \in [a, b], 使 f(\xi) = \eta \\
& \qquad\qquad\quad\; f(x) 在 [m, M] 之间的任意一个值(比如 \eta)都称为介值 \\
\end{align}
-->

![](../img/cad8.jpg)

例题 1

<!--
\begin{align}
& 证明方程 x^{5} + 4x + 1 = 0 有且仅有一个正根 \\
\\
& 令 f(x) = x^{5} + 4x + 1, f(x) 处处连续 \\
& 取一个好算的范围 [0, 1], 则 f(0) = -1, f(1) = 4, f(0) \cdot f(1) = -4 \lt 0 \\
& 根据零点定理, 存在 c \in (a, b), 使 f(c) = 0 \\
& 所以 c 是方程的1个解, 且 c 为正数 \\
\\
& 求导 f'(x) = 5x^{4} + 4 > 0, 所以 f(x) 在 [0, + \infty]单调递增 \\
& 所以方程的解唯一 \\
\end{align}
-->

![](../img/cad9.jpg)

例题 2

<!--
\begin{align}
& 设 f(x) 在 [0, 2] 上连续, f(0) + 2 \cdot f(1) + 3 \cdot f(2) = 6, 证明: 存在 \xi \in [0, 2], 使 f(\xi) = 1 \\
& {\color{Green} // 闭区间连续, 函数值相加 \Rightarrow 使用介值定理} \\
& 因为  f(x) 在 [0, 2] 上连续, 所以存在最大值 M 和最小值 m \\
& 因为 6 \cdot m \le f(0) + 2 \cdot f(1) + 3 \cdot f(2) \le 6 \cdot M \\
& 所以 6 \cdot m \le 6 \le 6 \cdot M \Rightarrow m \le 1 \le M \\
& 根据介值定理, 一定存在 \xi \in [0, 2], 使 f(\xi) = 1 \\
\end{align}
-->

![](../img/cad10.jpg)
