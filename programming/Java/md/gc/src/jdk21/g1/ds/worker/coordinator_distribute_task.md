# 分发任务

```cpp
// --- src/hotspot/share/gc/shared/workerThread.cpp --- //

void WorkerTaskDispatcher::coordinator_distribute_task(WorkerTask *task, uint num_workers) {
    // 设置要执行的任务
    _task = task;
    // 任务未执行完的worker线程数量
    _not_finished = num_workers;

    // 唤醒num_workers个worker线程来执行任务
    _start_semaphore.signal(num_workers);

    // 阻塞当前线程(执行coordinator_distribute_task函数的线程), 等待所有worker线程执行完毕
    // worker_run_task函数在执行完任务后会调用signal释放该信号量
    _end_semaphore.wait();

    // 确保所有工作线程都已完成
    assert(_not_finished == 0, "%d not finished workers?", _not_finished);
    _task = nullptr;
    // 正在执行任务的worker线程数量
    _started = 0;
}
```
