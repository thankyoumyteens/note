# 位运算

左移 n 位相当于乘 2^n。右移 n 位相当于除 2^n。

## 取出一个数指定位的值

```cpp
#include <iostream>

// 取出0x12345678中的0x1
int main() {
    long a = 0x12345678;

    long b = a & 0xF0000000;
    // 0x10000000
    std::cout << std::hex << b << std::endl;
    b = b >> (4 * 7);
    // 0x1
    std::cout << std::hex << b << std::endl;
    return 0;
}
```

## 两个数拼在一起

```cpp
#include <iostream>

int main() {
    long a = 0x1234;
    long b = 0x5678;
    long c = (a << 16) | b;
    // 0x12345678
    std::cout << std::hex << c << std::endl;
    return 0;
}
```
