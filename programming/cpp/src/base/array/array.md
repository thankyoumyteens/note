# 数组

```cpp
#include <iostream>

int main() {
    // 声明数组, 未初始化
    int arr1[3];
    std::cout << arr1[1] << std::endl;

    // 声明数组, 初始化为0
    int arr2[3] = {};
    std::cout << arr2[1] << std::endl;

    // 声明数组, 初始化为1, 2, 3
    // 编译器可自动推断出数组的大小
    int arr3[] = {1, 2, 3};
    std::cout << arr3[1] << std::endl;
    return 0;
}
```

## 计算数组的长度

```cpp

int arr[] = {1, 2, 3};

// 传统做法
unsigned size = sizeof(arr) / sizeof(arr[0]);

// C++17 增加
// 需要 #include <array>
unsigned size = std::size(arr);
```
