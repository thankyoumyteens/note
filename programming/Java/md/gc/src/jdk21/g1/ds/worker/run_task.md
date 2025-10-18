# run_task

其它类会通过调用 run_task 函数来让 worker 线程执行指定的任务

```cpp
// --- src/hotspot/share/gc/shared/workerThread.cpp --- //

void WorkerThreads::run_task(WorkerTask *task, uint num_workers) {
    // 启动num_workers个worker线程
    WithActiveWorkers with_active_workers(this, num_workers);
    // 执行任务
    run_task(task);
}

void WorkerThreads::run_task(WorkerTask *task) {
    set_indirectly_suspendible_threads();
    // 分发任务
    _dispatcher.coordinator_distribute_task(task, _active_workers);
    clear_indirectly_suspendible_threads();
}
```
