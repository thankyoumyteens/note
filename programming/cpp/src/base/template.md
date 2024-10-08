# 泛型

函数模版:

```cpp
#include <iostream>

template<typename T>
T add(T a, T b) {
    return a + b;
}

template<typename T>
void sort(T *arr, int length) {
    for (int i = 0; i < length; i++) {
        for (int j = i + 1; j < length; j++) {
            if (arr[i] > arr[j]) {
                T temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    // 自动推导泛型类型
    int r1 = add(1, 2);
    std::cout << "result: " << r1 << std::endl;

    // 手动指定泛型类型
    auto r2 = add<double>(1, 2);
    std::cout << "result: " << r2 << std::endl;

    int arr[] = {3, 2, 1};
    // 传递指针
    sort(arr, 3);
    for (int i: arr) {
        std::cout << i << " ";
    }
    return 0;
}
```

## 重载

传递指针类型时会出现问题

```cpp
#include <iostream>

template<typename T>
T max(T a, T b) {
    // 如果a和b时指针, 则比较的是指针存储的地址而不是值
    return a > b ? a : b;
}

int main(int argc, char *argv[]) {
    int a = 100;
    int b = 2;
    // 结果不对
    int *r1 = max(&a, &b);
    std::cout << "result: " << *r1 << std::endl;
    return 0;
}
```

使用重载解决

```cpp
#include <iostream>

template<typename T>
T max(T a, T b) {
    return a > b ? a : b;
}
template<typename T>
T max(T *a, T *b) {
    return *a > *b ? *a : *b;
}

int main(int argc, char *argv[]) {
    int a = 100;
    int b = 2;
    int r1 = max(&a, &b);
    std::cout << "result: " << r1 << std::endl;
    int r2 = max(a, b);
    std::cout << "result: " << r2 << std::endl;
    return 0;
}
```
