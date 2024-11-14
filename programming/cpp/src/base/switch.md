# switch 语句

```cpp
int a = 1;
switch (a) {
    case 1:
        std::cout << "ok" << std::endl;
        break;
    default:
        break;
}
```

## 在 switch 条件中创建变量

与 if 语句一样, C++17 允许在 switch 语句中创建变量。

```cpp
switch (int a = 1; a) {
    case 1:
        std::cout << "ok" << std::endl;
        break;
    default:
        break;
}
```
