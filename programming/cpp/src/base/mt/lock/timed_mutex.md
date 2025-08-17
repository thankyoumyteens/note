# timed_mutex

它在 std::mutex 的基础上增加了超时获取锁的能力，允许线程在获取锁时指定等待时间，避免无限期阻塞，提高了多线程程序的灵活性和健壮性。

除了 lock()、unlock()、try_lock() 等基础方法外，std::timed_mutex 还提供了两个核心超时方法：

- try_lock_for(const duration& rel_time)：尝试获取锁，最多等待 rel_time 时间（相对时间），超时返回 false。
- try_lock_until(const time_point& abs_time)：尝试获取锁，直到 abs_time 时间点（绝对时间），超时返回 false。

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

// 带超时功能的互斥锁
std::timed_mutex timed_mtx;
int shared_counter = 0;

// 线程函数：使用超时锁访问共享资源
void worker_thread(int id) {
    // 每个线程尝试5次获取锁
    for (int i = 0; i < 5; ++i) {
        // 尝试获取锁，最多等待100毫秒
        if (timed_mtx.try_lock_for(std::chrono::milliseconds(100))) {
            // 成功获取锁，操作共享资源
            shared_counter++;
            std::cout << "线程 " << id << " 成功获取锁，计数: " << shared_counter << std::endl;

            // 持有锁一段时间（模拟工作）
            std::this_thread::sleep_for(std::chrono::milliseconds(50));

            // 释放锁
            timed_mtx.unlock();
        } else {
            // 超时未获取锁，做其他处理
            std::cout << "线程 " << id << " 获取锁超时，继续等待下一次尝试" << std::endl;
        }

        // 两次尝试之间间隔一段时间
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
}

int main() {
    std::thread worker1(worker_thread, 1);
    std::thread worker2(worker_thread, 2);
    worker1.join();
    worker2.join();
    std::cout << "最终计数: " << shared_counter << std::endl << std::endl;

    return 0;
}
```
