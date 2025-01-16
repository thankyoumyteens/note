# 静态局部变量

静态局部变量(简称静态变量)的生命周期和程序相同, 但作用域是局部的。

```cpp
#include <iostream>

void f1() {
    // 这行代码只会被执行一次
    // 静态局部变量默认会被初始化为0
    static int a;
    std::cout << a++ << std::endl;
}

int main() {
    f1(); // 0
    f1(); // 1
    f1(); // 2

    // 报错, 外部无法访问
    std::cout << a++ << std::endl;
    return 0;
}
```
