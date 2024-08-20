# 两个数拼在一起

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
