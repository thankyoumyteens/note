# 动态内存分配

## malloc

`malloc`函数是 C 语言标准库中的一部分，它定义在头文件`stdlib.h`中。这个函数用于动态分配内存, 它允许分配的内存大小是运行时确定的，而不是在编译时就确定。`malloc`返回的内存块在开始时不会被初始化，它的初始内容是未定义的。

### 函数定义

```c
void* malloc(size_t size);
```

### 参数

- `size`：需要分配的内存大小，以字节为单位。这个参数必须是一个`size_t`类型的值，`size_t`是一个无符号整数类型，足以表示可分配的内存大小

### 返回值

- 如果分配成功，会返回一个指向分配的内存地址的指针
- 如果分配失败，会返回`nullptr`

### 释放内存

在 C/C++ 中，没有自动的垃圾回收机制，所以需要在适当的时候使用`free`函数来释放这块内存，避免内存泄漏。例如：

```cpp
free(p);
```

在释放内存后，你应该将指针设置为`nullptr`，避免悬挂指针（dangling pointer）问题：

```cpp
array = nullptr;
```

### 使用示例

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

## calloc

`calloc`函数用于在堆上分配内存并初始化所有位为零。这个函数定义在头文件`stdlib.h`中。由于需要初始化分配的内存, calloc 的性能比 malloc 差。

### 函数定义

```c
void* calloc(size_t num, size_t size);
```

### 参数

- `num`：要分配的元素的数量
- `size`：每个元素的大小（以字节为单位）

### 返回值

- 如果分配成功，会返回一个指向分配的内存块的指针，这块内存已经被初始化为零
- 如果分配失败，会返回`nullptr`

### 释放内存

与`malloc`一样，`calloc`分配的内存不再使用时，应该使用`free`函数来释放, 并且在释放内存后，将指针设置为`nullptr`，避免悬挂指针问题。

## realloc

`realloc`函数可以改变之前通过`malloc`、`calloc`或`realloc`本身分配的内存的大小。这个函数定义在头文件`stdlib.h`中。`realloc`的主要优势在于它可以扩展或缩小内存块的大小，而无需释放并重新分配内存，这样可以避免数据丢失和潜在的性能问题。`realloc`首先会在原来的内存基础上扩展, 如果无法扩展到指定的大小, 它会在其它位置重新找一块新的内存, 并把原来内存的数据拷贝到新的内存中。如果新的内存块比原来的内存块小，那么原来内存块中超出新块大小的部分将不会被初始化。如果新的内存块比原来的内存块大，那么新内存块中超出原来块大小的部分将不会被初始化。

### 函数定义

```c
void* realloc(void *ptr, size_t new_size);
```

### 参数

- `ptr`：指向先前分配的内存块的指针。如果是`nullptr`，`realloc`就会和`malloc`一个作用
- `new_size`：内存块应该具有的新大小，单位是字节

### 返回值

- 如果成功，`realloc`返回指向新分配内存块的指针（这可能与输入的`ptr`相同，也可能不同）
- 如果`new_size`是 0 并且`ptr`不是`nullptr`，`realloc`可能会释放内存，并且返回`nullptr`
- 如果无法分配请求的大小，返回`nullptr`指针，并且原来的内存块保持不变

### 使用示例

```c
// 原始分配10个整数的空间
int *array = (int *) malloc(10 * sizeof(int));
// 扩展到20个整数的空间
int *new_array = (int *) realloc(array, 20 * sizeof(int));
```

如果`realloc`成功，`new_array`将指向一个更大的内存块，这个新块可能与原来的`array`位于不同的地址。如果`realloc`失败，`new_array`将是`nullptr`，但原来的`array`仍然有效。

## new

在 C++中，`new`关键字是一种用于动态内存分配的操作符，它允许程序在运行时分配和构造对象。`new`底层是用`malloc`实现的，不同的是, C++的`new`操作符不仅分配内存，还会调用构造函数来初始化对象。

`new`的基本用法如下：

```cpp
type *pointer = new type(args...);
```

这里，`type`是要创建的对象的类型，`pointer`是一个指向新分配并初始化的对象的指针，`args...`是传递给对象构造函数的参数列表。

如果内存分配失败，`new`会抛出一个`std::bad_alloc`异常，而不是返回`nullptr`。

### 释放内存

使用`new`创建的对象需要使用`delete`操作符来释放内存。

如果使用`new[]`创建了一个数组，应该使用`delete[]`来释放它。

### 使用示例

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
