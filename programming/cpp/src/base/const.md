# 常量

定义常量的两种方式:

1. `类型 常量名 = 初始值`
2. `类型 常量名{初始值}`

```cpp
#include <iostream>

int main() {
    const int a = 10;
    const int b{10};

    std::cout << "a = " << a << std::endl;
    std::cout << "b = " << b << std::endl;
    return 0;
}
```
