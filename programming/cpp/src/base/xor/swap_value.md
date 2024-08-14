# 交换两个变量的值

仅适用于整数类型的变量:

```cpp
int a = 1;
int b = 2;

a = a ^ b
b = a ^ b
a = a ^ b // a = 2, b = 1
```

计算过程:

1. `a = a ^ b`:
   - `a = a ^ b`
   - `b = b`
2. `b = a ^ b`:
   - `a = a ^ b`
   - `b = a ^ b ^ b`, 由于`b ^ b = 0`, 所以 `b = a`
3. `a = a ^ b`:
   - `a = a ^ b ^ a`, 由于`a ^ a = 0`, 所以 `a = b`
   - `b = a`
