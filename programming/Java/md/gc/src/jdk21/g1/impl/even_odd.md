# 判断奇偶

奇数的二进制最低位都是 1, 偶数都是 0。

```cpp
#include <iostream>

int main() {
    int a = 999;

    // 是否奇数
    bool is_odd = (a & 1) == 1;
    std::cout << is_odd << std::endl;

    // 是否偶数
    bool is_even = (a & 1) == 0;
    std::cout << is_even << std::endl;

    return 0;
}
```
