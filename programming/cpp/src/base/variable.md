# 变量

定义变量的两种方式:

1. `类型 变量名 = 初始值`
2. `类型 变量名{初始值}`

```cpp
#include <iostream>

int main() {
    int a = 10;
    int b{10};

    std::cout << "a = " << a << std::endl;
    std::cout << "b = " << b << std::endl;
    return 0;
}
```
