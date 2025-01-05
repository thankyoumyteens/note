# new

new 底层是用 malloc 实现的, 不同的是, C++的 new 操作符不仅分配内存, 还会调用构造函数来初始化对象。

```cpp
Foo *p1 = (Foo *) malloc(sizeof(Foo));
Foo *p2 = new Foo();
```

执行这些代码行后, p1 和 p2 将指向堆中足以保存 Foo 对象的内存区域。通过这两个指针可访问 Foo 的数据成员和方法。不同之处在于, p1 指向的 Foo 对象不是一个正常的对象, 因为这个对象从未构建。malloc 函数只负责留出一块一定大小的内存。它不知道或关心对象本身。相反, 调用 new 不仅会分配正确大小的内存, 还会调用相应的构造函数以构建对象。

如果内存分配失败, new 会抛出一个`std::bad_alloc`异常, 而不是返回 nullptr。

## 释放内存

使用 new 创建的对象需要使用 delete 操作符来释放内存。

类似地, 使用 free 函数时, 不会调用对象的析构函数。使用 delete 时, 将调用析构函数来清理对象。

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
    myObject = nullptr;

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
