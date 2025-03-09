# 函数重载

C++ 允许定义名称相同的函数, 条件是它们的参数个数、数据类型和排列顺序不同。

```cpp
int func(int a);
int func(int a, int b);
int func(string a, int b);
```
