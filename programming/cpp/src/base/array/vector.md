# std::vector

如果希望数组的大小是动态的，在 vector 中添加新元素时，vector 会自动调整大小。

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> arr;
    // 添加元素
    arr.push_back(10);
    std::cout << arr[0] << std::endl;
    return 0;
}
```
