# malloc

`malloc`函数是 C 语言标准库中的一部分, 它定义在头文件`stdlib.h`中。这个函数用于动态分配内存, 它允许分配的内存大小是运行时确定的, 而不是在编译时就确定。`malloc`返回的内存块在开始时不会被初始化, 它的初始内容是未定义的。

## 函数定义

```c
void* malloc(size_t size);
```

## 参数

- `size`: 需要分配的内存大小, 以字节为单位。这个参数必须是一个`size_t`类型的值, `size_t`是一个无符号整数类型, 足以表示可分配的内存大小

## 返回值

- 如果分配成功, 会返回一个指向分配的内存地址的指针
- 如果分配失败, 会返回`nullptr`

## 释放内存

在 C/C++ 中, 没有自动的垃圾回收机制, 所以需要在适当的时候使用`free`函数来释放这块内存, 避免内存泄漏。例如: 

```cpp
free(p);
```

在释放内存后, 你应该将指针设置为`nullptr`, 避免悬挂指针(dangling pointer)问题: 

```cpp
array = nullptr;
```

## 使用示例

```cpp
#include <iostream>
#include <cstdlib>

int main() {
    size_t int_count = 0;
    size_t int_size = sizeof(int);
    std::cin >> int_count;
    int *p = (int *) malloc(int_count * int_size);
    if (p == nullptr) {
        std::cout << "内存分配失败" << std::endl;
        return 1;
    }
    if (int_count >= 2) {
        p[0] = 100;
        p[1] = 200;
        std::cout << p[0] << " " << p[1] << std::endl;
    }
    free(p);
    p = nullptr;
    return 0;
}
```
