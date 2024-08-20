# 取出一个数指定位的值

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
