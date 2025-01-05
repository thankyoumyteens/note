# 友元

C++ 允许某个类将其他类、其他类的成员函数或非成员函数声明为友元(friend), 友元可以访问类的 protected, private 数据成员和方法。

## 类作为友元

```cpp
class Demo;

class Logger {
public:
    void print(const Demo &d);
};

class Demo {
    friend Logger;

private:
    int val;
};

void Logger::print(const Demo &d) {
    std::cout << d.val << std::endl;
}
```

## 成员函数作为友元

```cpp
class Demo;

class Logger {
public:
    void print(const Demo &d);
};

class Demo {
    friend void Logger::print(const Demo &);

private:
    int val;
};

void Logger::print(const Demo &d) {
    std::cout << d.val << std::endl;
}
```

## 非成员函数作为友元

```cpp
class Demo {
    friend void printLog(const Demo &);

private:
    int val;
};

void printLog(const Demo &d) {
    std::cout << d.val << std::endl;
}
```
