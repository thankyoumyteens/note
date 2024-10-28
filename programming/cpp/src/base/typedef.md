# 类型别名

为 int 取一个别名 MyInt 的三种方法:

1. `#define MyInt int`
2. `typedef int MyInt;`
3. `using Myint = int;`

定义函数指针的别名:

```cpp
#include <iostream>

typedef int (*MyAdd)(int, int);

int add(int a, int b) {
    return a + b;
}

int main(int argc, char *argv[]) {
    MyAdd myAdd = add;
    int result = myAdd(1, 2);
    std::cout << "result: " << result << std::endl;
    return 0;
}
```
