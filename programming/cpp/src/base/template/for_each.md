# 实现遍历列表

```cpp
#include <iostream>
#include <vector>

// 遍历列表
template<typename T, typename V>
void forEach(T begin, T end, void(*call)(const V &item)) {
    for (T item = begin; item != end; ++item) {
        call(*item);
    }
}

// 自定义输出
template<typename T>
void printItem(const T &item) {
    std::cout << "item: " << item << std::endl;
}

int main(int argc, char *argv[]) {
    std::vector<std::string> list1{"aaa", "bbb", "ccc"};
    std::vector<int> list2{1, 2, 3};

    forEach(list1.begin(), list1.end(), printItem<std::string>);
    forEach(list2.begin(), list2.end(), printItem<int>);

    return 0;
}
```
