# decltype

关键字 decltype 把表达式作为实参，计算出该表达式的类型。

```cpp
int a = 10;
decltype(a) b;
```

decltype 和 auto 的区别在于，decltype 不会去除引用和 const 限定符。

```cpp
int a = 10;
const int &b = a;

// c的类型是 const int &
decltype(b) c = b;
```
