# 指向常量的指针

指向常量的指针(pointer to const)不能用于改变其所指对象的值。要想存放常量的地址, 只能使用指向常量的指针:

```cpp
const int a = 10;
const int *p = &a;
*p = 20; // 报错
```
