# 定积分的几何应用

## 面积

<!--
\begin{align}
& 设平面区域 D 由 L: y = f(x) 及直线 x = a, x = b 围成, \\
& 则区域 D 的面积为: A = \int_{a}^{b} f(x) \mathrm{d} x \\
\\
& 设平面区域 D 由 L: y = g(x), y = f(x) \; (g(x) \le f(x)) 及直线 x = a, x = b 围成, \\
& 则区域 D 的面积为: A = \int_{a}^{b} [f(x) - g(x)] \mathrm{d} x \\
\\
& 设平面区域 D 由 L: r = r(\theta) 及射线 \theta = \alpha, \theta = \beta 围成, \\
& 则区域 D 的面积为: A = \frac{1}{2} \int_{\alpha}^{\beta} r^2(\theta) \mathrm{d} \theta \\
\\
& 设平面区域 D 由 L_1: r_1 = r_1(\theta), L_2: r_2 = r_2(\theta) \; (r_1(\theta) \le r_2(\theta)) 及射线 \theta = \alpha, \theta = \beta 围成, \\
& 则区域 D 的面积为: A = \frac{1}{2} \int_{\alpha}^{\beta} [r_2^2(\theta) - r_1^2(\theta)] \mathrm{d} \theta \\
\end{align}
-->

![](../img/di6_0.jpg)

例题 1

<!--
\begin{align}
& 求 L: (x^2 + y^2)^2 = 4(x^2 - y^2) 围成的面积 \\
& {\color{Green} // 遇到 x^2 + y^2 就转换成极坐标} \\
& 令 \begin{cases}
x = r \cos \theta \\
y = r \sin \theta \\
\end{cases}, \\
& {\color{Green} // L: (r^2 \cos ^2 \theta + r^2 \sin ^2 \theta)^2 = 4(r^2 \cos ^2 \theta - r^2 \sin ^2 \theta)} \\
& {\color{Green} // L: r^4 = 4 r^2(\cos ^2 \theta - \sin ^2 \theta)} \\
& {\color{Green} // L: r^2 = 4(\cos ^2 \theta - \sin ^2 \theta)} \\
& {\color{Green} // L: r^2 = 4 \cos 2 \theta} \\
& 则 L: r^2 = 4 \cos 2 \theta \\
& {\color{Green} // L 是双纽线, 四个象限的面积相等, 求第一象限的面积再乘4即可} \\
& {\color{Green} // A = \frac{1}{2} \int_{\alpha}^{\beta} r^2(\theta) \mathrm{d} \theta} \\
& A = \frac{1}{2} \int_{0}^{\frac{\pi}{4}} r^2(\theta) \mathrm{d} \theta \\
& \;\;\, = \frac{1}{2} \int_{0}^{\frac{\pi}{4}} 4 \cos 2 \theta \mathrm{d} \theta \\
& \;\;\, = \int_{0}^{\frac{\pi}{4}} 2 \cos 2 \theta \mathrm{d} \theta \\
& \;\;\, = \int_{0}^{\frac{\pi}{4}} \cos 2 \theta \mathrm{d}(2 \theta) \\
& \;\;\, = \int_{0}^{\frac{\pi}{2}} \cos \theta \mathrm{d} \theta \\
& \;\;\, = 1 \\
& 整个的面积: 4A = 4 \\
\end{align}
-->

![](../img/di6_1.jpg)

例题 2

<!--
\begin{align}
& 求椭圆 L: \frac{x^2}{a^2} + \frac{y^2}{b^2} = 1 \; (a > 0, b > 0) 所围成的区域面积 \\
\\
& 方法1使用直角坐标 \\
& {\color{Green} // 椭圆四个象限的面积相等, 求第一象限的面积再乘4即可} \\
& {\color{Green} // 转成 y = f(x) 的形式} \\
& \frac{x^2}{a^2} + \frac{y^2}{b^2} = 1 \\
& b^2 x^2 + a^2 y^2 = a^2 b^2 \\
& a^2 y^2 = a^2 b^2 - b^2 x^2 \\
& y^2 = \frac{b^2}{a^2} (a^2 - x^2) \\
& y = \frac{b}{a} \sqrt{a^2 - x^2} \; (0 \le x \le a) \\
& {\color{Green} // 第一象限的面积就是曲边梯形的面积} \\
& A = \frac{b}{a} \int_{0}^{a} \sqrt{a^2 - x^2} \mathrm{d}x \\
& {\color{Green} // y = \sqrt{a^2 - x^2} 是圆形, 第一象限就是 \frac{1}{4} 个圆} \\
& A = \frac{b}{a} \frac{\pi}{4} a^2 \\
& A = \frac{\pi}{4} ab \\
& 椭圆的面积就是 4A = \pi ab \\
\end{align}
-->

![](../img/di6_2.jpg)

例题 3

<!--
\begin{align}
& 求椭圆 L: \frac{x^2}{a^2} + \frac{y^2}{b^2} = 1 \; (a > 0, b > 0) 所围成的区域面积 \\
\\
& 方法2使用极坐标 \\
& {\color{Green} // 椭圆四个象限的面积相等, 求第一象限的面积再乘4即可} \\
& 令 \begin{cases}
x = r \cos \theta \\
y = r \sin \theta \\
\end{cases}, 则 L: \frac{r^2 \cos ^2 \theta}{a^2} + \frac{r^2 \sin ^2 \theta}{b^2} = 1 \\
& {\color{Green} // 转换成 r^2 = r^2(\theta) 的形式} \\
& r^2 (\frac{\cos ^2 \theta}{a^2} + \frac{\sin ^2 \theta}{b^2}) = 1 \\
& r^2 \frac{b^2 \cos ^2 \theta + a^2 \sin ^2 \theta}{a^2 b^2} = 1 \\
& r^2 = \frac{a^2 b^2}{b^2 \cos ^2 \theta + a^2 \sin ^2 \theta} \\
& {\color{Green} // 第一象限的面积就是扇形的面积} \\
& A = \frac{1}{2} \int_{0}^{\frac{\pi}{2}} \frac{a^2 b^2}{b^2 \cos ^2 \theta + a^2 \sin ^2 \theta} \mathrm{d}x \\
& A = \frac{a^2 b^2}{2} \int_{0}^{\frac{\pi}{2}} \frac{1}{b^2 \cos ^2 \theta + a^2 \sin ^2 \theta} \mathrm{d}x \\
& {\color{Green} // 遇到分子/分母是 \sin 和 \cos 的平方这种积分} \\
& {\color{Green} // 就把分子和分母同除以 \cos ^2 \theta} \\
& A = \frac{a^2 b^2}{2} \int_{0}^{\frac{\pi}{2}} \frac{\frac{1}{\cos ^2 \theta}}{\frac{b^2 \cos ^2 \theta + a^2 \sin ^2 \theta}{\cos ^2 \theta}} \mathrm{d}x \\
& {\color{Green} // \frac{1}{\cos ^2 \theta} = \sec ^2 \theta, 并且 (\sec ^2 \theta)' = \tan \theta} \\
& {\color{Green} // 把 \sec ^2 \theta 移到 d 后面} \\
& A = \frac{a^2 b^2}{2} \int_{0}^{\frac{\pi}{2}} \frac{1}{\frac{b^2 \cos ^2 \theta + a^2 \sin ^2 \theta}{\cos ^2 \theta}} \mathrm{d}(\tan \theta) \\
& A = \frac{a^2 b^2}{2} \int_{0}^{\frac{\pi}{2}} \frac{1}{b^2 + a^2 \frac{\sin ^2 \theta}{\cos ^2 \theta}} \mathrm{d}(\tan \theta) \\
& A = \frac{a^2 b^2}{2} \int_{0}^{\frac{\pi}{2}} \frac{1}{b^2 + a^2 \tan ^2 \theta} \mathrm{d}(\tan \theta) \\
& A = \frac{a^2 b^2}{2} \int_{0}^{\frac{\pi}{2}} \frac{1}{b^2 + (a \tan \theta)^2} \mathrm{d}(\tan \theta) \\
& {\color{Green} // 把常数 a 拿一个到 d 后面} \\
& A = \frac{a b^2}{2} \int_{0}^{\frac{\pi}{2}} \frac{1}{b^2 + (a \tan \theta)^2} \mathrm{d}(a \tan \theta) \\
& {\color{Green} // \int \frac{1}{a^2 + x^2} \mathrm{d}x = \frac{1}{a} \arctan \frac{x}{a} + C} \\
& A = \frac{a b^2}{2} \frac{1}{b} \arctan \frac{a \tan \theta}{b} \big|_{0}^{\frac{\pi}{2}} \\
& {\color{Green} // \tan 0 = 0} \\
& {\color{Green} // \tan \frac{\pi}{2} = + \infty} \\
& {\color{Green} // \arctan + \infty = \frac{\pi}{2}} \\
& A = \frac{a b}{2} \frac{\pi}{2} \\
& A = \frac{\pi}{4} ab \\
& 椭圆的面积就是 4A = \pi ab \\
\end{align}
-->

![](../img/di6_3.jpg)

## 体积

<!--
\begin{align}
& 设平面区域 D 由 L: y = f(x) 、直线 x = a, x = b 以及 x 轴围成的曲边梯形, \\
\\
& 1、区域 D 绕 x 轴旋转一周而成的几何体的体积为: \\
& \quad \;\;\, V_x = \pi \int_{a}^{b} f^2(x) \mathrm{d} x \\
\\
& 2、区域 D 绕 y 轴旋转一周而成的几何体的体积为: \\
& \quad \;\;\, V_y = 2 \pi \int_{a}^{b} x f(x) \mathrm{d} x \\
\end{align}
-->

![](../img/di6_4.jpg)

例题

<!--
\begin{align}
& L: y = \sqrt{2x - x^2} \; (0 \le x \le 2), 求 V_x 和 V_y \\
\\
& V_x = \pi \int_{a}^{b} f^2(x) \mathrm{d} x \\
& \;\;\;\, = \pi \int_{0}^{2} \sqrt{2x - x^2}^2 \mathrm{d} x \\
& \;\;\;\, = \pi \int_{0}^{2} (2x - x^2) \mathrm{d} x \\
& \;\;\;\, = \pi (\int_{0}^{2} 2x \mathrm{d} x - \int_{0}^{2} x^2 \mathrm{d} x) \\
& \;\;\;\, = \pi (4 - \frac{8}{3}) \\
& \;\;\;\, = \frac{4}{3} \pi \\
\\
& V_y = 2 \pi \int_{a}^{b} x f(x) \mathrm{d} x \\
& \;\;\;\, = 2\pi \int_{0}^{2} x \sqrt{2x - x^2} \mathrm{d} x \\
& {\color{Green} // 配方: x^2 + 2ax + a^2 = (x + a)^2} \\
& {\color{Green} // 根号里是 -(x^2 - 2x)} \\
& {\color{Green} // 所以 a = 1 \Rightarrow -(x^2 - 2x + 1 - 1)} \\
& {\color{Green} // \Rightarrow -(x - 1)^2 + 1} \\
& \;\;\;\, = 2\pi \int_{0}^{2} x \sqrt{1 - (x - 1)^2} \mathrm{d} x \\
& \;\;\;\, = 2\pi \int_{0}^{2} (x - 1 + 1) \sqrt{1 - (x - 1)^2} \mathrm{d} x \\
& \;\;\;\, = 2\pi \int_{0}^{2} (x - 1 + 1) \sqrt{1 - (x - 1)^2} \mathrm{d} (x - 1) \\
& {\color{Green} // x - 1 换成 t} \\
& \;\;\;\, = 2\pi \int_{-1}^{1} (t + 1) \sqrt{1 - t^2} \mathrm{d} t \\
& \;\;\;\, = 2\pi (\int_{-1}^{1} t\sqrt{1 - t^2} \mathrm{d} t + \int_{-1}^{1} \sqrt{1 - t^2} \mathrm{d} t) \\
& {\color{Green} // 对称区间的定积分性质} \\
& {\color{Green} // 若 f(-x) = - f(x), 则 \int_{-a}^{a} f(x) \mathrm{d}x = 0} \\
& {\color{Green} // t\sqrt{1 - t^2} 是奇函数} \\
& \;\;\;\, = 2\pi (0 + \int_{-1}^{1} \sqrt{1 - t^2} \mathrm{d} t) \\
& \;\;\;\, = 2\pi \int_{-1}^{1} \sqrt{1 - t^2} \mathrm{d} t \\
& {\color{Green} // y = \sqrt{1 - t^2} 是单位圆, 函数在一三象限, 所以只要其一半面积} \\
& \;\;\;\, = \pi ^ 2 \\
\end{align}
-->

![](../img/di6_5.jpg)
