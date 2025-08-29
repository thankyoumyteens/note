# 条件变量

条件变量是一种用于多线程同步的机制，它允许线程在满足特定条件之前阻塞等待，直到其他线程通知条件已满足。条件变量通常与互斥锁配合使用，用于实现生产者 - 消费者模型等需要线程间协作的场景。

std::condition_variable 提供了以下关键方法实现线程间的等待与通知：

- 等待操作
  - `wait(unique_lock<mutex>& lock)`：释放锁并阻塞当前线程，直到被其他线程唤醒。唤醒后重新获取锁并继续执行
  - `wait(unique_lock<mutex>& lock, Predicate pred)`：带条件的等待，相当于循环检查 pred 条件，直到条件为 true 才返回。这是更安全的用法，可避免虚假唤醒(虚假唤醒: 操作系统可能在没有收到 notify 的情况下唤醒线程)
- 通知操作
  - `notify_one()`：唤醒一个正在等待该条件变量的线程（如果有）
  - `notify_all()`：唤醒所有正在等待该条件变量的线程

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <queue>

// 共享队列（生产者-消费者模型）
std::queue<int> data_queue;
// 互斥锁: 用来保护共享队列
std::mutex mtx;
// 条件变量: 用于线程间通知
std::condition_variable cv;
// 标志位: 是否结束程序
bool stop_flag = false;

// 生产者线程函数: 生成数据并放入队列
void producer(int id) {
    for (int i = 0; i < 5; ++i) {
        // 模拟数据生成耗时
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // 加锁保护共享队列
        std::unique_lock<std::mutex> lock(mtx);

        // 生产数据
        int data = id * 100 + i;
        data_queue.push(data);
        std::cout << "生产者 " << id << " 生产数据: " << data
                  << ", 队列大小: " << data_queue.size() << std::endl;

        // 通知消费者有新数据可用
        cv.notify_one();  // 唤醒一个等待的消费者
    }

    std::cout << "生产者 " << id << " 完成生产" << std::endl;
}

// 消费者线程函数：从队列中获取并处理数据
void consumer(int id) {
    while (!stop_flag) {
        // 加锁（使用unique_lock，条件变量需要灵活控制锁）
        std::unique_lock<std::mutex> lock(mtx);

        // 等待条件满足：队列不为空 或 程序结束
        // wait会释放锁并阻塞，被唤醒后重新获取锁并检查条件
        cv.wait(lock, []{
            return !data_queue.empty() || stop_flag;
        });

        // 如果是程序结束信号，退出循环
        if (stop_flag && data_queue.empty()) {
            break;
        }

        // 处理数据
        int data = data_queue.front();
        data_queue.pop();
        std::cout << "消费者 " << id << " 消费数据: " << data
                  << ", 剩余大小: " << data_queue.size() << std::endl;

        // 解锁（unique_lock会自动管理，此处可省略）
    }

    std::cout << "消费者 " << id << " 退出" << std::endl;
}

int main() {
    // 创建生产者和消费者线程
    std::thread producer1(producer, 1);
    std::thread producer2(producer, 2);
    std::thread consumer1(consumer, 1);
    std::thread consumer2(consumer, 2);

    // 等待生产者完成
    producer1.join();
    producer2.join();

    // 通知消费者所有数据已生产完毕
    {
        std::lock_guard<std::mutex> lock(mtx);
        stop_flag = true;
    }
    cv.notify_all();  // 唤醒所有等待的消费者

    // 等待消费者完成
    consumer1.join();
    consumer2.join();

    std::cout << "所有线程完成工作" << std::endl;
    return 0;
}
```
