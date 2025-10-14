# 实现快速排序

```java
public class QuickSort {

    /**
     * 交换数组data中索引为i和j的元素
     */
    private static void swap(int[] data, int i, int j) {
        int temp = data[i];
        data[i] = data[j];
        data[j] = temp;
    }

    private static void partition(int[] data, int left, int right) {
        if (left >= right) {
            return;
        }
        int pivot = left;
        int i = pivot + 1;
        int j = pivot;
        while (i <= right) {
            if (data[i] > data[pivot]) {
                // 如果arr[i] > arr[pivot], 直接i++就可以了
                i++;
            } else {
                // 如果arr[i] < arr[pivot]
                // 交换arr[j+1]和arr[i]
                swap(data, j + 1, i);
                j++;
                i++;
            }
        }
        // 交换arr[pivot]和arr[j], 让基准值落在正确的位置
        swap(data, pivot, j);
        // 此时j指向的元素就是基准值, 它的左边都是小于等于它的元素, 右边都是大于它的元素

        // 递归排序arr[left...j-1]和arr[j+1...right]
        partition(data, left, j - 1);
        partition(data, j + 1, right);
    }

    /**
     * 快速排序
     *
     * @param data 待排序的数组
     */
    public static void sort(int[] data) {
        partition(data, 0, data.length - 1);
    }

    /**
     * 测试方法
     */
    public static void main(String[] args) {
        int[] data = {6, 4, 2, 3, 1, 5};
        sort(data);
        for (int datum : data) {
            System.out.print(datum + " ");
        }
    }
}
```
