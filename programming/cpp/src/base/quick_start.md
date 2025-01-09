# Hello World

CLion 创建 C++ 项目:

- 新建工程: 在新项目向导的语言标准字段中选择 C++ 11
- 已有工程: 在 CMakeLists.txt 文件中 将 `CMAKE_CXX_STANDAR` 变量设置为 11

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```
