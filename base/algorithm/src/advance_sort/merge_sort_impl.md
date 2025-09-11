# 实现归并排序

```java
import java.util.Arrays;

public class MergeSort {

    public static void sort(int[] data) {
        mergeSort(data, 0, data.length - 1);
    }

    private static void mergeSort(int[] data, int left, int right) {
        // 求解最基本的问题
        if (left >= right) {
            return;
        }
        // 把原问题转化成更小的问题

        // 拆分
        int mid = (left + right) / 2;
        mergeSort(data, left, mid);
        mergeSort(data, mid + 1, right);
        // 合并
        merge(data, left, mid, right);
    }

    /**
     * 合并
     */
    private static void merge(int[] data, int left, int mid, int right) {
        // 把data[left...mid]和data[mid+1...right]复制到临时数组中
        int[] temp = Arrays.copyOfRange(data, left, right + 1);

        int i = left;
        int j = mid + 1;
        int k = left; // 指向原数组的元素
        for (; k < right + 1; k++) {
            // 注意: temp数组的索引是从0开始的, 而data的索引是从left开始的
            // 所以：使用i、j索引访问temp数组的元素时需要减去left
            if (i > mid) {
                // 如果：左边的数组已经遍历完了，就只需要复制右边的数组
                data[k] = temp[j - left];
                j++;
            } else if (j > right) {
                // 如果：右边的数组已经遍历完了，就只需要复制左边的数组
                data[k] = temp[i - left];
                i++;
            } else if (temp[i - left] < temp[j - left]) {
                // 如果：data[i] < data[j]，就把data[i]复制到原数组中
                data[k] = temp[i - left];
                i++;
            } else {
                // 如果：data[i] >= data[j]，就把data[j]复制到原数组中
                data[k] = temp[j - left];
                j++;
            }
        }
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
