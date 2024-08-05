# 枚举

定义枚举:

```
enum class 类型名:基本类型 {
    选项1,
    选项2
};
```

示例:

```cpp
#include <iostream>

// 默认就是int, ":int" 可以省略
enum class DemoType : int {
    A = 1,
    B,
    C
};

int main() {
    DemoType a = DemoType::C;
    if (a == DemoType::A) {
        std::cout << "a is A" << std::endl;
    } else if (a == DemoType::B) {
        std::cout << "a is B" << std::endl;
    } else if (a == DemoType::C) {
        std::cout << "a is C" << std::endl;
    }
    return 0;
}
```
