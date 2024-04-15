# 极限

## 数列的极限

如果一个数列的项越来越接近某个特定的值，那么这个值就被称为该数列的极限。

<!--
\begin{align}
& 有一个数列 \left \{ a_{n} \right \}, 其中a_{n} 表示数列的第n项 \\
& 如果对于任意给定的正数 \varepsilon (无论多小), 都存在一个正整数 N, \\
& 使得当 n \gt N 时, |a_{n} - A| \lt \varepsilon \\
& 则数列 \left \{ a_{n} \right \} 以 A 为极限, 记作: \lim_{n \to \infty} a_{n} = A \\
& 这个定义说明了数列的项a_{n}可以无限接近A，但并不要求a_{n}必须等于A \\
\end{align}
-->

![](../img/lim1.jpg)

<!--
\begin{align}
& 已知数列 \left \{ a_{n} \right \} 的极限为A, 证明: 数列 \left \{ |a_{n}| \right \} 的极限为 |A|, 反之不一定成立 \\
&\because \lim_{x \to \infty} a_{n} = A \\
& \therefore 根据极限的定义: \forall \varepsilon  \gt 0, 总 \exists N \gt 0, \\
& \;\;\, 使得, 当 n \gt N 时, |a_{n} - A| \lt \varepsilon \\
& 根据三角不等式: ||a_{n}| - |A|| \le |a_{n} - A| \\
& \therefore \forall \varepsilon  \gt 0, 总 \exists N \gt 0, \\
& \;\;\, 使得, 当 n \gt N 时, ||a_{n}| - |A|| \lt \varepsilon \\
& \therefore \lim_{x \to \infty} |a_{n}| = |A| \\
\\
& 假设 a_{n} = (-1)^{n}, 则 \lim_{x \to \infty} a_{n} 不存在, 但是 \lim_{x \to \infty} |a_{n}| = 1 \\
& \therefore 反之不成立 \\
\end{align}
-->

![](../img/lim2.jpg)
