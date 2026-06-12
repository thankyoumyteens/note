# 解题思路

暴力解是两层循环比较所有数字，时间复杂度是 `O(n²)`。

优化思路是：

```text
用 HashSet 记录已经见过的数字。
每次遍历到一个 num，就判断它是否已经在 set 里。
如果在，说明重复。
如果不在，就加入 set。
```

核心变量：

```text
set：保存已经出现过的数字
num：当前正在检查的数字
```

关键顺序：

```text
先 contains 判断
再 add 当前数字
```

## Java 模板

```java
import java.util.HashSet;
import java.util.Set;

class Solution {
    public boolean containsDuplicate(int[] nums) {
        // set 用来记录已经出现过的数字
        Set<Integer> set = new HashSet<>();

        for (int num : nums) {
            // 如果当前数字已经出现过，说明存在重复元素
            if (set.contains(num)) {
                return true;
            }

            // 当前数字第一次出现，加入 set
            set.add(num);
        }

        // 遍历结束都没有发现重复
        return false;
    }
}
```

复杂度：

```text
Time: O(n)
Space: O(n)
```

## 典型题目讲解

例子：

```text
nums = [1, 2, 3, 1]
```

过程：

```text
看到 1，set 没有，加入 set
看到 2，set 没有，加入 set
看到 3，set 没有，加入 set
再次看到 1，set 已经有 1，返回 true
```

如果是：

```text
nums = [1, 2, 3, 4]
```

每个数字都是第一次出现，最后返回：

```text
false
```

这题的核心不是代码，而是判断：

```text
只问“有没有出现过” -> HashSet
需要下标 / 次数 / 映射关系 -> HashMap
```

## 常见边界条件

```text
空数组 -> false
数组长度为 1 -> false
所有元素都不重复 -> false
所有元素都相同 -> true
包含负数 -> 正常处理
包含 0 -> 正常处理
```

## 英文面试表达模板

```text
I use a hash set to store the numbers I have already seen.

For each number, I check whether it already exists in the set.

If it exists, that means we found a duplicate, so I return true.

Otherwise, I add the number to the set.

The time complexity is O(n), and the space complexity is O(n).
```
