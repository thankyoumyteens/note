# 右值引用

在 C++中，左值(lvalue)是可获取其地址的一个量，例如一个有名称的变量。由于经常出现在赋值语句的左边，因此将其称作左值。

另外，所有不是左值的量都是右值(rvalue)，例如字面量、临时对象或临时值。通常右值位于赋值运算符的右边。

例如:

```cpp
int a = 4 * 2;
```

在这条语句中，a 是左值，它具有名称，它的地址为 `&a`。右侧表达式 `4 * 2` 的结果是右值。它是一个临时值，将在语句执行完毕时销毁。

右值引用是一个对右值(rvalue)的引用。特别地，这是一个当右值是临时对象时才适用的概念。右值引用的目的是在涉及临时对象时提供可选用的特定函数。由于知道临时对象会被销毁，通过右值引用，某些涉及复制大量值的操作可通过简单地复制指向这些值的指针来实现。

使用 `&&` 指定右值引用。

```cpp
void print(std::string &str) {
    std::cout << "lvalue:" << str << std::endl;
}

// 接收右值引用
void print(std::string &&str) {
    std::cout << "rvalue:" << str << std::endl;
}

int main() {
    std::string str = "hello world";
    // 调用左值版本
    print(str);

    // 调用右值版本
    print("hello world");
    return 0;
}
```
