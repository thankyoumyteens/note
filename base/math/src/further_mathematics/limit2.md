# 函数的极限

## x 接近某一个点时的极限

<!--
\begin{align}
& 函数 f(x) 的 x 在 a 的去心邻域内有定义, \\
& 如果对于任意给定的正数 \varepsilon (要多小有多小), 都存在一个 \delta , \\
& 使得当 0 \lt |x - a| \lt \delta 时, |f(x) - A| \lt \varepsilon \\
& 则函数 f(x) 以 A 为极限, 记作: \lim_{x \to a} f(x) = A \\
& 即: 当 x 无限接近 a 时, f(x) 无限接近 A \\
\end{align}
-->

![](../img/lim3.jpg)

例题:

<!--
\begin{align}
& 已知 f(x) = \frac{x^{2} + x - 2}{x^{2} - 1}, 求 \lim_{x \to 1} f(x) \\
& \lim_{x \to 1} f(x) = \lim_{x \to 1} \frac{x^{2} + x - 2}{x^{2} - 1} \\
& \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, = \lim_{x \to 1} \frac{(x - 1)(x + 2)}{(x - 1)(x + 1)} \\
& 当x无限趋近于1时, x - 1无限小, 可以忽略不计 \\
& \therefore \lim_{x \to 1} f(x) = \lim_{x \to 1} \frac{x + 2}{x + 1} \\
& 把1带入x \Rightarrow  \lim_{x \to 1} f(x) = \frac{3}{2} \\
\end{align}
-->

![](../img/lim4.jpg)

## x 接近无穷时的极限

<!--
\begin{align}
& 如果对于任意给定的正数 \varepsilon (要多小有多小), 都存在一个 X \gt 0 , \\
& 当 x \gt X 时, 有 |f(x) - A| \lt \varepsilon \\
& 则函数 f(x) 在 x \to +\infty 时以 A 为极限, 记作: \lim_{x \to +\infty} f(x) = A \\
\\
& 如果对于任意给定的正数 \varepsilon (要多小有多小), 都存在一个 X \gt 0 , \\
& 当 x \lt -X 时, 有 |f(x) - A| \lt \varepsilon \\
& 则函数 f(x) 在 x \to -\infty 时以 A 为极限, 记作: \lim_{x \to -\infty} f(x) = A \\
\\
& 如果对于任意给定的正数 \varepsilon (要多小有多小), 都存在一个 X \gt 0 , \\
& 当 |x| \gt X 时, 有 |f(x) - A| \lt \varepsilon \\
& 则函数 f(x) 在 x \to \infty 时以 A 为极限, 记作: \lim_{x \to \infty} f(x) = A \\
\end{align}
-->

![](../img/lim9.jpg)
