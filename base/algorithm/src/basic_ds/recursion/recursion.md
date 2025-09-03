# 递归

递归本质上是把原来的问题转化成更小的同一类问题。

示例: 数组求和 `sum(arr[0...n-1])`

1. `sum(arr[0...n-1]) = arr[0] + sum(arr[1...n-1])`
   - `sum(arr[1...n-1])` 就是相比 `sum(arr[0...n-1])` 更小一些的同一类问题
2. `sum(arr[1...n-1]) = arr[1] + sum(arr[2...n-1])`
   - `sum(arr[2...n-1])` 也是相比 `sum(arr[1...n-1])` 更小一些的同一类问题
3. 以此类推...
4. `sum(arr[n-1...n-1]) = arr[n-1] + sum([])`
   - `sum([])` 是最基本的问题, 它值是 0
   - 此时, 结合上面的一系列式子, 就可以得到 `sum(arr[0...n-1])` 的结果

所有递归算法都包含两部分:

1. 求解最基本的问题
2. 把原问题转化成更小的问题

```java
private static int doSum(int[] arr, int startIndex) {
    // 求解最基本的问题
    if (startIndex == arr.length) {
        return 0;
    }
    // 把原问题转化成更小的问题
    return arr[startIndex] + doSum(arr, startIndex + 1);
}

public static int sum(int[] arr) {
    return doSum(arr, 0);
}
```
