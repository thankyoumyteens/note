# 优化归并排序

如果左边的数组里所有元素都小于右边的元素, 说明已经有序了, 就不需要再执行合并过程了。

```java
private static void mergeSort(int[] data, int left, int right) {
    if (left >= right) {
        return;
    }

    // 拆分
    int mid = (left + right) / 2;
    mergeSort(data, left, mid);
    mergeSort(data, mid + 1, right);

    // 如果data[mid] <= data[mid+1]，
    // 那么就表示左数组的所有元素都小于右数组
    // 就不需要合并了, 直接返回
    if (data[mid] <= data[mid + 1]) {
        return;
    }

    // 合并
    merge(data, left, mid, right);
}
```
