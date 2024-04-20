# memcopy

`memcpy`函数用于将一段内存中的数据复制到另一段内存中。这个函数定义在头文件`<string.h>`中，是处理内存和字符串操作中非常常用的一个函数。

## 函数定义

```c
void *memcpy(void *dest, const void *src, size_t n);
```

`memcpy`会从`src`指向的源内存地址开始，复制`n`个字节的数据到`dest`指向的目标内存地址。复制操作是逐字节进行的，不保证对象的对齐，并且不会调用对象的复制构造函数或赋值操作符（对于 C++中的类对象）。

## 参数

1. `dest`：目标内存地址的指针，指向需要将数据复制到的内存位置。
2. `src`：源内存地址的指针，指向需要复制数据的内存位置。
3. `n`：需要复制的字节数。

## 返回值

`memcpy`函数返回一个指向目标内存的指针，通常是`dest`参数的值。

## 使用示例

```c
#include <cstdio>
#include <cstring>

int main() {
    char src[] = "Hello, World!";
    char dest[20];

    // 复制src到dest
    // 包括字符串结束符'\0'
    memcpy(dest, src, strlen(src) + 1);

    printf("Copied String: %s\n", dest);
    return 0;
}
```
