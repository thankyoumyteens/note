# 常量

定义常量方式:

```cpp
#include <iostream>

int main() {
    const int a = 10;

    std::cout << "a = " << a << std::endl;
    return 0;
}
```

## 列表初始化

```cpp
#include <iostream>

int main() {
    // C++11增加
    // 类型 变量名{初始值}
    const int b{10};

    std::cout << "b = " << b << std::endl;
    return 0;
}
```

## 指向常量的指针

指向常量的指针(pointer to const)不能用于改变其所指对象的值。要想存放常量的地址，只能使用指向常量的指针:

```cpp
#include <iostream>

int main() {
    const int a = 10;
    const int *p = &a;
    *p = 20; // 报错
    std::cout << "a: " << *p << std::endl;
    return 0;
}
```

## 常量指针

常量指针(const pointer)必须初始化，而且一旦初始化完成，则它的值(也就是存放在指针中的那个地址)就不能再改变了。把\*放在 const 关键字之前用以说明指针是一个常量，即不变的是指针本身的值而非指向的那个值:

```cpp
#include <iostream>

int main() {
    int a = 10;
    int b = 20;
    int *const p = &a;
    *p = 100;
    p = &b; // 报错
    std::cout << "a: " << a << std::endl;
    return 0;
}
```
