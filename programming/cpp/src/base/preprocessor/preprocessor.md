# 预处理器

预处理指令以#字符开始, 比如 `#include`, 当预处理器看到 `#include <iostream>` 标记时就会提取 `<iostream>` 头文件中的所有内容并提供给当前文件。头文件最常见的用途是声明在其他地方定义的函数。在 C++中, 声明通常放在扩展名为 `.h` 的文件中, 称为头文件, 其定义通常包含在扩展名为 `.cpp` 的文件中, 称为源文件。

## 头文件保护符

C++程序还会用到的一项预处理功能是头文件保护符(header guard), 头文件保护符依赖于预处理变量。预处理变量有两种状态：已定义和未定义。

`#define` 指令把一个名字设定为预处理变量, 另外两个指令则分别检查某个指定的预处理变量是否已经定义：`#ifdef` 当且仅当变量已定义时为真, `#ifndef `当且仅当变量未定义时为真。一旦检查结果为真, 则执行后续操作直至遇到 `#endif` 指令为止。

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

第一次包含 my_utils.h 时, `#ifndef` 的检查结果为真, 预处理器将顺序执行后面的操作直至遇到 `#endif` 为止。此时, 预处理变量 CPP_PRIMER_DEMO_MY_UTILS_H 的值将变为已定义, 而且 my_utils.h 也会被拷贝到程序中。后面如果再一次包含 my_utils.h, 则 `#ifndef` 的检查结果将为假, 编译器将忽略 `#ifndef` 到 `#endif` 之间的部分。

如果编译器支持 `#pragma once` 指令(大多数现代编译器都支持), 可采用以下方法重写上面的代码：

```cpp
#pragma once

#include <string>

struct Demo {
    std::string name;
    int age;
};
```

## 引入头文件

在 #include 指令中：

- 尖括号 `<>`：用于包含标准库头文件，编译器会到系统指定的标准库路径下去查找对应的头文件，比如 `<stdio.h>` 等，它通常是编译器自带的标准库内容
- 双引号 `""`：一般用于包含用户自定义的头文件，编译器会先在当前源文件所在目录下查找相应头文件，如果没找到，再去标准库路径等其他路径下查找，常用于自己编写的模块对应的头文件包含情况
