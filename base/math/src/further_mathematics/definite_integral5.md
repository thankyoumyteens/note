# 反常积分

<!--
\begin{align}
& 正常积分: \\
& \quad 1、积分区间有限 \\
& \quad 2、f(x) 在积分区间上连续或者存在有限个第一类间断点 \\
\end{align}
-->

![](../img/di5_1.jpg)

## 区间无限的反常积分

### 积分区间右侧无限的反常积分

<!--
\begin{align}
& 设函数 f(x) 在 [a, + \infty ) 上连续, 对任意一个大于 a 的 b, \\
& 有 \int_{a}^{b} f(x) \mathrm{d}x = F(b) - F(a), \\
& 如果极限 \lim_{b \to + \infty} [F(b) - F(a)] = A, \\
& 则称反常积分 \int_{a}^{+ \infty} f(x) \mathrm{d}x 收敛于常数 A, \\
& 记为 \int_{a}^{+ \infty} f(x) \mathrm{d}x = A \\
& 若极限不存在, 则称反常积分 \int_{a}^{+ \infty} f(x) \mathrm{d}x 发散 \\
\end{align}
-->

![](../img/di5_2.jpg)

例题 1

<!--
\begin{align}
& 判断反常积分 \int_{1}^{+ \infty} \frac{1}{\sqrt{x} (1 + x)} \mathrm{d}x 的敛散性 \\
& 任取 b > 1, \\
& \;\;\;\; \int_{1}^{b} \frac{1}{\sqrt{x} (1 + x)} \mathrm{d}x \\
& {\color{Green} // 把 \frac{1}{\sqrt{x}} 放到 d 后面} \\
& = 2 \int_{1}^{b} \frac{1}{1 + x} \mathrm{d}(\sqrt{x}) \\
& = 2 \int_{1}^{b} \frac{1}{1 + (\sqrt{x})^2} \mathrm{d}(\sqrt{x}) \\
& = 2 \arctan \sqrt{x} \big|_{1}^{b} \\
& = 2 (\arctan \sqrt{b} - \frac{\pi}{4}) \\
& \lim_{b \to + \infty} 2 (\arctan \sqrt{b} - \frac{\pi}{4}) = \frac{\pi}{2} \\
& 所以反常积分收敛于 \frac{\pi}{2} \\
\end{align}
-->

![](../img/di5_3.jpg)

敛散性判别法

<!--
\begin{align}
& 1、如果存在 \alpha > 1, 使得 \lim_{x \to + \infty} x^{\alpha} f(x) 存在, \\
& \;\;\;\;\; 则反常积分 \int_{a}^{+ \infty} f(x) \mathrm{d}x 收敛 \\
& 2、如果存在 \alpha \le 1, 使得 \lim_{x \to + \infty} x^{\alpha} f(x) = k \; (k \ne 0), \\
& \;\;\;\;\; 或者 \lim_{x \to + \infty} x^{\alpha} f(x) = \infty \\
& \;\;\;\;\; 则反常积分 \int_{a}^{+ \infty} f(x) \mathrm{d}x 发散 \\
\end{align}
-->

![](../img/di5_4.jpg)

例题 1

<!--
\begin{align}
& 判断反常积分 \int_{0}^{+ \infty} \frac{\sqrt{x}}{4 + x^2} \mathrm{d}x 的敛散性 \\
& {\color{Green} // 要判断 \lim_{x \to + \infty} x^{\alpha} f(x) 是否存在} \\
& \;\;\;\; \lim_{x \to + \infty} x^{\alpha} \frac{\sqrt{x}}{4 + x^2} \\
& {\color{Green} // 分子最大是 \frac{1}{2} 次方, 分母是 2次方, 相差 \frac{3}{2} 次方} \\
& {\color{Green} // 所以 \alpha 取 \frac{3}{2}} \\
& = \lim_{x \to + \infty} x^{\frac{3}{2}} \frac{\sqrt{x}}{4 + x^2} \\
& = \lim_{x \to + \infty} x^{\frac{3}{2}} \frac{x^{\frac{1}{2}}}{4 + x^2} \\
& = \lim_{x \to + \infty} \frac{x^2}{4 + x^2} \\
& = 1 \\
& 因为 \alpha = \frac{3}{2} > 1, 且极限存在, 所以反常积分收敛 \\
\end{align}
-->

![](../img/di5_5.jpg)
