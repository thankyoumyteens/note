# 传递指针类型

传递指针类型时会出现问题

```cpp
#include <iostream>

template<typename T>
T max(T a, T b) {
    // 如果a和b是指针, 则比较的是指针存储的地址而不是值
    return a > b ? a : b;
}

int main(int argc, char *argv[]) {
    int a = 100;
    int b = 2;
    // 结果不对
    int *r1 = max(&a, &b);
    std::cout << "result: " << *r1 << std::endl;
    return 0;
}
```

## 使用函数重载解决

```cpp
#include <iostream>

template<typename T>
T max(T a, T b) {
    return a > b ? a : b;
}
template<typename T>
T max(T *a, T *b) {
    return *a > *b ? *a : *b;
}

int main(int argc, char *argv[]) {
    int a = 100;
    int b = 2;
    int r1 = max(&a, &b);
    std::cout << "result: " << r1 << std::endl;
    int r2 = max(a, b);
    std::cout << "result: " << r2 << std::endl;
    return 0;
}
```
