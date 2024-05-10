# 无穷小与无穷大

## 无穷小

<!--
\begin{align}
& f(x) 在 x = a 的去心邻域内有定义, \\
& 如果 \lim_{x \to a} f(x) = 0, 则称: \\
& f(x) 在 x \to a 时为无穷小。 \\
\end{align}
-->

![](../img/i1.jpg)

<!--
\begin{align}
& (1) & 0是无穷小, 是唯一的一个与自变量趋向无关的无穷小 \\
& (2) & 一个非0的函数是不是无穷小, 与自变量的趋向有关, \\
& & 比如 f(x) = \left ( x - 1 \right ) ^{2}, 只有当 x \to 1 时才是无穷小 \\
\end{align}
-->

![](../img/i2.jpg)

## 无穷小的比较

<!--
\begin{align}
& 当 x \to x_{0} 时, \alpha (x) \to 0, \beta (x) \to 0 \\
& \; (1) \;\;\;\; 若 \lim_{x \to x_{0}} \frac{\beta (x)}{\alpha (x)} = 0,
即 \beta (x) 靠近 0 的速度比 \alpha (x) 更快, 则称 \beta (x) 为 \alpha (x) 的高阶无穷小,
记为 \beta (x) = o \left ( \alpha (x) \right )  \\
& \; (2) \;\;\;\; 若 \lim_{x \to x_{0}} \frac{\beta (x)}{\alpha (x)} = k \ne 0 \ne \infty,
即 \beta (x) 和 \alpha (x) 是倍数关系, 则称 \beta (x) 为 \alpha (x) 的同阶无穷小,
记为 \beta (x) = O \left ( \alpha (x) \right )  \\
& \; (3) \;\;\;\; 若 \lim_{x \to x_{0}} \frac{\beta (x)}{\alpha (x)} = 1,
则称 \beta (x) 和 \alpha (x) 为等价无穷小(一种特殊的同阶无穷小) \\
\end{align}
-->

![](../img/i3.jpg)

## 无穷大

<!--
\begin{align}
& f(x) 在 x = a 的去心邻域内有定义, \\
& 如果对任意(要多大有多大)的 M \gt 0, \\
& 当 0 \lt | x - a| \lt \delta 时, |f(x)| \ge M \\
& 则称: f(x) 在 x \to a 时为无穷大。 \\
\\
& 另一种表示方法: 如果 \lim_{x \to a} \frac{1}{f(x)} = 0 \\
& 则称: f(x) 在 x \to a 时为无穷大, 即无穷小的倒数。 \\
\end{align}
-->

![](../img/i4.jpg)

1. 两个无穷大之积仍为无穷大
2. 两个无界函数/数列之积不一定是无界函数/数列, 比如: 两个无界数列 `1, 0, 3, 0, 5, ...` 和 `0, 2, 0, 4, 0, ...` 的积是有界的

## 无穷小的一般性质
