# 创建简单线程

```cpp
#include <iostream>
#include <thread>

// 无参数的线程函数
void print_hello() {
    std::cout << "线程id: " << std::this_thread::get_id() << std::endl;
}

int main() {
    // 创建线程
    std::thread t1(print_hello);
    // 等待线程t1执行完成
    t1.join();

    return 0;
}
```
