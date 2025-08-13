# this_thread

std::this_thread 是一个命名空间，定义在 `<thread>` 头文件中，提供了一系列与当前线程相关的工具函数。这些函数用于用于控制当前执行线程的行为，如休眠、获取线程 ID 等。

std::this_thread 的主要函数:

1. get_id()
   - 功能：返回当前线程的唯一标识符（std::thread::id 类型）
   - 用途：用于线程标识、日志记录、调试等场景
   - 示例：`std::thread::id tid = std::this_thread::get_id();`
2. sleep_for(duration)
   - 功能：使当前线程休眠指定的时间间隔
   - 参数：duration 是 `<chrono>` 库中的时间间隔类型（如 seconds、milliseconds 等）
   - 用途：模拟工作负载、控制执行节奏、等待资源等
   - 示例：`std::this_thread::sleep_for(std::chrono::seconds(2));`（休眠 2 秒）
3. sleep_until(time_point)
   - 功能：使当前线程休眠直到指定的时间点
   - 参数：time_point 是 `<chrono>` 库中的时间点类型（如 system_clock::time_point）
   - 用途：需要在特定时间点唤醒线程的场景（如定时任务）
   - 示例：`std::this_thread::sleep_until(system_clock::now() + 1s);`（1 秒后唤醒）
4. yield()
   - 功能：当前线程主动放弃 CPU 时间片，允许其他线程运行
   - 用途：在忙等待中减少 CPU 占用，提高多线程效率
   - 示例：`std::this_thread::yield();`
