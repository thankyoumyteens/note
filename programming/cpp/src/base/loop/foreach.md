# 基于区间的 for 循环

```cpp
#include <iostream>

int main() {
    int arr[] = {1, 2, 3};
    auto [a, b, c] = arr;

    for (auto item: arr) {
        std::cout << item << std::endl;
    }
    return 0;
}
```
