
# 排序(从小到大)

## 选择排序

找到未排序的元素中最小的元素将它与未排序元素的第一个元素交换

找到最小元素1
![selectionSort1](img/selectionSort1.png)
与第一个元素8交换
![selectionSort2](img/selectionSort2.png)
找到最小元素2
![selectionSort3](img/selectionSort3.png)
与第一个元素6交换
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

## 插入排序

遍历所有元素, 将遍历到的元素放到正确的位置

首先遍历到8, 由于在8之前没有元素, 继续下一步
![insertionSort1](img/insertionSort1.png)
接着遍历到6
![insertionSort2](img/insertionSort2.png)
由于6比8小, 所以将8向后移动
![insertionSort3](img/insertionSort3.png)
将6放到8原来的位置(正确的位置), 前两个元素排好序了, 继续下一步
![insertionSort4](img/insertionSort4.png)
接着遍历到2
![insertionSort5](img/insertionSort5.png)
由于2比8小, 所以将8向后移动
![insertionSort6](img/insertionSort6.png)
由于2比6小, 所以将6向后移动
![insertionSort7](img/insertionSort7.png)
将2放到6原来的位置(正确的位置), 前三个元素排好序了, 继续下一步
![insertionSort8](img/insertionSort8.png)

```
/**
 * 插入排序
 */
public void sort(Comparable[] array) {
    // 遍历元素
    for (int i = 1; i < array.length; i++) {
        // 将当前遍历到的元素array[i]提取出来
        Comparable item = array[i];
        // 寻找array[i]合适的插入位置
        // j保存元素item应该插入的位置
        int j;
        for (j = i; j > 0; j--) {
            if (item.compareTo(array[j - 1]) < 0) {
                array[j] = array[j - 1];
            } else {
                break;
            }
        }
        // 将item插入j的位置
        array[j] = item;
    }
}
```
