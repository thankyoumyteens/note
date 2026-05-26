# 暴力思路

```java
for (int i = 0; i < nums.length; i++) {
    for (int j = i + 1; j < nums.length; j++) {
        if (nums[i] + nums[j] == target) {
            return new int[]{i, j};
        }
    }
}
```

问题：

```text
时间复杂度 O(n²)
每个数都要和后面的数配对
```
