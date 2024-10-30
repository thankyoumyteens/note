# 预处理器

比如预处理功能 `#include`，当预处理器看到 `#include` 标记时就会用指定的头文件的内容代替 `#include`。

C++程序还会用到的一项预处理功能是头文件保护符(header guard)，头文件保护符依赖于预处理变量。预处理变量有两种状态：已定义和未定义。

`#define` 指令把一个名字设定为预处理变量，另外两个指令则分别检查某个指定的预处理变量是否已经定义：`#ifdef` 当且仅当变量已定义时为真，`#ifndef `当且仅当变量未定义时为真。一旦检查结果为真，则执行后续操作直至遇到 `#endif` 指令为止。

例如 my_utils.h：

```cpp
// 如果没有定义过预处理变量 CPP_PRIMER_DEMO_MY_UTILS_H, 会继续执行下面的代码
// 如果定义过预处理变量 CPP_PRIMER_DEMO_MY_UTILS_H, 不会执行下面的代码
#ifndef CPP_PRIMER_DEMO_MY_UTILS_H
// 定义 CPP_PRIMER_DEMO_MY_UTILS_H 变量
#define CPP_PRIMER_DEMO_MY_UTILS_H

#include <string>

struct Demo {
    std::string name;
    int age;
};
#endif //CPP_PRIMER_DEMO_MY_UTILS_H
```

第一次包含 my_utils.h 时，`#ifndef` 的检查结果为真，预处理器将顺序执行后面的操作直至遇到 `#endif` 为止。此时，预处理变量 CPP_PRIMER_DEMO_MY_UTILS_H 的值将变为已定义，而且 my_utils.h 也会被拷贝到程序中。后面如果再一次包含 my_utils.h，则 `#ifndef` 的检查结果将为假，编译器将忽略 `#ifndef` 到 `#endif` 之间的部分。
