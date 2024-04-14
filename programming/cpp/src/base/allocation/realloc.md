# realloc

`realloc`函数可以改变之前通过`malloc`、`calloc`或`realloc`本身分配的内存的大小。这个函数定义在头文件`stdlib.h`中。`realloc`的主要优势在于它可以扩展或缩小内存块的大小, 而无需释放并重新分配内存, 这样可以避免数据丢失和潜在的性能问题。`realloc`首先会在原来的内存基础上扩展, 如果无法扩展到指定的大小, 它会在其它位置重新找一块新的内存, 并把原来内存的数据拷贝到新的内存中。如果新的内存块比原来的内存块小, 那么原来内存块中超出新块大小的部分将不会被初始化。如果新的内存块比原来的内存块大, 那么新内存块中超出原来块大小的部分将不会被初始化。

## 函数定义

```c
void* realloc(void *ptr, size_t new_size);
```

## 参数

- `ptr`: 指向先前分配的内存块的指针。如果是`nullptr`, `realloc`就会和`malloc`一个作用
- `new_size`: 内存块应该具有的新大小, 单位是字节

## 返回值

- 如果成功, `realloc`返回指向新分配内存块的指针(这可能与输入的`ptr`相同, 也可能不同)
- 如果`new_size`是 0 并且`ptr`不是`nullptr`, `realloc`可能会释放内存, 并且返回`nullptr`
- 如果无法分配请求的大小, 返回`nullptr`指针, 并且原来的内存块保持不变

## 使用示例

```c
// 原始分配10个整数的空间
int *array = (int *) malloc(10 * sizeof(int));
// 扩展到20个整数的空间
int *new_array = (int *) realloc(array, 20 * sizeof(int));
```

如果`realloc`成功, `new_array`将指向一个更大的内存块, 这个新块可能与原来的`array`位于不同的地址。如果`realloc`失败, `new_array`将是`nullptr`, 但原来的`array`仍然有效。
