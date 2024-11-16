# 常量

定义常量:

```cpp
const int a = 10;
std::cout << "a = " << a << std::endl;
```

## 使用 const 保护参数

```cpp
// 在函数内无法修改str指向的字符串的值
void printString(const std::string *str) {
    *str = "other string"; // 无法通过编译
    std::cout << *str << std::endl;
}

int main() {
    std::string str = "Hello, World!";
    printString(&str);
    return 0;
}
```
