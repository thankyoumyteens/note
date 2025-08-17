# WorkerTaskDispatcher

```cpp
// --- src/hotspot/share/gc/shared/workerThread.hpp --- //

// 使用信号量实现Worker线程的调度
class WorkerTaskDispatcher {
    // 要派发给worker线程的任务
    WorkerTask *_task;

    // 正在执行任务的worker线程数量
    volatile uint _started;
    // 任务未执行完的worker线程数量
    volatile uint _not_finished;

    // 用于唤醒worker线程的信号量
    Semaphore _start_semaphore;
    // 用于通知WorkerTaskDispatcher所有的worker线程都完成了任务
    Semaphore _end_semaphore;

public:
    WorkerTaskDispatcher();

    // 分发任务
    // 将单个任务分发给多个(num_workers个)worker线程, 并等待所有worker线程完成任务
    void coordinator_distribute_task(WorkerTask *task, uint num_workers);

    // 执行任务
    // 等待任务, 并执行这个任务
    void worker_run_task();
};
```
