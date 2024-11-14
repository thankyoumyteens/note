# if 语句

```cpp
int a = 1;
if (a == 1) {
    std::cout << "ok" << std::endl;
} else {
    std::cout << "error" << std::endl;
}
```

## 在 if 条件中创建变量

C++17 允许在 if 语句中创建变量。

```cpp
if (int a = 1; a == 1) {
    std::cout << "ok" << std::endl;
}
```
