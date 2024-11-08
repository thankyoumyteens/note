# decltype

C++11 标准引入类型说明符 decltype，它的作用是选择并返回操作数的数据类型。在此过程中，编译器分析表达式并得到它的类型，却不实际计算表达式的值。比如 `decltype(func1()) sum = a;` sum 的类型就是函数 func1 的返回值类型。

如果 decltype 使用的表达式是一个变量，则 decltype 返回该变量的类型:

```cpp
#include <iostream>

int main(int argc, char *argv[]) {
    const int a = 10;
    const int &b = a;

    // c的类型是 const int &
    decltype(b) c = a;

    // d的类型是 const int
    decltype(b) d = 0;

    // e的类型是 const int
    decltype(a) e = a;

    return 0;
}
```

如果 decltype 使用的表达式不是一个变量，则 decltype 返回表达式结果对应的类型:

```cpp
#include <iostream>

int main(int argc, char *argv[]) {
    const int a = 10;
    const int *p = &a;

    // c的类型是 const int *
    decltype(p) c = &a;

    // d的类型是 const int &
    decltype(*p) d = a;

    // e的类型是 int
    decltype(1 + 1) e = 100;

    return 0;
}
```
