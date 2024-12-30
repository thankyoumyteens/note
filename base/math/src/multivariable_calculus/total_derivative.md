# 全微分

<!--
\begin{align}
& 设二元函数 z = f(x, y) \quad (x, y) \in D, (x_0, y_0) \in D \\
& \; \Delta z = f(x_0 + \Delta x, y_0 + \Delta y) - f(x_0, y_0) \\
& 或者 z = f(x, y) - f(x_0, y_0) \\
& 令 \rho = \sqrt{(\Delta x)^2 + (\Delta y)^2} \\
& 如果 \Delta z = A \Delta x + B \Delta y + o(\rho) \\
& 则称 z = f(x, y) 在 (x_0, y_0) 处可全微, 简称可微 \\
& 记为 \mathrm{d}z \big|_{M_0} = A \Delta x + B \Delta y \\
& 习惯上记为 \mathrm{d}z \big|_{M_0} = A \mathrm{d}x + B \mathrm{d}y \\
\end{align}
-->

![](../img/td1.jpg)

<!--
\begin{align}
& 如果 \Delta z = A \Delta x + B \Delta y + o(\rho) \\
& 则 A = \frac{\partial z}{\partial x}\big|_{M_0}, B = \frac{\partial z}{\partial y}\big|_{M_0} \\
\\
& 如果 z = f(x, y) 可微 \\
& 则 \mathrm{d}z = \frac{\partial z}{\partial x}\mathrm{d}x + \frac{\partial z}{\partial y}\mathrm{d}y \\
&
\end{align}
-->

![](../img/td2.jpg)

例题

<!--
\begin{align}
& z = x^2 \ln (1 + \tan y), 求 \mathrm{d}z \\
& \frac{\partial z}{\partial x} = 2x \ln (1 + \tan y) \\
& \frac{\partial z}{\partial y} = x^2 \frac{\sec ^2 y}{1 + \tan y} \\
& \mathrm{d}z = \frac{\partial z}{\partial x}\mathrm{d}x + \frac{\partial z}{\partial y}\mathrm{d}y \\
& \quad = 2x \ln (1 + \tan y) \mathrm{d}x + x^2 \frac{\sec ^2 y}{1 + \tan y} \mathrm{d}y \\
\end{align}
-->

![](../img/td3.jpg)

- 可微一定连续
- 可微一定可偏导
