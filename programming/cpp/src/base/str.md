# 字符串操作

## 拼接

```cpp
#include <iostream>

using std::string;

int main() {
    string str = "1";
    // + 左边必须是string类型变量
    str = str + "2";
    std::cout << str << std::endl;
    return 0;
}
```

## 比较

```cpp
#include <iostream>

using std::string;

int main() {
    string a = "1";
    string b = "2";

    std::cout << (a > b) << std::endl;
    std::cout << (a < b) << std::endl;
    std::cout << (a == b) << std::endl;
    // a > b -> 结果大于0
    // a < b -> 结果小于0
    // a == b -> 结果等于0
    std::cout << a.compare(b) << std::endl;
    return 0;
}
```

## 查找子串

```cpp
#include <iostream>

using std::string;

int main() {
    string a = "123123";
    // 从头开始找
    std::cout << a.find("23") << std::endl;
    // 从索引2处开始找
    std::cout << a.find("23", 2) << std::endl;
    //没找到返回 std::string::npos, 是一个很大的数
    std::cout << a.find("00") << std::endl;
    return 0;
}
```

## 截取子串

```cpp
#include <iostream>

using std::string;

int main() {
    string a = "123123";
    // 从索引1开始截取长度为2的字符串
    std::cout << a.substr(1, 2) << std::endl;
    return 0;
}
```

## 替换

```cpp
#include <iostream>

using std::string;

int main() {
    string a = "123123";
    // 从索引1开始长度为2的字符串, 替换成abc
    std::cout << a.replace(1, 2, "abc") << std::endl;
    // 输出: 1abc123
    return 0;
}
```
