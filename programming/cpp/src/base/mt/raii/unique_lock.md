# unique_lock

```cpp
#include <iostream>
#include <thread>
#include <mutex>

std::mutex mtx;
int shared_data = 0;

// 示例1：基本用法与手动解锁
void basic_usage() {
    // std::defer_lock: 延迟锁定（构造时不获取锁）
    std::unique_lock<std::mutex> lock(mtx, std::defer_lock);

    // 手动获取锁
    lock.lock();
    std::cout << "线程 " << std::this_thread::get_id() << " 获取锁" << std::endl;

    // 操作共享资源
    shared_data = 42;

    // 提前手动解锁, 如果不提前解锁就会在析构函数中释放锁
    lock.unlock();
    std::cout << "线程 " << std::this_thread::get_id() << " 提前解锁" << std::endl;

    // 后续需要时可再次锁定
    std::this_thread::sleep_for(std::chrono::seconds(1));
    lock.lock();
    std::cout << "线程 " << std::this_thread::get_id() << " 再次获取锁" << std::endl;
}


int main() {
    std::thread t1(basic_usage);
    std::thread t2(basic_usage);
    t1.join();
    t2.join();
    std::cout << std::endl;

    return 0;
}
```
