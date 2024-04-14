# new

在 C++中, `new`关键字是一种用于动态内存分配的操作符, 它允许程序在运行时分配和构造对象。`new`底层是用`malloc`实现的, 不同的是, C++的`new`操作符不仅分配内存, 还会调用构造函数来初始化对象。

`new`的基本用法如下: 

```cpp
type *pointer = new type(args...);
```

这里, `type`是要创建的对象的类型, `pointer`是一个指向新分配并初始化的对象的指针, `args...`是传递给对象构造函数的参数列表。

如果内存分配失败, `new`会抛出一个`std::bad_alloc`异常, 而不是返回`nullptr`。

## 释放内存

使用`new`创建的对象需要使用`delete`操作符来释放内存。

如果使用`new[]`创建了一个数组, 应该使用`delete[]`来释放它。

## 使用示例

```cpp
#include <iostream>

int main() {
    // 分配内存并调用构造函数
    MyClass *myObject = new MyClass("ok");
    std::cout << "Value: " << myObject->val << std::endl;
    // 释放内存
    delete myObject;

    size_t int_count = 0;
    std::cin >> int_count;
    // 分配数组
    int *p = new int[int_count];

    if (int_count >= 2) {
        p[0] = 100;
        p[1] = 200;
        std::cout << p[0] << " " << p[1] << std::endl;
    }
    // 释放内存
    delete[] p;
    p = nullptr;
    return 0;
}
```
