# memset

`memset` 是 C 语言标准库中的一个函数, 用于将一块内存中的所有字节设置为特定的值。这个函数定义在头文件 `<cstring>` 或 `<string.h>` 中, 常用于初始化或清零内存。

## 函数定义

```c
void *memset(void *str, int c, size_t n);
```

`memset` 函数从 `str` 指向的内存地址开始, 将连续的 `n` 个字节设置为值 `c`。`c` 通常传递一个 `int` 类型的值, 但只会取其低 8 位, 因为每个字节由 8 位组成。

## 参数

1. `str`: 指向要填充的内存块的起始地址的指针。
2. `c`: 要设置的值, 必须是一个整数（通常是 `unsigned char` 类型）, 并且会被转换为 `unsigned char`。
3. `n`: 要设置的字节数。

### 返回值

`memset` 函数返回指向被设置内存块的起始地址的指针, 通常是 `str` 参数的值。

### 使用示例

```c
#include <cstdio>
#include <cstring>

int main() {
    char buffer[10];

    // 将buffer的前5个字节设置为字符'A'
    memset(buffer, 'A', 5);

    // 将buffer的剩余5个字节设置为字符'B'
    memset(buffer + 5, 'B', 5);

    // 输出buffer的内容
    printf("Buffer: %s\n", buffer);
    return 0;
}
```
