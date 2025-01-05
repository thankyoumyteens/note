# 迭代器运算

可以令迭代器和一个整数值相加(或相减), 其返回值是向前(或向后)移动了若干个位置的迭代器。

```cpp
#include <iostream>

using std::vector;
using std::cout;

// 二分查找
int main(int argc, char *argv[]) {
    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    int target = 7;
    const unsigned long len = v.end() - v.begin();
    auto middle = v.begin() + len / 2;
    while (middle != v.end()) {
        if (*middle == target) {
            break;
        }
        if (*middle < target) {
            middle = middle + (v.end() - middle) / 2;
        } else {
            middle = middle - (middle - v.begin()) / 2;
        }
    }
    cout << *middle;

    return 0;
}
```
