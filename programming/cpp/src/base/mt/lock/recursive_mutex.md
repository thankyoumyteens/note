# recursive_mutex

std::recursive_mutex 允许同一线程对已持有的锁再次调用 lock()，只要解锁次数与加锁次数相同即可正常释放。这解决了 std::mutex 中同一线程重复加锁导致的死锁问题。

提供与 std::mutex 相同的基本操作：

- lock()：获取锁（同一线程可多次调用）。
- unlock()：释放锁（需与 lock() 调用次数相同）。
- try_lock()：尝试获取锁（成功返回 true）。

适用场景: 主要用于递归函数或同一同一函数中多次需要加锁的场景。例如，递归遍历数据结构时，每次递归调用都需要访问共享资源，此时递归锁可避免死锁。

```cpp
#include <iostream>
#include <thread>
#include <mutex>

// 递归互斥锁
std::recursive_mutex rec_mtx;
int shared_value = 0;

// 递归函数：演示同一线程多次加锁
void recursive_func(int depth) {
    // 第一次调用：获取锁；递归调用时：再次获取同一把锁（仅recursive_mutex允许）
    rec_mtx.lock();

    // 操作共享资源
    shared_value++;
    std::cout << "递归深度: " << depth
              << ", 线程ID: " << std::this_thread::get_id()
              << ", 共享值: " << shared_value << std::endl;

    // 递归终止条件
    if (depth > 0) {
        recursive_func(depth - 1);  // 递归调用，再次进入加锁逻辑
    }

    // 解锁：次数需与加锁次数相同
    rec_mtx.unlock();
}

// 线程函数：启动递归调用
void thread_func() {
    recursive_func(3);  // 递归深度为3，会触发4次加锁（包括始调用+3次递归）
}

int main() {
    std::thread t1(thread_func);
    std::thread t2(thread_func);

    t1.join();
    t2.join();

    std::cout << "最终共享值: " << shared_value << std::endl;  // 预期结果：8（每个线程贡献4次递增）
    return 0;
}
```
