# 重载赋值运算符

```cpp
class Demo {
public:
    int val;

    // 重载赋值运算符
    Demo &operator=(const Demo &rhs) {
        if (this == &rhs) {
            // 自赋值
            return *this;
        }
        val = rhs.val;
        return *this;
    }
};

int main() {
    Demo a;
    a.val = 100;

    Demo b;

    // 相当于 b.operator=(a);
    b = a;
    std::cout << "b.val: " << b.val << std::endl;
    return 0;
}
```
