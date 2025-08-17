# worker 线程的入口

```cpp
// --- src/hotspot/share/gc/shared/workerThread.cpp --- //

void WorkerThread::run() {
    // 设置worker线程的优先级为高
    os::set_priority(this, NearMaxPriority);

    // 不断执行worker线程的任务
    while (true) {
        // 所有worker线程共享同一个_dispatcher对象
        // 使用_dispatcher调度worker线程
        _dispatcher->worker_run_task();
    }
}
```
