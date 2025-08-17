# 常见的算法时间复杂度

O(1) < O(logn) < O(&#8730;n) < O(n) < O(nlogn) < O(n<sup>2</sup>) < O(2<sup>n</sup>) < O(n!)

## 线性查找

```java
for (int i = 0; i < data.length; i++)
    if (data[i].equals(target))
        return i;
```

时间复杂度是 O(n)

## 一个数组中的元素可以组成哪些数据对

```java
for (int i = 0; i < data.length; i++)
    for (int j = i + 1; j < data.length; j++)
        // 获得一个数据对: (data[i], data[j])
```

时间复杂度是 O(n<sup>2</sup>)

## 遍历一个 n × n 的二维数组

```java
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        // 遍历到 arr[i][j]
```

时间复杂度是 O(n<sup>2</sup>)

## 遍历一个 a × a 的二维数组, 且 a × a = n

注意: 要明确 n 是哪个

```java
for (int i = 0; i < a; i++)
    for (int j = 0; j < a; j++)
        // 遍历到 arr[i][j]
```

时间复杂度是 O(a<sup>2</sup>) = O(n)

## 数字 n 的二进制位数

十进制转二进制: 除 2 取余

```java
while(n != 0) {
    // 得到的余数就是二进制中的一个位
    b = n % 2;
    n = n / 2;
}
```

时间复杂度是 O(log<sub>2</sub>n) = O(logn)

由于 while 循环每次前进 `n / 2` 步, 所以需要 log<sub>2</sub>n 次循环 n 才能变为 0

## 数字 n 的十进制位数

```java
while(n != 0) {
    // 得到的余数就是十进制中的一个位
    b = n % 10;
    n = n / 10;
}
```

时间复杂度是 O(log<sub>10</sub>n) = O(logn)

由于 while 循环每次前进 `n / 10` 步, 所以需要 log<sub>10</sub>n 次循环 n 才能变为 0

## 数字 n 的所有约数

约数: 如果 x 是 n 的约数, 就表示 n % x == 0

```java
for (int i = 1; i <= n; i++)
    if (n % i == 0)
        // i是n的一个约数
```

时间复杂度是 O(n)

### 优化

由于 2 × 5 = 10, 在求出 2 的同时, 就已经得到了另一个约数 5, 所以不需要遍历 n 次

```java
for (int i = 1; i * i <= n; i++)
    if (n % i == 0)
        // i和n/i是n的两个约数
```

时间复杂度是 O(&#8730;n)

## 长度为 n 的二进制数字

时间复杂度是 O(2<sup>n</sup>)

## 长度为 n 的数组的所有排列

时间复杂度是 O(n!)

## 判断数字 n 是不是偶数

```java
return n % 2 == 0;
```

时间复杂度是 O(1)
