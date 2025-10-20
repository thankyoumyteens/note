# 随机选择基准值

选择第一个元素作为基准值时，如果数组已排序或接近排序, 会导致划分极度不平衡：

- 基准值左侧没有元素，右侧包含剩余所有元素（或反之）
- 递归树退化为单链，时间复杂度从理想的 O(nlog n) 退化到 O(n^2)

```java
private static void partition(int[] data, int left, int right) {
    if (left >= right) {
        return;
    }

    // 生成一个[left, right]之间的随机整数作为基准值的索引
    int pivot = left + (new Random()).nextInt(right - left + 1);
    // 将基准值放到数组的第一个位置
    swap(data, left, pivot);

    pivot = left;
    int i = pivot + 1;
    int j = pivot;
    // ...
}
```
