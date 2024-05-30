# 极限存在准则

## 极限存在定理

### 夹逼定理(数列型)

<!--
\begin{align}
& 三个数列 a_{n}, b_{n}, c_{n}, 且 a_{n} \le b_{n} \le c_{n} \\
& 如果 \lim_{x \to \infty} a_{n} = \lim_{x \to \infty} c_{n} = A, 则: \lim_{x \to \infty} b_{n} = A \\
\end{align}
-->

![](../img/lec1.jpg)

证明

<!--
\begin{align}
& 因为 \lim_{x \to \infty} a_{n} = A, 所以, 对任意的 \varepsilon \gt 0 \\
& 存在 N_{1} \gt 0, 当 n \gt N_{1} 时, |a_{n} - A| \lt \varepsilon, \\
& 即 A - \varepsilon \lt a_{n} \lt A + \varepsilon \qquad (1)\\
& 因为 \lim_{x \to \infty} c_{n} = A, 所以, 对任意的 \varepsilon \gt 0 \\
& 存在 N_{2} \gt 0, 当 n \gt N_{2} 时, |c_{n} - A| \lt \varepsilon, \\
& 即 A - \varepsilon \lt c_{n} \lt A + \varepsilon \qquad (2)\\
& 取 N = max\left \{ N_{1}, N_{2} \right \} , 当 n \gt N 时, (1) 和 (2) 都成立, \\
& 而已知 a_{n} \le b_{n} \le c_{n}, 则 A - \varepsilon \lt a_{n} \le b_{n} \le c_{n} \lt A + \varepsilon \\
& 所以 A - \varepsilon \lt b_{n} \lt A + \varepsilon, 即 |b_{n} - A| \lt \varepsilon \\
& 所以 \lim_{x \to \infty} b_{n} = A \\
\end{align}
-->

![](../img/lec2.jpg)

### 夹逼定理(函数型)

<!--
\begin{align}
& 三个函数 f(x), g(x), h(x) 在 x = a 的去心邻域内满足 f(x) \le g(x) \le h(x) \\
& 如果 \lim_{x \to a} f(x) = \lim_{x \to a} h(x) = A, 则 \lim_{x \to a} g(x) = A \\
\end{align}
-->

![](../img/lec3.jpg)

证明

<!--
\begin{align}
& 因为 \lim_{x \to a} f(x) = A, 所以, 对任意的 \varepsilon \gt 0 \\
& 存在 \delta_{1} \gt 0, 当 0 \lt |x - a| \lt \delta_{1} 时, |f(x) - A| \lt \varepsilon, \\
& 即 A - \varepsilon \lt f(x) \lt A + \varepsilon \qquad (1)\\
& 因为 \lim_{x \to a} h(x) = A, 所以, 对任意的 \varepsilon \gt 0 \\
& 存在 \delta_{2} \gt 0, 当 0 \lt |x - a| \lt \delta_{2} 时, |h(x) - A| \lt \varepsilon, \\
& 即 A - \varepsilon \lt h(x) \lt A + \varepsilon \qquad (2)\\
& 取 \delta = min\left \{ \delta_{1}, \delta_{2} \right \} , 当 0 \lt |x - a| \lt \delta 时, (1) 和 (2) 都成立, \\
& 而已知 f(x) \le g(x) \le h(x), 则 A - \varepsilon \lt f(x) \le g(x) \le h(x) \lt A + \varepsilon \\
& 所以 A - \varepsilon \lt g(x) \lt A + \varepsilon, 即 |g(x) - A| \lt \varepsilon \\
& 所以 \lim_{x \to a} g(x) = A \\
\end{align}
-->

![](../img/lec4.jpg)
