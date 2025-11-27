# 查找大于 target 的最小值

示例：在数组 `[1, 3, 5, 7, 9]` 中找到大于 2 的最小值。

查找过程：

1. 第一次循环
   1. `left=0`, `right=4`, `mid=2`, 则 `nums[mid]=5`
   2. `5 > 2`, 记录 `result=5`，并去左子数组中继续搜索
2. 第二次循环
   1. `left=0`, `right=1`, `mid=0`，则 `nums[mid]=1`
   2. `1 ≤ 2`, 不记录 result, 并去右子数组中继续搜索
3. 第三次循环
   1. `left=1`, `right=1`, `mid=1`, 则 `nums[mid]=3`
   2. `3 > 2`, 记录 `result=3`, 并去左子数组中继续搜索
4. 此时 `left > right`, 循环结束

结果: 大于 2 的最小值是 3。

```java
public class FindMinGreaterThanTarget {

    public static int findMinGreaterThanTarget(int[] data, int target) {
        int result = -1;
        int left = 0;
        int right = data.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (data[mid] > target) {
                result = mid;
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        int[] data = {1, 3, 5, 7, 9};
        int target = 2;
        int index = findMinGreaterThanTarget(data, target);
        System.out.println("最小的比目标值" + target + "大的元素为: " + data[index]);
    }
}
```
