# 优化选择排序

循环不变量: `data[i...n)` 是没有排序的, `data[0...i)` 是排好序的。

循环体: 每次循环都要把找到的最小值 `data[minIndex]` 放到 `data[i]` 的位置, 以维持循环不变量。

时间复杂度: O(n<sup>2</sup>)

![](../img/selection_sort2.jpg)
