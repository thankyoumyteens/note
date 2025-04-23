# 函数模版

```cpp
#include <iostream>

template<typename T>
T add(T a, T b) {
    return a + b;
}

int main(int argc, char *argv[]) {
    // 自动推导类型
    int r1 = add(1, 2);
    std::cout << "result: " << r1 << std::endl;

    // 手动指定类型
    auto r2 = add<double>(1, 2);
    std::cout << "result: " << r2 << std::endl;

    return 0;
}
```
