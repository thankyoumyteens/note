# 结构体

```cpp
struct Person {
    std::string name;
    int age;
};
```

使用:

```cpp
Person tom;
tom.name = "Tom";
tom.age = 10;

std::cout << tom.name << std::endl;
```

## 通过指针访问结构体

```cpp
Person tom;
Person *p = &tom;
p->name = "Tom";
p->age = 10;

std::cout << p->name << std::endl;
```
