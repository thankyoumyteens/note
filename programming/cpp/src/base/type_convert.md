# 类型转换

C++提供了三种方法来显式地转换变量类型。

```cpp
#include <iostream>

int main() {
    double a = 3.14;
    int b;
    // 方法1
    b = (int) a;
    // 方法2
    b = int(a);
    // 方法3
    b = static_cast<int>(a);
    std::cout << b << std::endl;
    return 0;
}
```
