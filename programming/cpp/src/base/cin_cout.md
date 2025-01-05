# 输入输出

```cpp
#include <iostream>

int main() {
    std::cout << "Enter two numbers:" << std::endl;
    int v1 = 0, v2 = 0;
    std::cin >> v1 >> v2;
    std::cout << "The sum of " << v1 << " and " << v2 << " is " << v1 + v2 << std::endl;
    return 0;
}
```

在 C++中, 一个表达式产生一个计算结果, 它由一个或多个运算对象和(通常是)一个运算符组成。

```cpp
std::cout << "Enter two numbers:" << std::endl;
```

`<<` 运算符接受两个运算对象：左侧的运算对象必须是一个 ostream 对象, 右侧的运算对象是要打印的值。此运算符将给定的值写到给定的 ostream 对象中。输出运算符的计算结果就是其左侧运算对象。即 `std::cout`。

我们的输出语句使用了两次 `<<` 运算符。因为此运算符返回其左侧的运算对象, 因此第个运算符的结果成为了第二个运算符的左侧运算对象。这样, 我们就可以将输出请求连接起来。因此, 我们的表达式等价于

```cpp
(std::cout << "Enter two numbers:") << std::endl;
```
