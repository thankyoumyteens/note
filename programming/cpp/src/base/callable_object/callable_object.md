# 可调用对象

在 C++ 中，可调用对象（Callable Object）指所有可以像函数一样被 “调用” 的实体，即能通过 `()` 运算符执行操作的对象或表达式。

C++ 中常见的可调用对象分为以下 5 类，核心是能通过统一语法 `名称(参数)` 触发执行：

## 普通函数 / 函数指针

最基础的可调用对象，直接通过函数名或指针调用。

```cpp
void func(int x) {
    std::cout << " 输入参数: " << x << std::endl;
}

int main() {
    // 直接调用
    func(100);

    // 通过函数指针调用
    void (*p)(int) = func;
    p(200);

    return 0;
}
```

## 类成员函数指针

指向类非静态成员函数的指针，调用时需绑定具体的类对象（或指针 / 引用）。

```cpp
class A {
public:
    void method(int x) {
        std::cout << " 输入参数: " << x << std::endl;
    }
};

int main() {
    A a;
    // 指向成员函数的指针
    void (A::*p)(int) = &A::method;
    // 调用成员函数
    (a.*p)(20);

    return 0;
}
```

## 函数对象(Functor，仿函数)

重载了 `operator()` 的类 / 结构体的对象，本质是 “行为像函数的对象”，可携带状态（成员变量）。

```cpp
class Add {
public:
    int operator()(int a, int b) {
        return a + b;
    }
};

int main() {
    Add add;
    int sum = add(3, 4); // 调用 operator()，sum=7
    std::cout << sum << std::endl;

    return 0;
}
```

## lambda 表达式(C++11 引入)

匿名的函数对象，可捕获外部变量，语法简洁，常用于临时需要 “小函数” 的场景（如算法参数）。

```cpp
int main() {
    auto multiply = [](int a, int b) { return a * b; };
    int res = multiply(5, 6);
    std::cout << res << std::endl;

    return 0;
}
```

## std::function(C++11 引入)

通用的 “函数包装器”，可封装上述所有可调用对象，统一类型接口，解决 “不同可调用对象类型不兼容” 的问题（如作为函数参数、容器元素）。

```cpp
#include <iostream>
#include <functional>

int add(int a, int b) {
    return a + b;
}

int main() {
    std::function<int(int, int)> calc;

    calc = add;          // 封装函数对象
    int diff1 = calc(10, 3);
    std::cout << diff1 << std::endl;

    calc = [](int a, int b) { return a - b; }; // 封装 lambda
    int diff2 = calc(10, 3);
    std::cout << diff2 << std::endl;

    return 0;
}
```
