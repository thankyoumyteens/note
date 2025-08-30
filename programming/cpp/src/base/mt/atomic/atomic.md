# 原子类型

原子类型的所有操作（如赋值、自增、比较等）都是不可分割的，不会被其他线程中断。这意味着无需额外的同步机制（如互斥锁），就能保证多线程访问的安全性。大多数原子类型的实现采用硬件级别的原子指令（如 CPU 的 CAS 指令），避免了互斥锁的上下文切换开销，性能通常优于基于锁的同步。

C++ 标准库提供了多种原子类型，对应基本数据类型：

- `std::atomic<bool>`：原子布尔型
- `std::atomic<char>`、`std::atomic<int>`、`std::atomic<long>`等：原子整数类型
- `std::atomic<float>`、`std::atomic<double>`：原子浮点类型（C++20 起支持）
- `std::atomic<T*>`：原子指针类型

```cpp
#include <iostream>
#include <thread>
#include <atomic>
#include <vector>

// 原子类型变量（可以安全地被多线程访问）
std::atomic<int> atomic_counter(0);

// 使用原子类型的线程函数
void atomic_increment() {
    for (int i = 0; i < 100000; ++i) {
        // 原子自增操作，线程安全
        atomic_counter++;
    }
}

int main() {
    const int num_threads = 8;
    std::vector<std::thread> threads;

    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(atomic_increment);
    }
    for (auto& t : threads) {
        t.join();
    }

    std::cout << "结果: " << atomic_counter << std::endl;
    return 0;
}
```
