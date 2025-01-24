# 原始字面量

通过原始字面量避免使用斜杠转译。格式是 `R"(内容)"`。

```cpp
#include <iostream>

int main() {
    std::string a = R"(C:\Users\user\Desktop\c\c\main.cpp)";

    std::cout << a << std::endl;

    std::string b = R"(
{
    "name": "c",
    "version": "0.1.0",
    "description": "",
}
)";

    std::cout << b << std::endl;

    return 0;
}
```
