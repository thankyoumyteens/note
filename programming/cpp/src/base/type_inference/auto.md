# auto

auto 可用于告诉编译器，在编译时自动推断变量的类型。

```cpp
int a = 10;
auto b = a;
```

注意: `auto`去除了引用和 `const` 限定符，从而会创建副本。如果不需要副本，可使用 `auto &`或 `const auto &`。

```cpp
int a = 10;
const int &b = a;

// c的类型是 int, 而不是 const int &
auto c = b;

// d的类型是 const int
const auto d = b;
// e的类型是 const int &
const auto &e = b;
```
