# 颜色分类

[75.颜色分类](https://leetcode.com/problems/sort-colors/description/)

给定一个包含红色、白色和蓝色、共 n 个元素的数组 nums，原地对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。

我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。

必须在不使用库内置的 sort 函数的情况下解决这个问题。

示例 1：

```
输入：nums = [2,0,2,1,1,0]
输出：[0,0,1,1,2,2]
```

示例 2：

```
输入：nums = [2,0,1]
输出：[0,1,2]
```

提示：

```
n == nums.length
1 <= n <= 300
nums[i] 为 0、1 或 2
```

进阶：

你能想出一个仅使用常数空间的一趟扫描算法吗？

```java
public class SortColors {

    /**
     * 交换数组data中索引为i和j的元素
     */
    private static void swap(int[] data, int i, int j) {
        int temp = data[i];
        data[i] = data[j];
        data[j] = temp;
    }

    private static void partition3(int[] data, int left, int right) {
        if (left >= right) {
            return;
        }

        // 由于只有0,1,2三种元素, 所以基准值固定为中间的值 1

        int i = left;
        int lt = -1;
        int gt = right + 1;
        // 循环不变量:
        // arr[left...lt] == 0
        // arr[lt+1...i-1] == 1
        // arr[gt...right] == 2
        while (true) {
            if (i == gt) {
                // [left, right]区间已经排序完成, 退出循环
                break;
            }
            // 如果arr[i] == arr[pivot], 直接i++就可以了
            if (data[i] == 1) {
                i++;
                continue;
            }
            // 如果arr[i] < arr[pivot], 则交换arr[lt+1]和arr[i]
            // 然后：lt++、i++
            if (data[i] < 1) {
                swap(data, lt + 1, i);
                lt++;
                i++;
                continue;
            }
            // 如果arr[i] > arr[pivot], 则交换arr[gt-1]和arr[i]
            // 然后：gt--
            if (data[i] > 1) {
                swap(data, gt - 1, i);
                gt--;
            }
        }
        // 排序完成, 不需要递归了
        // 时间复杂度为O(n)
    }

    public static void sortColors(int[] data) {
        partition3(data, 0, data.length - 1);
    }

    /**
     * 测试用例
     */
    public static void main(String[] args) {
        int[] data = {2, 0, 2, 1, 1, 0};
        sortColors(data);
        for (int datum : data) {
            System.out.print(datum + " ");
        }
    }
}
```
