# 实现遍历列表

自定义回调函数, 处理每个遍历到的元素

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

## 传入类

自定义回调函数可以传入类, 以实现更多功能。

```cpp
#include <iostream>
#include <utility>
#include <vector>

// 遍历列表
template<typename T, typename F>
void forEach(T begin, T end, F call) {
    for (T item = begin; item != end; ++item) {
        call(*item);
    }
}

// 自定义输出(类)
template<typename T>
class Printer {
private:
    std::string prefix;
public:
    explicit Printer(std::string prefix) : prefix(std::move(prefix)) {}

    // 重载()运算符, 实现模拟函数调用
    void operator()(const T &item) {
        std::cout << prefix << item << std::endl;
    }
};

// 自定义输出(函数)
template<typename T>
void printItem(const T &item) {
    std::cout << "item: " << item << std::endl;
}

int main(int argc, char *argv[]) {
    std::vector<std::string> list1{"aaa", "bbb", "ccc"};
    std::vector<int> list2{1, 2, 3};

    // 传入类
    forEach(list1.begin(), list1.end(), Printer<std::string>("当前遍历到: "));
    // 传入函数
    forEach(list2.begin(), list2.end(), printItem<int>);

    return 0;
}
```
