# 算法

- <a href="sort.md">排序</a>

## 二分查找(要求输入数组有序)

```
/**
 * 查找target在array中的索引, 没找到返回-1
 */
int search(Comparable[] array, Comparable target) {
    int left = 0;
    int right = array.length - 1;
    // 在array[left, right]中查找target
    while (left <= right) {
        // 取中间的元素
        // int middle = (right + left) / 2; // 数值过大会溢出
        int middle = left + (right - left) / 2;
        if (array[middle].equals(target)) {
            return middle;
        }
        if (target.compareTo(array[middle]) < 0) {
            // 在左半部分查找
            right = middle - 1;
        } else {
            left = middle + 1;
        }
    }
    return -1;
}
```

# 数据结构

- <a href="heap.md">堆</a>
- <a href="binarySearchTree.md">二分搜索树</a>


