# lock_guard

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <stdexcept>

// 共享资源
int shared_data = 0;
std::mutex mtx;

// 示例1：基本用法，避免手动加锁/解锁
void basic_usage(int thread_id) {
    for (int i = 0; i < 1000; ++i) {
        // 构造lock_guard时自动加锁，离开作用域时自动解锁
        std::lock_guard<std::mutex> lock(mtx);

        // 临界区：安全操作共享资源
        shared_data++;
        // 即使在此处提前return，lock析构时仍会解锁
    }
}

// 示例2：异常场景下的自动解锁
void exception_safe_usage() {
    try {
        std::lock_guard<std::mutex> lock(mtx);
        shared_data = 100;

        // 模拟异常
        throw std::runtime_error("模拟错误");

        // 以下代码不会执行，但锁仍会被释放
        shared_data = 200;
    }
    catch (const std::exception &e) {
        std::cout << "捕获异常: " << e.what() << "，但锁已安全释放" << std::endl;
    }
}

// 示例3：与递归锁配合使用
std::recursive_mutex rec_mtx;
int recursive_data = 0;

void recursive_func(int depth) {
    // 每次递归都会创建lock_guard，自动加锁
    std::lock_guard<std::recursive_mutex> lock(rec_mtx);

    recursive_data++;
    std::cout << "递归深度: " << depth << ", 数据值: " << recursive_data << std::endl;

    if (depth > 0) {
        recursive_func(depth - 1);  // 递归调用，再次加锁（仅recursive_mutex允许）
    }
    // 离开作用域时自动解锁，解锁次数与加锁次数匹配
}

int main() {
    // 测试基本用法
    std::thread thread1(basic_usage, 1);
    std::thread thread2(basic_usage, 2);
    thread1.join();
    thread2.join();
    std::cout << "最终共享数据值: " << shared_data << std::endl << std::endl;

    // 测试异常安全
    exception_safe_usage();
    std::cout << "异常后共享数据值: " << shared_data << std::endl << std::endl;

    // 测试递归锁配合
    std::thread rec_thread(recursive_func, 3);
    rec_thread.join();
    std::cout << "递归操作后数据值: " << recursive_data << std::endl;

    return 0;
}
```
