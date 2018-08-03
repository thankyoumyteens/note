
# 排序

## 选择排序

```
/**
    * 选择排序
    * @param array 要排序的数据
    */
public void sort(Comparable[] array) {
    for (int i = 0; i < array.length; i++) {
        // 寻找[i,length)区间里的最小值
        // 并把最小值的索引保存到minIndex中
        int minIndex = i;
        for (int j = i + 1; j < array.length; j++) {
            if (array[j].compareTo(array[minIndex]) < 0) {
                minIndex = j;
            }
        }
        // 将最小的元素与剩下的元素列表中第一名元素交换
        ArrayUtil.swap(array, i, minIndex);
        // 此时[0,i]的元素已经排好序
    }
}
```