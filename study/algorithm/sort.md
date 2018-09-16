# 排序(从小到大)

- <a href="#selectionSort">选择排序</a>
- <a href="#insertionSort">插入排序</a>
- <a href="#mergeSort">归并排序</a>
- <a href="#quickSort">快速排序</a>

<a id="selectionSort"></a>
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

<a id="insertionSort"></a>
## 插入排序

遍历所有元素, 将遍历到的元素放到正确的位置

首先遍历到8, 由于在8之前没有元素, 继续下一步
![insertionSort1](img/insertionSort1.PNG)
接着遍历到6
![insertionSort2](img/insertionSort2.PNG)
由于6比8小, 所以将8向后移动
![insertionSort3](img/insertionSort3.PNG)
将6放到8原来的位置(正确的位置), 前两个元素排好序了, 继续下一步
![insertionSort4](img/insertionSort4.PNG)
接着遍历到2
![insertionSort5](img/insertionSort5.PNG)
由于2比8小, 所以将8向后移动
![insertionSort6](img/insertionSort6.PNG)
由于2比6小, 所以将6向后移动
![insertionSort7](img/insertionSort7.PNG)
将2放到6原来的位置(正确的位置), 前三个元素排好序了, 继续下一步
![insertionSort8](img/insertionSort8.PNG)

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

<a id="mergeSort"></a>
## 归并排序

将素组不断二分, 直到每个数组长度为1,
再将分开的数组不断合并, 合并过程中排序

![](img/mergeSort.png)

### 合并过程

创建待排序数组的副本,
建立3个索引i,j,k

![](img/mergeSort02.PNG)

比较i和j元素的大小,j指向的值小

![](img/mergeSort03.PNG)

将j指向的值覆盖原数组k指向的值,
k右移,j右移,i保持不变

![](img/mergeSort04.PNG)

比较i和j元素的大小,i指向的值小

![](img/mergeSort05.PNG)

将i指向的值覆盖原数组k指向的值,
k右移,i右移,j保持不变

![](img/mergeSort06.png)

```
/**
 * 归并, 合并
 * 将arr[l...mid]和arr[mid+1...r]两部分进行归并
 *
 * @param l   left
 * @param mid middle
 * @param r   right
 */
private static void merge(Comparable[] arr, int l, int mid, int r) {
    Comparable[] aux = Arrays.copyOfRange(arr, l, r + 1);
    // 初始化, i指向左半部分的起始索引位置l
    // j指向右半部分起始索引位置mid + 1
    int i = l;
    int j = mid + 1;
    for (int k = l; k <= r; k++) {
        if (i > mid) {
            // 左半部分元素已经全部处理完毕
            arr[k] = aux[j - l];
            j++;
        } else if (j > r) {
            // 右半部分元素已经全部处理完毕
            arr[k] = aux[i - l];
            i++;
        } else if (aux[i - l].compareTo(aux[j - l]) < 0) {
            // 左半部分所指元素 < 右半部分所指元素
            arr[k] = aux[i - l];
            i++;
        } else {
            // 左半部分所指元素 >= 右半部分所指元素
            arr[k] = aux[j - l];
            j++;
        }
    }
}

/**
 * 将数组二分
 * 递归使用归并排序,对arr[l...r]的范围进行排序
 */
private static void mergeSort(Comparable[] arr, int l, int r) {
    if (l >= r)
        return;

    int mid = (l + r) / 2;
    mergeSort(arr, l, mid);
    mergeSort(arr, mid + 1, r);
    merge(arr, l, mid, r);
}

/**
 * 归并排序
 */
@Override
public void sort(Comparable[] array) {
    mergeSort(array, 0, array.length - 1);
}
```

<a id="quickSort"></a>
## 快速排序

选中第一个元素4, 调整数组使得4左边的元素小于4,
右边的元素大于4

以4分割原数组为左右两个数组, 继续执行上面的操作,
直到操作后的子数组长度小于等于1

左: 选中2, 调整数组\[2, 3, 1\], 操作结束后,
左右数组长度为1, 不再继续操作

右: 选中6, 调整数组\[, 6, 5, 7, 8\],
操作结束后, 左数组长度为1, 不再继续操作,
右数组继续执行上面的操作

![](img/quickSort.png)

### 使元素v左边的元素小于v, v右边的元素大于v的操作(分割操作)

选择第一个元素分割数组在特殊情况会变成O(n^2),

比如原数组已经使升序排好序的状态,
每次分割后左数组为空, 右数组为上一层数组长度减1,

这时可以随机选择一个元素, 把它与第一个元素交换

![](img/quickSort01.PNG)

将e与v比较, 如果e大于v, 则i+1

![](img/quickSort02.PNG)

如果e小于v, 则交换arr\[i\]和arr\[j\], 再j+1

![](img/quickSort03.PNG)

处理后

![](img/quickSort04.PNG)

最后将v与arr\[j\]交换

![](img/quickSort05.PNG)

```
/**
 * 对arr[l...r]部分进行partition操作
 * 返回p, 使得arr[l...p-1] < arr[p] ; arr[p+1...r] > arr[p]
 */
private static int partition(Comparable[] arr, int l, int r) {
    Comparable v = arr[l];

    int j = l;
    // 调整数组, 使得: arr[l+1...j] < v, arr[j+1...i-1] > v
    for (int i = l + 1; i <= r; i++)
        if (arr[i].compareTo(v) < 0) {
            j++;
            ArrayUtil.swap(arr, j, i);
        }
    ArrayUtil.swap(arr, l, j);

    return j;
}

/**
 * 递归使用快速排序,对arr[l...r]的范围进行排序
 */
private static void quickSort(Comparable[] arr, int l, int r) {
    // 数组长度<=1
    if (l >= r)
        return;

    int p = partition(arr, l, r);
    quickSort(arr, l, p - 1);
    quickSort(arr, p + 1, r);
}

/**
 * 快速排序
 */
@Override
public void sort(Comparable[] array) {
    quickSort(array, 0, array.length - 1);
}
```

## 三路快速排序(快速排序优化)

将数组分割成3部分: 小于v, 等于v, 大于v

## 分割过程

![](img/qS3_1.PNG)

e等于v

无操作, i++

![](img/qS3_2.PNG)

e小于v

将arr\[i\]和arr\[lt+1\]交换, i++, lt++

![](img/qS3_4.PNG)

e大于v

将arr\[i\]和arr\[gt-1\]交换, i不变, gt--

![](img/qS3_5.PNG)

处理完成后

![](img/qS3_6.PNG)

将arr\[l\]和arr\[lt\]交换

![](img/qS3_7.PNG)

```
/**
 * 递归使用快速排序, 对arr[l...r]的范围进行排序
 */
private static void quickSsort(Comparable[] arr, int l, int r) {

    // 对于小规模数组, 使用插入排序
    if (r - l <= 15) {
        InsertionSort.sort(arr, l, r);
        return;
    }

    // 随机在arr[l...r]的范围中, 选择一个数值作为标定点pivot
    ArrayUtil.swap(arr, l, (int) (Math.random() * (r - l + 1)) + l);

    Comparable v = arr[l];

    // arr[l+1...lt] < v
    int lt = l;
    // arr[gt...r] > v
    int gt = r + 1;
    // arr[lt+1...i) == v
    int i = l + 1;

    while (i < gt) {
        if (arr[i].compareTo(v) < 0) {
            ArrayUtil.swap(arr, i, lt + 1);
            i++;
            lt++;
        } else if (arr[i].compareTo(v) > 0) {
            ArrayUtil.swap(arr, i, gt - 1);
            gt--;
        } else { // arr[i] == v
            i++;
        }
    }

    ArrayUtil.swap(arr, l, lt);

    quickSsort(arr, l, lt - 1);
    quickSsort(arr, gt, r);
}

/**
 * 快速排序
 */
@Override
public void sort(Comparable[] array) {
    quickSsort(array, 0, array.length - 1);
}
```
