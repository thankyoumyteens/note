# 集合

集合: 所有特定性质的对象放在一块。每一个对象叫做元素。

全集: 所有元素都包含。

空集: 没有任何元素。

## 运算

### 交集

<!-- A \cap B 或者 AB -->

![](../img/set1.jpg)

### 并集

<!-- A \cup B 或者 A + B -->

![](../img/set2.jpg)

### 差

属于 A, 但不属于 B

<!-- A \setminus B 或者 A - B -->

![](../img/set3.jpg)
![](../img/set3_1.png)

### 补

不属于 A 的元素构成的集合, 称为 A 的补

<!-- \bar{A} -->

![](../img/set4.jpg)
![](../img/set4_1.jpg)

## 关系

### 包含

A 的所有元素都在 B 中

<!-- A \subset B -->

![](../img/set5.jpg)

### 互斥(不相容)

A 和 B 没有共同的元素

<!-- \begin{align}
& \forall x \in A \Rightarrow x \notin B \\
& 反之, \forall x \in B \Rightarrow x \notin A \\
& 即 AB = \emptyset
\end{align} -->

![](../img/set6.jpg)
![](../img/set6_1.png)

### 对立

<!-- \begin{align}
& \forall x \in A \Rightarrow x \notin B \\
& 反之, \forall x \in B \Rightarrow x \notin A \\
& 且, \forall x \in \Omega \Rightarrow x \in A 或 x \in B \\
& 即 AB = \emptyset 且 A + B = \Omega \\
& 或者 \bar{A} = B
\end{align} -->

![](../img/set7.jpg)
![](../img/set7_1.jpg)
