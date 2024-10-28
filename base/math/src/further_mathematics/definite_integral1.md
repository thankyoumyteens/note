# 定积分基本定理与特殊性质

<!--
\begin{align}
& 不定积分 \int f(x) \mathrm{d}x \ne \int f(t) \mathrm{d}t \ne \int f(u) \mathrm{d}u \\
& 而定积分由积分的上下限和函数关系决定，与积分变量无关，\\
& 即 \int_{a}^{b} f(x) \mathrm{d}x = \int_{a}^{b} f(t) \mathrm{d}t = \int_{a}^{b} f(u) \mathrm{d}u \\
\\
& 定积分 \int_{a}^{x} f(x) \mathrm{d}x 在表达式中的 x 和积分上限 x 不同, \\
& 这个定积分也可以写成 \int_{a}^{x} f(t) \mathrm{d}t, \\
& 之所以积分上限也用 x 表示, 是因为这个定积分的积分上限也是变化的, \\
& 即 \varphi (x) = \int_{a}^{x} f(t) \mathrm{d}t 也是一个函数, 称为积分上限函数 \\
\\
& 定积分 \int_{a}^{x} f(x, t) \mathrm{d}t 在表达式中的 x 和积分上限 x 相同, \\
& 因为积分变量是 t, 而不是 x \\
\end{align}
-->

![](../img/di1_1.jpg)

## 定积分基本定理

<!--
\begin{align}
& 设函数 f(x) 在 [a, b] 上连续, 它的积分上限函数 \Phi (x) = \int_{a}^{x} f(t) \mathrm{d}t, \\
& 则 \Phi '(x) = \frac{\mathrm{d} }{\mathrm{d} x} \Phi (x) = f(x) \\
\end{align}
-->

![](../img/di1_2.jpg)

证明

<!--
\begin{align}
& \Delta \Phi (x) = \Phi (x + \Delta x) - \Phi (x) \\
& = \int_{a}^{x + \Delta x} f(t) \mathrm{d}t - \int_{a}^{x} f(t) \mathrm{d}t \\
& = \int_{a}^{x} f(t) \mathrm{d}t + \int_{x}^{x + \Delta x} f(t) \mathrm{d}t - \int_{a}^{x} f(t) \mathrm{d}t \\
& = \int_{x}^{x + \Delta x} f(t) \mathrm{d}t \\
& 因为 f(x) 在 [a, b] 上连续, 根据积分中值定理 \\
& 存在 \xi \in [x, x + \Delta x] \subset [a, b], \\
& 使 \int_{x}^{x + \Delta x} f(t) \mathrm{d}t = f(\xi)\Delta x \\
& 把 \Delta x 移到左边: \frac{\Delta \Phi (x)}{\Delta x}  = f(\xi) \\
& 两边取极限 \lim_{\Delta x \to 0} \frac{\Delta \Phi (x)}{\Delta x} = \lim_{\Delta x \to 0} f(\xi) \\
& 因为 \xi \in [x, x + \Delta x], 所以当 \Delta x \to 0 时, \xi \to x \\
& 所以 \lim_{\Delta x \to 0} \frac{\Delta \Phi (x)}{\Delta x} = \lim_{\xi \to x} f(\xi) \\
& 因为 f(x) 在 [a, b] 上连续, \\
& 所以极限值等于函数值: \lim_{\xi \to x} f(\xi) = f(x) \\
& 所以 \lim_{\Delta x \to 0} \frac{\Delta \Phi (x)}{\Delta x} = f(x) \\
& 根据导数的定义: \Phi '(x) = \frac{\mathrm{d} }{\mathrm{d} x} \Phi (x) = f(x) \\
\end{align}
-->

![](../img/di1_3.jpg)

<!--
\begin{align}
& 1、若 f(x) 在 [a, b] 上连续, 则 f(x) 一定存在原函数 \\
& 2、\Phi (x) = \int_{a}^{x} f(t) \mathrm{d}t 就是 f(x) 的一个原函数 \\
& 3、\frac{\mathrm{d}}{\mathrm{d} x} \int_{a}^{\Phi (x)} f(t) \mathrm{d}t
= f[\Phi (x)] \Phi '(x) \\
\end{align}
-->

![](../img/di1_4.jpg)

例题 1

<!--
\begin{align}
& \;\;\;\; \lim_{x \to 0} \frac{\int_{0}^{x} e^{-t^2} \mathrm{d}t - x}{x^3} \\
& {\color{Green} // 被积函数和 x 无关, 用洛必达法则对 x 求导} \\
& = \lim_{x \to 0} \frac{(\int_{0}^{x} e^{-t^2} \mathrm{d}t - x)'}{3x^2} \\
& {\color{Green} // \frac{\mathrm{d}}{\mathrm{d} x} \int_{a}^{\Phi (x)} f(t) \mathrm{d}t
= f[\Phi (x)] \Phi '(x)} \\
& = \lim_{x \to 0} \frac{ e^{-x^2} - 1}{3x^2} \\
& = \frac{1}{3} \lim_{x \to 0} \frac{ e^{-x^2} - 1}{x^2} \\
& {\color{Green} // 继续用洛必达法则} \\
& = \frac{1}{3} \lim_{x \to 0} \frac{ -2x e^{-x^2}}{2x} \\
& = - \frac{1}{3} \lim_{x \to 0} e^{-x^2} \\
& = - \frac{1}{3} \\
\end{align}
-->

![](../img/di1_5.jpg)

例题 2

<!--
\begin{align}
& \;\;\;\; f(x) 连续, f(0) = 0, f'(0) = \pi,
求 \lim_{x \to 0} \frac{\int_{0}^{x} f(t) \mathrm{d}t}{x - \ln(1 + x)} \\
& {\color{Green} // 麦克劳林公式 \ln(1 + x) = x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - ... + o(x^{n})} \\
& {\color{Green} // 用一个 x 把分母的 x 消掉, 再多加一个 - \frac{x^{2}}{2} 就不需要继续写了} \\
& {\color{Green} // 写成: \ln(1 + x) = x - \frac{x^{2}}{2} + o(x^2)} \\
& {\color{Green} // 分母等价于: x - \ln(1 + x) = \frac{x^{2}}{2} + o(x^2)} \\
& = \lim_{x \to 0} \frac{\int_{0}^{x} f(t) \mathrm{d}t}{\frac{x^{2}}{2} + o(x^2)} \\
& {\color{Green} // 由于是求极限, 所以可以去掉高阶无穷小} \\
& = \lim_{x \to 0} \frac{\int_{0}^{x} f(t) \mathrm{d}t}{\frac{x^{2}}{2}} \\
& {\color{Green} // 被积函数和 x 无关, 用洛必达法则对 x 求导} \\
& = \lim_{x \to 0} \frac{(\int_{0}^{x} f(t) \mathrm{d}t)'}{x} \\
& {\color{Green} // \frac{\mathrm{d}}{\mathrm{d} x} \int_{a}^{\Phi (x)} f(t) \mathrm{d}t
= f[\Phi (x)] \Phi '(x)} \\
& = \lim_{x \to 0} \frac{f(x)}{x} \\
& {\color{Green} // 用导数的定义} \\
& = \lim_{x \to 0} \frac{f(x) - f(0)}{x - 0} = f'(0) = \pi \\
\end{align}
-->

![](../img/di1_6.jpg)

例题 3

<!--
\begin{align}
& \;\;\;\; 设函数 f(x) 连续, \varphi (x) = \int_{0}^{x} (x - t)f(t) \mathrm{d}t, 求 \varphi ''(x) \\
\end{align}
-->
