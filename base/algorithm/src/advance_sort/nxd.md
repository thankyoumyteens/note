# 数组中逆序对的总数

[LCR 170. 交易逆序对的总数](https://leetcode.cn/problems/shu-zu-zhong-de-ni-xu-dui-lcof/description/)

在股票交易中，如果前一天的股价高于后一天的股价，则可以认为存在一个「交易逆序对」。请设计一个程序，输入一段时间内的股票交易记录 record，返回其中存在的「交易逆序对」总数。

示例 1：

```
输入：record = [9, 7, 5, 4, 6]
输出：8
解释：交易中的逆序对为 (9, 7), (9, 5), (9, 4), (9, 6), (7, 5), (7, 4), (7, 6), (5, 4)。
```

提示：

1. `0 <= record.length <= 50000`

归并排序的核心是 “分治”：将数组分成两半，分别排序后合并。在合并过程中，可以同步统计逆序对的数量，无需额外遍历数组。

具体步骤：

1. 拆分：将数组递归拆分为左右两个子数组，直到子数组长度为 1。拆分的目标是将原数组分解为最小单位（长度为 1 的子数组），因为长度为 1 的数组不存在逆序对
2. 合并与统计：合并两个已排序的子数组时，若左子数组元素大于右子数组元素，则左子数组当前位置及之后的所有元素都与右子数组当前元素构成逆序对，累加统计即可

合并时统计逆序对的原理：

- 设 left 是左子数组（已排序），right 是右子数组（已排序）
- 用指针 i 遍历 left，指针 j 遍历 right
- 当 `left[i]` > `right[j]` 时
  - 由于 left 已排序，`left[i]` 之后的所有元素(`left[i+1]`, `left[i+2]`, ...)都大于 `left[i]`，因此它们也必然大于 `right[j]`
  - 所以，`right[j]` 与 `left[i]` 及其之后的所有元素构成逆序对，逆序对数量为 `left.length - i`(left 剩余元素的个数)

```java
public class ReversePairs {

    // 用于辅助合并操作的临时数组
    private static int[] temp;

    public static int reversePairs(int[] record) {
        if (record == null || record.length <= 1) {
            return 0; // 空数组或单个元素数组无逆序对
        }
        temp = new int[record.length]; // 初始化临时数组
        return mergeSortAndCount(record, 0, record.length - 1);
    }

    /**
     * 归并排序并统计逆序对
     *
     * @param arr   待排序数组
     * @param left  左边界索引
     * @param right 右边界索引
     * @return 逆序对总数
     */
    private static int mergeSortAndCount(int[] arr, int left, int right) {
        if (left >= right) {
            return 0; // 单个元素或空区间，无逆序对
        }

        // 拆分：递归处理左右子数组
        int mid = left + (right - left) / 2; // 避免整数溢出
        int countLeft = mergeSortAndCount(arr, left, mid); // 左子数组内部逆序对
        int countRight = mergeSortAndCount(arr, mid + 1, right); // 右子数组内部逆序对

        // 合并：统计跨左右子数组的逆序对
        int countCross = mergeAndCount(arr, left, mid, right);

        // 总逆序对 = 左内部 + 右内部 + 跨数组
        return countLeft + countRight + countCross;
    }

    /**
     * 合并两个已排序子数组，并统计跨数组的逆序对
     *
     * @param arr   原数组
     * @param left  左子数组起始索引
     * @param mid   左子数组结束索引（右子数组起始索引为mid+1）
     * @param right 右子数组结束索引
     * @return 跨数组的逆序对数量
     */
    private static int mergeAndCount(int[] arr, int left, int mid, int right) {
        int i = left; // 左子数组指针
        int j = mid + 1; // 右子数组指针
        int k = left; // 临时数组指针
        int count = 0; // 跨数组逆序对计数器

        // 合并两个子数组，同时统计逆序对
        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                // 左元素 <= 右元素，无逆序对，直接放入临时数组
                temp[k++] = arr[i++];
            } else {
                // 左元素 > 右元素，左子数组剩余元素均与当前右元素构成逆序对
                temp[k++] = arr[j++];
                // 逆序对数量 = 左子数组剩余元素个数（mid - i + 1）
                count += mid - i + 1;
            }
        }

        // 处理左子数组剩余元素
        while (i <= mid) {
            temp[k++] = arr[i++];
        }

        // 处理右子数组剩余元素
        while (j <= right) {
            temp[k++] = arr[j++];
        }

        // 将临时数组中的有序元素复制回原数组
        for (k = left; k <= right; k++) {
            arr[k] = temp[k];
        }

        return count;
    }

    /**
     * 测试逆序对算法
     */
    public static void main(String[] args) {
        // 创建测试用例
        int[][] testCases = {
                {3, 2, 1},          // 预期结果：3
                {7, 5, 6, 4},       // 预期结果：5
                {1, 2, 3, 4, 5},    // 预期结果：0（无逆序对）
                {5, 4, 3, 2, 1},    // 预期结果：10
                {},                 // 预期结果：0（空数组）
                {1},                // 预期结果：0（单个元素）
                {2, 4, 3, 5, 1}     // 预期结果：5
        };

        // 遍历测试用例并输出结果
        for (int[] arr : testCases) {
            int result = reversePairs(arr);
            System.out.printf("逆序对总数=%d%n", result);
        }
    }
}
```
