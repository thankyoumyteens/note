# 换元积分法

<!--
\mathrm{d}f(x) = f'(x)\mathrm{d}x
-->

## 第一类换元积分法

例题 1

<!--
\begin{align}
& \;\;\;\; \int \frac{1}{\sqrt{a^2 - x^2}} \mathrm{d}x \\
& {\color{Green} // 提出一个 a^2 } \\
& = \int \frac{1}{a \sqrt{1 - (\frac{x}{a})^2}} \mathrm{d}x \\
& {\color{Green} // 把 \frac{1}{a} 放到 d 后面, 常数可以直接移动} \\
& = \int \frac{1}{\sqrt{1 - (\frac{x}{a})^2}} \mathrm{d}(\frac{x}{a}) \\
& {\color{Green} // 把 \frac{x}{a} 看成一个整体} \\
& = \arcsin \frac{x}{a} + C \\
\end{align}
-->

![](../img/ii2_1.jpg)

例题 2

<!--
\begin{align}
& \;\;\;\; \int \frac{x + 1}{x^2 + 2x + 3} \mathrm{d}x \\
& {\color{Green} // 分子提出来一个 \frac{1}{2}} \\
& = \frac{1}{2} \int \frac{2x + 2}{x^2 + 2x + 3} \mathrm{d}x \\
& {\color{Green} // 把 2x + 2 放到 d 后面} \\
& = \frac{1}{2} \int \frac{1}{x^2 + 2x + 3} \mathrm{d}(x^2 + 2x) \\
& {\color{Green} // d 后面可以随意加减常数, 给它 +3 和分母一致} \\
& = \frac{1}{2} \int \frac{1}{x^2 + 2x + 3} \mathrm{d}(x^2 + 2x + 3) \\
& {\color{Green} // 把 x^2 + 2x + 3 看成一个整体} \\
& = \frac{1}{2} \ln | x^2 + 2x + 3 | + C \\
& {\color{Green} //  x^2 + 2x + 3 > 0} \\
& = \frac{1}{2} \ln (x^2 + 2x + 3) + C \\
\end{align}
-->

![](../img/ii2_2.jpg)

例题 3

<!--
\begin{align}
& \;\;\;\; \int \frac{x^2}{\sqrt{x^3 + 1}} \mathrm{d}x \\
& {\color{Green} // 把 x^2 放到 d 后面} \\
& = \int \frac{1}{\sqrt{x^3 + 1}} \mathrm{d}(\frac{1}{3} x^3) \\
& {\color{Green} // 把 \frac{1}{3} 拿到外面} \\
& = \frac{1}{3} \int \frac{1}{\sqrt{x^3 + 1}} \mathrm{d}(x^3) \\
& {\color{Green} // d 后面可以随意加减常数, 给它 +1 和分母一致} \\
& = \frac{1}{3} \int \frac{1}{\sqrt{x^3 + 1}} \mathrm{d}(x^3 + 1) \\
& {\color{Green} // 把 x^3 + 1 看成一个整体,}  \\
& {\color{Green} // 凑成公式: \int \frac{1}{2 \sqrt{x}} \mathrm{d}x = \sqrt{x} + C}  \\
& = \frac{2}{3} \int \frac{1}{2 \sqrt{x^3 + 1}} \mathrm{d}(x^3 + 1) \\
& = \frac{2}{3} \sqrt{x^3 + 1} + C \\
\end{align}
-->

![](../img/ii2_3.jpg)

例题 4

<!--
\begin{align}
& \;\;\;\; \int \frac{x}{4 + x^4} \mathrm{d}x \\
& {\color{Green} // 把 x 放到 d 后面} \\
& = \frac{1}{2} \int \frac{1}{4 + x^4} \mathrm{d}(x^2) \\
& {\color{Green} // 把分母的 x 写成和 d 后面的 x 一样} \\
& = \frac{1}{2} \int \frac{1}{2^2 + (x^2)^2} \mathrm{d}(x^2) \\
& {\color{Green} // 把 x^2 看成一个整体,}  \\
& {\color{Green} // 使用公式: \int \frac{1}{a^2 + x^2} \mathrm{d}x = \frac{1}{a} \arctan \frac{x}{a} + C}  \\
& = \frac{1}{4} \arctan \frac{x^2}{2} + C \\
\end{align}
-->

![](../img/ii2_4.jpg)

例题 5

<!--
\begin{align}
& \;\;\;\; \int \frac{\mathrm{d}x}{\sqrt{x} (1 + x)} \\
& {\color{Green} // 凑成公式: \int \frac{1}{2 \sqrt{x}} \mathrm{d}x = \sqrt{x} + C} \\
& = 2 \int \frac{\mathrm{d}x}{2 \sqrt{x} (1 + x)} \\
& {\color{Green} // 把\frac{1}{2 \sqrt{x}} 放到 d 后面} \\
& = 2 \int \frac{\mathrm{d}(\sqrt{x})}{1 + x} \\
& {\color{Green} // 凑成公式: \int \frac{1}{1 + x^2} \mathrm{d}x = \arctan x + C}  \\
& = 2 \int \frac{\mathrm{d}(\sqrt{x})}{1 + (\sqrt{x})^2} \\
& {\color{Green} // 把 \sqrt{x} 看成一个整体}  \\
& = 2 \arctan \sqrt{x} + C \\
\end{align}
-->

![](../img/ii2_5.jpg)

例题 6

<!--
\begin{align}
& \;\;\;\; \int \frac{\tan ^2 \sqrt{x}}{\sqrt{x}} \mathrm{d}x \\
& {\color{Green} // 凑成公式: \int \frac{1}{2 \sqrt{x}} \mathrm{d}x = \sqrt{x} + C} \\
& = 2 \int \frac{\tan ^2 \sqrt{x}}{2\sqrt{x}} \mathrm{d}x \\
& {\color{Green} // 把\frac{1}{2 \sqrt{x}} 放到 d 后面} \\
& = 2 \int (\tan ^2 \sqrt{x}) \mathrm{d}(\sqrt{x}) \\
& {\color{Green} // 三角恒等式: \tan ^{2} x + 1 = \sec ^{2} x}  \\
& = 2 \int (\sec ^{2} \sqrt{x} - 1) \mathrm{d}(\sqrt{x}) \\
& = 2 \int (\sec ^{2} \sqrt{x}) \mathrm{d}(\sqrt{x}) - 2 \int 1 \mathrm{d}(\sqrt{x}) \\
& {\color{Green} // (\tan x)' = \sec^{2} x}  \\
& = 2 \tan \sqrt{x} - 2\sqrt{x} + C \\
\end{align}
-->

![](../img/ii2_6.jpg)

例题 7

<!--
\begin{align}
& \;\;\;\; \int \frac{e^x}{4 + e^{2x}} \mathrm{d}x \\
& {\color{Green} // 凑成公式: \int \frac{1}{a^2 + x^2} \mathrm{d}x = \frac{1}{a} \arctan \frac{x}{a} + C} \\
& = \int \frac{1}{2^2 + (e^{x})^2} \mathrm{d}(e^x) \\
& = \frac{1}{2} \arctan \frac{e^x}{2} + C \\
\end{align}
-->

![](../img/ii2_7.jpg)

例题 8

<!--
\begin{align}
& \;\;\;\; \int \frac{1}{1 + e^x} \mathrm{d}x \\
& {\color{Green} // 提取 e^x} \\
& = \int \frac{1}{e^x(e^{-x} + 1)} \mathrm{d}x \\
& = \int \frac{e^{-x}}{e^{-x} + 1} \mathrm{d}x \\
& {\color{Green} // e^{-x}放到 d 后面} \\
& = \int \frac{1}{e^{-x} + 1} \mathrm{d}(-e^{-x}) \\
& = - \int \frac{1}{e^{-x} + 1} \mathrm{d}(e^{-x}) \\
& {\color{Green} // d 后面可以随意加减常数, 给它 +1 和分母一致} \\
& = - \int \frac{1}{e^{-x} + 1} \mathrm{d}(e^{-x} + 1) \\
& = - \ln (e^{-x} + 1) + C \\
\end{align}
-->

![](../img/ii2_8.jpg)

例题 9

<!--
\begin{align}
& \;\;\;\; \int \frac{\sin x}{\sin x + \cos x} \mathrm{d}x \\
& {\color{Green} // 辅助角公式 a \sin x + b \cos x = \sqrt{a^2 + b^2} \sin (x + \arctan \frac{b}{a}), (a > 0)} \\
& {\color{Green} // 或者 a \sin x + b \cos x = \sqrt{a^2 + b^2} \cos (x - \arctan \frac{a}{b}), (b > 0)} \\
& = \int \frac{\sin x}{\sqrt{1^2 + 1^2} \cos (x - \arctan 1)} \mathrm{d}x \\
& {\color{Green} // \arctan 1 = \frac{\pi}{4}} \\
& = \frac{1}{\sqrt{2}} \int \frac{\sin x}{\cos (x - \frac{\pi}{4})} \mathrm{d}x \\
& = \frac{1}{\sqrt{2}} \int \frac{\sin [(x - \frac{\pi}{4}) + \frac{\pi}{4}]}{\cos (x - \frac{\pi}{4})} \mathrm{d}x \\
& = \frac{1}{\sqrt{2}} \int \frac{\sin [(x - \frac{\pi}{4}) + \frac{\pi}{4}]}{\cos (x - \frac{\pi}{4})} \mathrm{d}(x - \frac{\pi}{4}) \\
& {\color{Green} // 和差化积公式 \sin (a + b) = \sin a \cos b + \cos a \sin b} \\
& = \frac{1}{\sqrt{2}} \int \frac{\sin (x - \frac{\pi}{4}) \cos \frac{\pi}{4} + \cos (x - \frac{\pi}{4}) \sin \frac{\pi}{4}}{\cos (x - \frac{\pi}{4})} \mathrm{d}(x - \frac{\pi}{4}) \\
& {\color{Green} // \cos \frac{\pi}{4} = \sin \frac{\pi}{4} = \frac{1}{\sqrt{2}}} \\
& = \frac{1}{\sqrt{2}} \int \frac{\frac{1}{\sqrt{2}} [\sin (x - \frac{\pi}{4}) + \cos (x - \frac{\pi}{4})]}{\cos (x - \frac{\pi}{4})} \mathrm{d}(x - \frac{\pi}{4}) \\
& = \frac{1}{2} \int \frac{\sin (x - \frac{\pi}{4}) + \cos (x - \frac{\pi}{4})}{\cos (x - \frac{\pi}{4})} \mathrm{d}(x - \frac{\pi}{4}) \\
& = \frac{1}{2} \int \frac{\sin (x - \frac{\pi}{4})}{\cos (x - \frac{\pi}{4})} \mathrm{d}(x - \frac{\pi}{4}) + \frac{1}{2} \int \frac{\cos (x - \frac{\pi}{4})}{\cos (x - \frac{\pi}{4})} \mathrm{d}(x - \frac{\pi}{4}) \\
& = \frac{1}{2} \int \tan (x - \frac{\pi}{4}) \mathrm{d}(x - \frac{\pi}{4}) + \frac{1}{2} \int 1 \mathrm{d}(x - \frac{\pi}{4}) \\
& = \frac{1}{2} \int \tan (x - \frac{\pi}{4}) \mathrm{d}(x - \frac{\pi}{4}) + \frac{1}{2} (x - \frac{\pi}{4}) \\
& {\color{Green} // \int \tan x \mathrm{d}x = -\ln |\cos x| + C} \\
& = -\frac{1}{2} \ln |\cos (x - \frac{\pi}{4})| + \frac{1}{2} (x - \frac{\pi}{4}) + C \\
& {\color{Green} // \frac{1}{2} \times (- \frac{\pi}{4}) 是常数, 合并到 C 中} \\
& = -\frac{1}{2} \ln |\cos (x - \frac{\pi}{4})| + \frac{1}{2} x + C \\
\end{align}
-->

![](../img/ii2_9.jpg)

例题 10

<!--
\begin{align}
& \;\;\;\; \int \frac{\mathrm{d}x}{x^2 + 2x + 5} \\
& {\color{Green} // 分母没法因式分解, 使用配方} \\
& {\color{Green} // 配方: x^2 + 2ax + a^2 = (x + a)^2} \\
& {\color{Green} // 分母是 x^2 + 2x + 5} \\
& {\color{Green} // 所以 2a = 2 \Rightarrow a = 1} \\
& {\color{Green} // 所以把分母写成 (x + 1)^2} \\
& {\color{Green} // 再把少的值加上 (x + 1)^2 + 4} \\
& = \int \frac{\mathrm{d}x}{4 + (x + 1)^2} \\
& = \int \frac{\mathrm{d}x}{2^2 + (x + 1)^2} \\
& = \int \frac{\mathrm{d}(x + 1)}{2^2 + (x + 1)^2} \\
& {\color{Green} // \int \frac{1}{a^2 + x^2} \mathrm{d}x = \frac{1}{a} \arctan \frac{x}{a} + C} \\
& = \frac{1}{2} \arctan \frac{x + 1}{2} + C \\
\end{align}
-->

![](../img/ii2_10.jpg)

例题 11

<!--
\begin{align}
& \;\;\;\; \int \frac{\mathrm{d}x}{x^2 - x - 2} \\
& {\color{Green} // 分母可以因式分解} \\
& = \int \frac{\mathrm{d}x}{(x - 2)(x + 1)} \\
& {\color{Green} // 拆项, 并确保分子中没有x} \\
& {\color{Green} // 因为 \frac{1}{x - 2} - \frac{1}{x + 1} = \frac{x + 1 - (x - 2)}{(x - 2)(x + 1)} = \frac{3}{(x - 2)(x + 1)}} \\
& {\color{Green} // 所以需要补个 \frac{1}{3}} \\
& = \int \frac{\frac{1}{3} [x + 1 - (x - 2)]}{(x - 2)(x + 1)} \mathrm{d}x \\
& = \frac{1}{3} \int (\frac{1}{x - 2} - \frac{1}{x + 1}) \mathrm{d}x \\
& = \frac{1}{3} (\int \frac{\mathrm{d}x}{x - 2} - \int \frac{\mathrm{d}x}{x + 1} ) \\
& = \frac{1}{3} [\int \frac{\mathrm{d}(x - 2)}{x - 2} - \int \frac{\mathrm{d}(x + 1)}{x + 1} ] \\
& = \frac{1}{3} (\ln |x - 2| - \ln |x + 1|) + C \\
& = \frac{1}{3} \ln |\frac{x - 2}{x + 1}| + C \\
\end{align}
-->

![](../img/ii2_11.jpg)

例题 12

<!--
\begin{align}
& \;\;\;\; \int \frac{\mathrm{d}x}{\sqrt{x} (4 + x)} \\
& {\color{Green} // 分母有 \sqrt{x}, 就用公式: \int \frac{1}{2 \sqrt{x}} \mathrm{d}x = \sqrt{x} + C} \\
& = \int \frac{2 \mathrm{d}(\sqrt{x})}{4 + x} \\
& = 2 \int \frac{\mathrm{d}(\sqrt{x})}{2^2 + (\sqrt{x})^2} \\
& {\color{Green} // \int \frac{1}{a^2 + x^2} \mathrm{d}x = \frac{1}{a} \arctan \frac{x}{a} + C} \\
& = 2(\frac{1}{2} \arctan \frac{\sqrt{x}}{2}) + C \\
& = \arctan \frac{\sqrt{x}}{2} + C \\
\end{align}
-->

![](../img/ii2_12.jpg)

例题 13

<!--
\begin{align}
& \;\;\;\; \int \frac{\mathrm{d}x}{x \ln ^2 x} \\
& {\color{Green} // \frac{1}{x} 放到 d 后面} \\
& = \int \frac{\mathrm{d}(\ln x)}{\ln ^2 x} \\
& = - \frac{1}{\ln x} + C \\
\end{align}
-->

![](../img/ii2_13.jpg)

## 第二类换元积分法

对于被积函数含平方和或平方差, 或者被积函数为无理函数时, 一般使用第二类换元积分法, 即将 x 表示为一个含 t 的表达式。

<!--
\begin{align}
& 设 x = \varphi (t) 单调、可导且 \varphi '(t) \ne 0, 再令 f[\varphi (t)]\varphi '(t) 的原函数为 G(t), \\
& 则 \int f(x) \mathrm{d}x = \int f[\varphi (t)]\varphi '(t) \mathrm{d}t =
G(t) + C = G[\varphi ^{-1}(x)] + C \\
\end{align}
-->

![](../img/ii2_14.jpg)

被积函数是无理且无法积出来的情况, 需要通过第二类换元积分法把无理转换成有理

<!--
\begin{align}
& \;\;\;\; \int \frac{\mathrm{d}x}{1 + \sqrt{x}} \\
& {\color{Green} // 设 x = t^2} \\
& = \int \frac{\mathrm{d}(t^2)}{1 + t} \\
& = \int \frac{2t\mathrm{d}t}{1 + t} \\
& = 2 \int \frac{t}{1 + t} \mathrm{d}t \\
& = 2 \int (1 - \frac{1}{1 + t}) \mathrm{d}t \\
& = 2 (\int 1 \mathrm{d}t - \int \frac{1}{1 + t} \mathrm{d}t) \\
& = 2 (t - \int \frac{1}{1 + t} \mathrm{d}t) \\
& = 2 (t - \ln |1 + t|) + C \\
& = 2 \sqrt{x} - 2 \ln (1 + \sqrt{x}) + C \\
\end{align}
-->

![](../img/ii2_15.jpg)

### 三角代换

<!--
\begin{align}
& 1、被积函数表达式: \sqrt{a^2 - x^2} \\
& \quad\;\, 三角换元替换式: 令 x = a \sin t \\
& \quad\;\, 则: \sqrt{a^2 - x^2} \Rightarrow a \cos t \\
& 2、被积函数表达式: \sqrt{x^2 + a^2} \\
& \quad\;\, 三角换元替换式: 令 x = a \tan t \\
& \quad\;\, 则: \sqrt{x^2 + a^2} \Rightarrow a \sec t \\
& 3、被积函数表达式: \sqrt{x^2 - a^2} \\
& \quad\;\, 三角换元替换式: 令 x = a \sec t \\
& \quad\;\, 则: \sqrt{x^2 - a^2} \Rightarrow a \tan t \\
\end{align}
-->

![](../img/ii2_16.jpg)

例题 1

<!--
\begin{align}
& \;\;\;\; \int \frac{\mathrm{d}x}{\sqrt{x^2 + a^2}} \\
& {\color{Green} // 令 x = a \tan t} \\
& = \int \frac{\mathrm{d}(a \tan t)}{a \sec t} \\
& {\color{Green} // (\tan x)' = \sec^{2} x} \\
& = \int \frac{a \sec^{2} x}{a \sec t} \mathrm{d}t \\
& = \int \sec t \mathrm{d}t \\
& {\color{Green} // \int \sec x \mathrm{d}x = \ln |\sec x + \tan x| + C} \\
& = \ln |\sec t + \tan t| + C \\
& {\color{Green} // x = a \tan t \Rightarrow \tan t = \frac{x}{a}} \\
& {\color{Green} // 因为 令 x = a \tan t \Rightarrow \tan t = \frac{x}{a}} \\
& {\color{Green} // 画一个直角三角形, 两个直角边是 x 和 a, 斜边就是 \sqrt{x^2 + a^2}} \\
& {\color{Green} // \sec t = \frac{1}{\cos t} = \frac{\sqrt{x^2 + a^2}}{a}} \\
& = \ln |\frac{\sqrt{x^2 + a^2}}{a} + \frac{x}{a}| + C \\
& = \ln \frac{\sqrt{x^2 + a^2} + x}{a} + C \\
& = \ln (\sqrt{x^2 + a^2} + x) - \ln a + C \\
& {\color{Green} // - \ln a 是常数, 合并到 C 中} \\
& = \ln (\sqrt{x^2 + a^2} + x) + C \\
\end{align}
-->

![](../img/ii2_17.jpg)

例题 2

<!--
\begin{align}
& \;\;\;\; \int \frac{\mathrm{d}x}{x^2 \sqrt{1 - x^2}} \\
& {\color{Green} // 令 x = \sin t} \\
& = \int \frac{\mathrm{d}(\sin t)}{\sin ^2 t \sqrt{1 - \sin ^2 t}} \\
& {\color{Green} // (\sin x)' = \cos x} \\
& = \int \frac{\cos t}{\sin ^2 t \sqrt{1 - \sin ^2 t}} \mathrm{d}t \\
& {\color{Green} // 毕达哥拉斯定理: \sin ^{2} x + \cos ^{2} x = 1} \\
& = \int \frac{\cos t}{\sin ^2 t \cos t} \mathrm{d}t \\
& = \int \frac{1}{\sin ^2 t} \mathrm{d}t \\
& {\color{Green} // \csc x = \frac{1}{\sin x} \Rightarrow \csc ^2 x = \frac{1}{\sin ^2 x}} \\
& = \int \csc ^2 t \mathrm{d}t \\
& {\color{Green} // \int \csc ^2 x \mathrm{d}x = -\cot x + C} \\
& = -\cot t + C \\
& {\color{Green} // 因为 令 x = \sin t \Rightarrow \sin t = \frac{x}{1}} \\
& {\color{Green} // 画一个直角三角形, 对边是 x 斜边是 1, 邻边就是 \sqrt{1 + x^2}} \\
& {\color{Green} // \cot 是临比对} \\
& = -\frac{\sqrt{1 + x^2}}{x} + C \\
\end{align}
-->

![](../img/ii2_18.jpg)

例题 3

<!--
\begin{align}
& \;\;\;\; \int \frac{\mathrm{d}x}{x^2 \sqrt{x^2 + 1}} \\
& {\color{Green} // 令 x = \tan t} \\
& = \int \frac{\mathrm{d}(\tan t)}{(\tan t)^2 \sqrt{(\tan t)^2 + 1}} \\
& {\color{Green} // (\tan x)' = \sec^{2} x} \\
& = \int \frac{\sec^{2} t}{(\tan t)^2 \sqrt{(\tan t)^2 + 1}} \mathrm{d}t \\
& {\color{Green} // 毕达哥拉斯定理: \tan ^{2} x + 1 = \sec ^{2} x} \\
& = \int \frac{\sec^{2} t}{\tan ^{2} t \sec t} \mathrm{d}t \\
& = \int \frac{\sec t}{\tan ^{2} t} \mathrm{d}t \\
& {\color{Green} // \sec x = \frac{1}{\cos x}} \\
& = \int \frac{\frac{1}{\cos t}}{\frac{\sin ^2 t}{\cos ^2 t}} \mathrm{d}t \\
& = \int \frac{\cos t}{\sin ^2 t} \mathrm{d}t \\
& {\color{Green} // (\sin x)' = \cos x} \\
& = \int \frac{1}{\sin ^2 t} \mathrm{d}(\sin t) \\
& = - \frac{1}{\sin t} + C \\
& {\color{Green} // 因为 令 x = \tan t \Rightarrow \tan t = \frac{x}{1}} \\
& {\color{Green} // 所以画一个直角三角形, 对边是 x 临边是 1, 斜边就是 \sqrt{1 + x^2}} \\
& {\color{Green} // \sin 是对比斜} \\
& = - \frac{1}{\frac{x}{\sqrt{1 + x^2}}} + C \\
& = - \frac{\sqrt{1 + x^2}}{x} + C \\
\end{align}
-->

![](../img/ii2_19.jpg)
