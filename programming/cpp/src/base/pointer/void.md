# void 指针

函数的形参用 `void *`, 表示接受任意数据类型的指针, 比如:

```cpp
void *memccpy(void *__dst, const void *__src, int __c, size_t __n);
```

- 不能用 void 声明变量，它不能代表一个真实的变量
- 不能对 `void*` 指针直接解引用(需要转换成其它类型的指针)
- 把其它类型的指针赋值给 `void*` 指针不需要转换
- 把 `void*` 指针赋值给把其它类型的指针需要转换
