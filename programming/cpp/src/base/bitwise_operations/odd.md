# 使用位运算判断一个数是奇数还是偶数

在计算机科学中, 可以使用位运算（bitwise operations）来判断一个整数是奇数还是偶数。对于任何整数 n, 我们可以使用以下性质: 

- 如果 n 是奇数, 那么 n 的二进制表示中最右边的一位（即最低有效位, LSB）是 1
- 如果 n 是偶数, 那么 n 的二进制表示中最右边的一位是 0

基于这个性质, 我们可以使用位运算 `AND`（与）来检测 n 的最低有效位。在大多数编程语言中, `AND` 运算符通常表示为 `&`。当我们将 n 与数字 1 进行 `AND` 运算时, 如果结果为 1, 则 n 是奇数；如果结果为 0, 则 n 是偶数。

以下是使用位运算判断奇数和偶数的 C 语言示例代码: 

```c
#include <stdio.h>

int isOdd(int n) {
    return n & 1; // 如果 n 是奇数, 返回 1；如果是偶数, 返回 0
}

int main() {
    int number;
    printf("Enter an integer: ");
    scanf("%d", &number);

    if (isOdd(number)) {
        printf("%d is an odd number.\n", number);
    } else {
        printf("%d is an even number.\n", number);
    }

    return 0;
}
```
