# 极限的性质

## 唯一性

对于任意极限, 如果存在, 那么它必唯一。

证明:

<!--
\begin{align}
& 设: \lim_{x \to a} f(x) = A, \lim_{x \to a} f(x) = B, \\
& 假如 A \gt B \\
& 取 \varepsilon = \frac{A - B}{2} \gt 0, (\varepsilon 可以取任意值, 只是这个值方便举反例) \\
& 由于 \lim_{x \to a} f(x) = A, 根据极限的定义, 存在 \delta_{1} \gt 0, \\
& 当 0 \lt |x - a| \lt \delta_{1} 时, |f(x) - A| \lt \frac{A - B}{2} \\
& 即 \frac{A + B}{2} \lt f(x) \lt \frac{3A - B}{2} \;\;\;\;\;\; (1) \\
\\
& 由于 \lim_{x \to a} f(x) = B, 根据极限的定义, 存在 \delta_{2} \gt 0, \\
& 当 0 \lt |x - a| \lt \delta_{2} 时, |f(x) - B| \lt \frac{A - B}{2} \\
& 即 \frac{3B - A}{2} \lt f(x) \lt \frac{A + B}{2} \;\;\;\;\;\; (2) \\
\\
& 取 \delta = \min \left \{ \delta_{1},\delta_{2} \right \}, 当 0 \lt |x - a| \lt \delta 时, (1)和(2) 理应都成立 \\
& 矛盾, 所以 A \gt B 不对 \\
& 同理, A \lt B 也不对 \\
& 所以 A = B \\
\end{align}
-->

![](../img/la1.jpg)
