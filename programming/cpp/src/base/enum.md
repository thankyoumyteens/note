# 枚举

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
    }

    return 0;
}
```
