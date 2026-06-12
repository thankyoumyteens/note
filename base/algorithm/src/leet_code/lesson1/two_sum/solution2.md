# HashMap 优化思路

暴力解是两层循环，固定一个数 nums[i]，再去找另一个数，复杂度是 O(n²)。

优化点在于：

```text
对当前数字 nums[i]，
另一个数其实已经确定了：target - nums[i]
```

所以问题变成：

```
如何快速判断 need = target - nums[i] 是否在之前出现过？
```

答案是用 HashMap。

HashMap 设计：

```text
key：已经见过的数字
value：这个数字的下标
```

遍历数组时，每一轮做三件事：

```
1. 计算 need = target - nums[i]
2. 如果 map 里有 need，说明找到答案，返回 [map.get(need), i]
3. 如果没有，把当前 nums[i] 和下标 i 放进 map
```

模板：

```java
Map<Integer, Integer> map = new HashMap<>();

for (int i = 0; i < nums.length; i++) {
    int need = target - nums[i];

    if (map.containsKey(need)) {
        return new int[]{map.get(need), i};
    }

    map.put(nums[i], i);
}
```

完整代码：

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];

            if (map.containsKey(need)) {
                return new int[]{map.get(need), i};
            }

            map.put(nums[i], i);
        }

        return new int[0];
    }
}
```

## 为什么先查再放？

错误写法：

```java
map.put(nums[i], i);

if (map.containsKey(target - nums[i])) {
    return new int[]{map.get(target - nums[i]), i};
}
```

问题：

```text
可能把当前元素自己用两次。
```

例如：

```text
nums = [3, 2, 4]
target = 6
```

当 i = 0：

```text
nums[i] = 3
need = 3
```

如果先 put，再查，就会查到自己，错误返回 `[0, 0]`。

所以 Two Sum 标准顺序是：

```text
先查 need
再放当前 nums[i]
```

## 英文面试表达

```text
I will use a hash map to store the numbers I have already seen and their indices.

For each number, I calculate its complement, which is target minus the current number.

If the complement already exists in the map, I return the index of the complement and the current index.

Otherwise, I store the current number and its index in the map.

This reduces the time complexity from O(n squared) to O(n).
```

复杂度表达：

```text
Time complexity is O(n), because we scan the array once.
Space complexity is O(n), because we may store up to n elements in the hash map.
```
