# Two Sum

Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

给了一个数组, 还有一个结果target, 在数组中找到两个数字, 使其和为target

# 例子

```
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
```

# 解

这里只想用线性的时间复杂度来解决问题, 就是说只能遍历一个数字, 那么另一个数字呢, 可以事先将其存储起来, 使用一个HashMap, 来建立数字和其索引之间的映射, 由于HashMap是常数级的查找效率, 这样在遍历数组的时候, 用target减去遍历到的数字, 就是另一个需要的数字了, 直接在 HashMap 中查找其是否存在即可。注意要判断两个数字不能相同。

整个实现步骤为: 先遍历一遍数组, 建立HashMap, 然后再遍历一遍, 开始查找, 找到则记录index。

```java
public class Solution {
    public int[] twoSum(int[] nums, int target) {
        HashMap<Integer, Integer> m = new HashMap<Integer, Integer>();
        int[] r = new int[2];
        for (int i = 0; i < nums.length; ++i) {
            m.put(nums[i], i);
        }
        for (int i = 0; i < nums.length; ++i) {
            int t = target - nums[i];
            if (m.containsKey(t) && m.get(t) != i) {
                r[0] = i;
                r[1] = m.get(t);
                break;
            }
        }
        return res;
    }
}
```
