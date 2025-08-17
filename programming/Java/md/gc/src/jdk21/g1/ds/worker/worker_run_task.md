# 执行任务

```cpp
// --- src/hotspot/share/gc/shared/workerThread.cpp --- //

void WorkerTaskDispatcher::worker_run_task() {
    // 阻塞当前worker线程, 等待coordinator_distribute_task函数派发任务
    _start_semaphore.wait();

    // 多个worker线程并发修改_started的值, 所以需要原子操作
    const uint worker_id = Atomic::fetch_then_add(&_started, 1u);
    WorkerThread::set_worker_id(worker_id);

    // 执行任务
    GCIdMark gc_id_mark(_task->gc_id());
    _task->work(worker_id);

    // 任务执行完毕, 减少未完成的worker线程计数
    const uint not_finished = Atomic::sub(&_not_finished, 1u);

    if (not_finished == 0) {
        // 所有worker线程都执行完了任务
        // 唤醒coordinator_distribute_task函数阻塞的线程
        // 让coordinator_distribute_task函数继续执行
        _end_semaphore.signal();
    }
}
```
