# 实现选择排序

```java
public class SelectionSort {

    /**
     * 选择排序
     */
    public static void sort(int[] data) {
        // data[i...n) 是没有排序的
        // data[0...i) 是排好序的
        for (int i = 0; i < data.length; i++) {
            // data[i..data.length)范围内最小值的索引
            int minIndex = i;
            for (int j = i; j < data.length; j++) {
                if (data[j] < data[minIndex]) {
                    minIndex = j;
                }
            }
            // 交换data[i]和data[minIndex]
            swap(data, i, minIndex);
        }
    }

    /**
     * 交换数组data中索引为i和j的元素
     */
    private static void swap(int[] data, int i, int j) {
        int temp = data[i];
        data[i] = data[j];
        data[j] = temp;
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
