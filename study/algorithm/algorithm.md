
# 排序(从小到大)

## 选择排序

找到未排序的元素中最小的元素将它与未排序元素的第一个元素交换

找到最小元素: 1
![selectionSort1](img/selectionSort1.png)
与第一个元素: 8 交换
![selectionSort2](img/selectionSort2.png)
找到最小元素: 2
![selectionSort3](img/selectionSort3.png)
与第一个元素: 6 交换
![selectionSort4](img/selectionSort4.png)

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
