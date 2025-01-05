# 使用迭代器

支持迭代器的类型同时拥有返回迭代器的成员。比如, 这些类型都拥有名为 begin 和 end 的成员, 其中 begin 成员负责返回指向第一个元素的迭代器。end 成员则负责返回指向容器"最后一个元素的下一位置(one past the end)"的迭代器, 也就是说, 该迭代器指示的是容器的一个本不存在的"尾后(off the end)"元素, end 成员返回的迭代器常被称作尾后迭代器(off-the-end iterator)或者简称为尾迭代器(end iterator)。如果容器为空, 则 begin 和 end 返回的是同一个迭代器。

begin 和 end 返回的具体类型由对象是否是常量决定, 如果对象是常量, begin 和 end 返回 const_iterator；如果对象不是常量, 返回 iterator。

```cpp
vector<int> v1;
vector<int>::iterator begin = v1.begin();
vector<int>::iterator end = v1.end();

const vector<int> v2;
vector<int>::const_iterator begin = v1.begin();
vector<int>::const_iterator end = v1.end();
```

## 常用的迭代器操作

- `*iter` 返回迭代器 iter 所指元素的值
- `iter->mem` 访问成员变量, 等价于 `(*iter).mem`
- `++iter` 令 iter 指向容器中的下一个元素
- `--iter` 令 iter 指向容器中的上一个元素
- `iterl == iter2` 判断两个迭代器是否相等, 如果两个迭代器指示的是同一个元素或者它们是同一个容器的尾后迭代器, 则相等；反之, 不相等
- `iterl != iter2` 判断两个迭代器是否不相等

## 使用迭代器遍历 vector

```cpp
#include <iostream>

using std::vector;
using std::cout;

int main(int argc, char *argv[]) {
    vector<int> v = {1, 2, 3};
    // begin和end的类型是vector<int>::iterator
    auto begin = v.begin();
    auto end = v.end();
    for (auto it = begin; it != end; ++it) {
        cout << *it << " ";
    }
    return 0;
}
```

## cbegin 和 cend

如果对象只需读操作而无须写操作的话最好使用常量类型(比如 const_iterator)。为了便于专门得到 const_iterator 类型的返回值, C++11 新标准引入了两个新函数, 分别是 cbegin 和 cend:

```cpp
#include <iostream>

using std::vector;
using std::cout;

int main(int argc, char *argv[]) {
    vector<int> v = {1, 2, 3};
    // begin和end的类型是vector<int>::const_iterator
    auto begin = v.cbegin();
    auto end = v.cend();
    for (auto it = begin; it != end; ++it) {
        cout << *it << " ";
    }
    return 0;
}
```
