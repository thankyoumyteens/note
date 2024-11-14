# 结构化绑定

C++17 引入了结构化绑定(structured bindings)的概念，允许声明多个变量，这些变量使用数组、结构体、pair 或元组中的元素来初始化。

注意，必须为结构化绑定使用 auto 关键字。

## 使用数组初始化变量

```cpp
#include <iostream>

int main() {
    int arr[] = {1, 2, 3};
    auto [a, b, c] = arr;

    std::cout << a << std::endl; // 1
    std::cout << b << std::endl; // 2
    std::cout << c << std::endl; // 3
    return 0;
}
```

## 使用结构体初始化变量

```cpp
#include <iostream>

struct Demo {
    int x;
    int y;
    int z;
};

int main() {
    Demo demo;
    demo.x = 1;
    demo.y = 2;
    demo.z = 3;

    auto [a, b, c] = demo;

    std::cout << a << std::endl; // 1
    std::cout << b << std::endl; // 2
    std::cout << c << std::endl; // 3
    return 0;
}
```
