# 类

在 C++ 中, 类通常在头文件(.h)中声明, 在对应的源文件(.cpp)中定义其非内联方法和静态数据成员。

类中可以声明数据成员(属性)以及方法(行为)。每个数据成员以及方法都具有特定的访问级别：public、protected 或 private。这些标记可按任意顺序出现, 也可重复使用。

```cpp
class Person {
private:
    std::string name;
    int age;
public:
    // 使用构造函数初始化器初始化成员变量
    Person() : name("unknown"), age(0) {
        std::cout << "构造函数" << std::endl;
    }

    ~Person() {
        // 执行一些清理操作, 如关闭文件、释放内存等
        std::cout << "析构函数" << std::endl;
    }

    void setName(const std::string &newName) {
        name = newName;
    }

    // 最好将不改变对象的成员变量的方法声明为const
    const std::string &getName() const {
        return name;
    }
};
```

## 使用类

```cpp
// 在栈上创建对象
Person tom;
tom.setName("Tom");
std::cout << tom.getName() << std::endl;

// 在堆上创建对象
Person *jerry = new Person();
jerry->setName("Jerry");
std::cout << jerry->getName() << std::endl;
delete jerry;
```
