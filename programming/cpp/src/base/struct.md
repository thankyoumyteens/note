# 结构体

```cpp
#include <iostream>

struct Person {
    std::string name;
    int age;
};

int main() {
    Person tom;
    tom.name = "Tom";
    tom.age = 10;

    std::cout << tom.name << std::endl;
    return 0;
}
```
