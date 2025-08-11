# 创建带参数的线程

```cpp
#include <iostream>
#include <thread>

// 带参数的线程函数
void print_message(const std::string &msg, int count) {
    for (int i = 0; i < count; ++i) {
        std::cout << "线程id " << std::this_thread::get_id() << ": " << msg << " (" << i + 1 << ")" << std::endl;
    }
}

int main() {
    // 创建带参数的线程
    std::thread t1(print_message, "来自main", 10);
    // 等待线程t1执行完成
    t1.join();

    return 0;
}
```
