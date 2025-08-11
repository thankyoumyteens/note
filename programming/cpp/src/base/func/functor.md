# 仿函数

仿函数（Functor）是一种实现了 `operator()` 的类或结构体，使得该类的对象可以像函数一样被调用。仿函数结合了函数的灵活性和类的封装性，常用于 STL 算法、回调函数等场景。

```cpp
#include <iostream>

// 基本仿函数
struct Adder {
    // 重载()运算符
    int operator()(int a, int b) const {
        return a + b;
    }
};

int main() {
    Adder add;
    // 像函数一样调用
    std::cout << "1 + 1 = " << add(1, 1) << std::endl;
    // 临时对象调用
    std::cout << "10 + 10 = " << Adder()(10, 10) << std::endl;

    return 0;
}
```
