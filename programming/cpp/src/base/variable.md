# 变量

定义变量的方式:

```cpp
#include <iostream>

int main() {
    // 类型 变量名 = 初始值
    int a = 10;

    std::cout << "a = " << a << std::endl;
    return 0;
}
```

## 统一初始化

C++11 增加的功能。

```cpp
#include <iostream>

int main() {
    // 数据类型 变量名{初始值}
    int b{10};

    std::cout << "b = " << b << std::endl;
    return 0;
}
```

当用于内置类型的变量时, 这种初始化形式有一个重要特点：如果我们使用列表初始化且初始值存在丢失信息的风险, 则编译器将报错：

```cpp
int b{1.0d}; // 报错
```
