# 中值定理

<!--
\begin{align}
& {\Large 型1：f^{(n)}(\xi)=0} \\
\\
& {\large 如果n=1, 则需要找两个相等的函数值 f(a)=f(b)} \\
\\
& {\color{BLue} 例题：f(x)在[0,2]连续，(0,2)内可导，} \\
& {\color{BLue} 且f(0)=1，f(1)+2f(2)=3，} \\
& {\color{BLue} 证明：存在\xi\in(0,2)，使f'(\xi)=0} \\
& {\color{Green} // 闭区间连续、函数值相加 \Rightarrow 使用介值定理} \\
& 因为  f(x) 在 [0, 2] 上连续, 所以存在最大值 M 和最小值 m \\
& {\color{Green} // f(1)+2f(2) 一共是3个f相加} \\
& {\color{Green} // 所以m和M也乘3} \\
& 因为 3m \le f(1)+2f(2) \le 3M \\
& 所以 3m \le 3 \le 3M \\
& 得到 m \le 1 \le M，则1是介值 \\
& 根据介值定理, 一定存在 c \in [1, 2], 使 f(c) = 1 \\
& 由于f(0)=1、f(c)=1，且0\ne c \\
& 根据罗尔定理，存在 \xi \in (0, c) \subset (0,2), 使 f'(\xi) = 0 \\
\\
& {\color{BLue} 例题：f(x)在[0,1]连续，(0,1)内可导，} \\
& {\color{BLue} 且f(0)=-1，f(\frac{1}{2})=1，f(1)=\frac{1}{2}，} \\
& {\color{BLue} 证明：存在\xi\in(0,1)，使f'(\xi)=0} \\
& 令 h(x)=f(x)-\frac{1}{2}, 那么h(x)在[0,\frac{1}{2}]上连续 \\
& \; h(0)=-\frac{1}{2}，h(\frac{1}{2})=\frac{1}{2} \\
& 所以h(0)\cdot h(\frac{1}{2})\lt0 \\
& {\color{Green} // f(x) 在 [a, b] 上连续, 且 f(a) \cdot f(b) \lt 0，使用零点定理} \\
& 根据零点定理, 存在 c \in (0, \frac{1}{2}), 使 h(c) = 0 \\
& \; h(c)=0时，f(c)=\frac{1}{2} \\
& 因为 f(c)=f(1)=\frac{1}{2}，且0\ne c \\
& 根据罗尔定理，存在 \xi \in (0, c) \subset (0,1), 使 f'(\xi) = 0 \\
\\
& {\large 如果n=2, 则\left\{\begin{matrix}
找三个点用两次拉格朗日 \\
找两个点的一阶导数相等
\end{matrix}\right.}  \\
\\
& {\color{BLue} 例题：f(x)在[0,5]连续，(0,5)内二阶可导，} \\
& {\color{BLue} 3f(0)=f(1)+2f(2)=f(3)+f(4)+f(5)} \\
& {\color{BLue} 证明：存在\xi\in(0,5)，使f''(\xi)=0} \\
& {\color{Green} // 闭区间连续, 函数值相加 \Rightarrow 用介值定理} \\
& 因为 f(x) 在 [0, 5] 上连续, 所以存在最大值 M 和最小值 m \\
& 3m \le 3f(0) \le 3M \\
& 3m \le f(1)+2f(2) \le 3M \\
& m \le \frac{f(1)+2f(2)}{3} \le M \\
& \frac{f(1)+2f(2)}{3} 是介值 \\
& 根据介值定理，存在 c \in [1, 5], 使 f(c) = \frac{f(1)+2f(2)}{3} \\

\end{align}
-->
