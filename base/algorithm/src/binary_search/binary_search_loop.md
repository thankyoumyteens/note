# 非递归实现二分查找法

```java
public class BinarySearch {

    /**
     * 二分查找
     */
    public static int binarySearch(int[] data, int target) {
        int left = 0;
        int right = data.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (data[mid] == target) {
                // 递归结束条件: 找到目标值
                return mid;
            } else if (data[mid] > target) {
                // 如果中间值大于目标值, 则目标值在左半部分
                // 递归查找左半部分
                right = mid - 1;
            } else {
                // 如果中间值小于目标值, 则目标值在右半部分
                // 递归查找右半部分
                left = mid + 1;
            }
        }
        // 递归结束条件: 数组为空, 目标值不存在
        return -1;
    }

    /**
     * 测试方法
     */
    public static void main(String[] args) {
        int[] data = {6, 4, 2, 3, 1, 5};
        // 先对数组进行排序, 因为二分查找要求数组是有序的
        Arrays.sort(data);
        System.out.println("排序后的数组: " + Arrays.toString(data));
        // 查找目标值为3的元素
        int index = binarySearch(data, 3);
        if (index == -1) {
            System.out.println("未找到目标值");
        } else {
            System.out.println("目标值的索引为: " + index);
        }
    }
}
```
