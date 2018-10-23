# 二叉堆

## 满足的条件

1. 最大堆的任何一个节点不大于他的父亲节点
2. 最小堆的任何一个节点不小于他的父亲节点
3. 是完全二叉树

![](img/heap.png)

## 使用数组实现二叉堆

![]()

根节点从1开始建立索引, 根据某个节点的索引(index)可以计算出它的根节点和子节点的索引

- parent(index) = index / 2
- leftChild(index) = 2 * index
- rightChild(index) = 2 * index + 1

