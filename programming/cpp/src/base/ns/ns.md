# 命名空间

命名空间用来处理不同代码段之间的名称冲突问题。

```cpp
// 指定命名空间
namespace ns {
    // 声明函数
    void f();
}

// 定义命名空间中的函数
void ns::f() {
    std::cout << "ns::f()" << std::endl;
}

int main() {
    // 调用命名空间中的函数
    ns::f();
    return 0;
}
```

## using

可使用 using 指令避免预先指明命名空间。这个指令通知编译器，后面的代码将使用指定命名空间中的名称。

```cpp
#include <iostream>

// 之后调用命名空间std中的函数时不需要加上std::
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
```

还可以使用 using 指令来引用命名空间内的特定项。

```cpp
#include <iostream>

// 之后调用cout时不需要加std::前缀
using std::cout;

int main() {
    cout << "Hello, World!" << std::endl;
    return 0;
}
```

## 命名空间别名

可使用命名空间别名，为一个长的命名空间指定一个更简短的新名称。

```cpp
#include <iostream>

// 为std命名空间起别名s
namespace s = std;

int main() {
    s::cout << "Hello, World!" << s::endl;
    return 0;
}
```
