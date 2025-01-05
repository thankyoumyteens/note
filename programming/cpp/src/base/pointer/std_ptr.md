# 智能指针

智能指针对象在超出作用域时, 例如在函数执行完毕后, 会自动释放内存。

## unique_ptr

`std::unique_ptr` 类似于普通指针, 但在 unique_ptr 超出作用域或被删除时, 会自动释放内存或资源。unique_ptr 只属于它指向的对象。

```cpp
// make_unique 在C++14中引入

// 创建结构体的实例, 并创建指向它的指针p
std::unique_ptr<DemoStruct> p = std::make_unique<DemoStruct>();
p->name = "demo";
std::cout << p->name << std::endl;

// 创建数组, 并创建指向它的指针p
std::unique_ptr<DemoStruct[]> arr = std::make_unique<DemoStruct[]>(10);
arr[0].name = "demo";
std::cout << arr[0].name << std::endl;
```

## shared_ptr

和 unique_ptr 不同, 每个 `std::shared_ptr` 指针内部都维护一个引用计数器, 记录有多少个 shared_ptr 指针共享同一个对象。当引用计数降为零时, 对象会被自动删除。

```cpp
// 创建结构体的实例, 并创建指向它的指针p
std::shared_ptr<DemoStruct> p = std::make_shared<DemoStruct>();
p->name = "demo";
std::cout << p->name << std::endl;

// 创建数组, 并创建指向它的指针p
// 从C++17开始, 才可以将数组存储在shared_ptr中
std::shared_ptr<DemoStruct[]> arr(new DemoStruct[10]);
arr[0].name = "demo";
std::cout << arr[0].name << std::endl;
```
