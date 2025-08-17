# mutex

std::mutex 确保同一时间只有一个线程能获得锁，从而独占访问被保护的共享资源。其他试图获取锁的线程会被阻塞，直到持有锁的线程释放锁。

基本操作

- lock()：获取锁。如果锁已被其他线程持有，当前线程会阻塞等待，直到成功获取锁。
- unlock()：释放锁。必须由持有锁的线程调用，否则会导致未定义行为（通常程序崩溃）。
- try_lock()：尝试获取锁。如果锁未被持有，则获取成功并返回 true；如果锁已被持有，则立即返回 false（不会阻塞）。

非递归性: std::mutex 是非递归的，即同一线程不能对已持有的锁再次调用 lock()，否则会导致死锁（线程自己阻塞自己）。如果需要递归锁，应使用 std::recursive_mutex。

```cpp
#include <iostream>
#include <thread>
#include <mutex>

// 共享资源：计数器
int shared_counter = 0;

// 定义互斥锁
std::mutex mtx;

// 线程函数：安全地递增计数器
void increment_counter() {
    for (int i = 0; i < 10000; ++i) {
        mtx.lock();
        shared_counter++;
        mtx.unlock();
    }
}

int main() {
    std::thread thread1(increment_counter);
    std::thread thread2(increment_counter);

    // 等待所有线程完成
    thread1.join();
    thread2.join();
    std::cout << "最终计数器值: " << shared_counter << std::endl;
    return 0;
}
```