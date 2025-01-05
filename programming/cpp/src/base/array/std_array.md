# std::array

C++提供了一种大小固定的特殊容器 `std::array`, 在 `<array>` 头文件中定义。它基本上是对 C 风格的数组进行了简单包装。

可以用 `std::array` 替代 C 风格的数组, 它知道自身大小;不会自动转换为指针, 从而避免了某些类型的 bug;具有迭代器, 可方便地遍历元素。

```cpp
#include <iostream>
#include <array>

int main() {
    std::array<int, 3> arr = {1, 2, 3};
    // 使用自带的size函数直接获取数组长度
    std::cout << arr.size() << std::endl;
    return 0;
}
```
