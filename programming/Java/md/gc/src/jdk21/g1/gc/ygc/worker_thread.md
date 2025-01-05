# worker 线程

```cpp
// --- src/hotspot/share/gc/shared/workerThread.cpp --- //

// worker线程的入口
void WorkerThread::run() {
    // 设置worker线程的优先级为高
    os::set_priority(this, NearMaxPriority);

    // 不断执行worker线程的任务
    while (true) {
        // WorkerTaskDispatcher *const _dispatcher;
        // 所有worker线程共享同一个_dispatcher对象
        _dispatcher->worker_run_task();
    }
}
```

## WorkerTaskDispatcher

```cpp
// --- src/hotspot/share/gc/shared/workerThread.hpp --- //

// 使用信号量实现Worker线程的调度
class WorkerTaskDispatcher {
    // 要派发给WorkerThreads的任务
    WorkerTask *_task;

    volatile uint _started;
    volatile uint _not_finished;

    // 用于启动任务的信号量, 初始值为0
    Semaphore _start_semaphore;
    // 用于通知协调器所有的worker都完成了, 初始值为0
    Semaphore _end_semaphore;
};
```

## 信号量

```cpp
// --- src/hotspot/share/runtime/semaphore.hpp --- //

class Semaphore : public CHeapObj<mtSynchronizer> {
    // 不同的操作系统使用不同的实现
    SemaphoreImpl _impl;

    NONCOPYABLE(Semaphore);

public:
    Semaphore(uint value = 0) : _impl(value) {}

    ~Semaphore() {}

    // signal 函数(V操作)用于释放一个资源
    // 当一个进程调用 signal 函数时, 它会将信号量的值加 1
    // 如果有其他进程因为调用 wait 函数而处于等待状态(即信号量的值为 0 时等待), 
    // 那么这些等待的进程中的一个会被唤醒, 允许它继续执行, 以获取刚刚释放的资源
    void signal(uint count = 1) { _impl.signal(count); }

    // wait 函数(P操作)主要用于请求一个资源
    // 当一个进程调用 wait 函数时, 它会检查信号量的值
    // 如果信号量的值大于 0, 那么进程可以继续执行, 并将信号量的值减 1, 表示占用了一个资源
    // 如果信号量的值等于 0, 那么调用 wait 函数的进程会被阻塞, 进入等待状态, 直到信号量的值大于 0
    // 这种阻塞机制确保了在资源有限的情况下, 多个进程能够有序地访问资源
    void wait() { _impl.wait(); }

    // trywait 函数是一种非阻塞的尝试获取资源的操作
    // 它和 wait 函数类似, 也会检查信号量的值
    // 如果信号量的值大于 0, 那么它会将信号量的值减 1, 并且函数返回成功, 表示获取资源成功
    // 但是, 与 wait 函数不同的是, 如果信号量的值等于 0, trywait 函数不会阻塞进程, 
    // 而是直接返回一个表示资源不可用的状态(通常是返回一个错误码或者特定的值), 
    // 这样进程可以继续执行其他任务, 而不是进入等待状态
    bool trywait() { return _impl.trywait(); }

    void wait_with_safepoint_check(JavaThread *thread);
};
```

## 执行任务

worker 线程会不停地调用 `_dispatcher->worker_run_task()` 函数, 而 worker_run_task 函数一开始会获取`_start_semaphore` 信号量资源, 如果资源为 0, 则表示没有需要执行的任务 worker_run_task 会阻塞等待。

执行任务的流程:

1. 任务的发起方会调用 coordinator_distribute_task 函数给 `_start_semaphore` 信号量增加资源, 有几个 worker 线程需要并行执行就增加几个资源, 之后会开始等待 `_end_semaphore` 信号量的资源
2. `_start_semaphore` 信号量资源大于 0 之后, 每个 worker 线程中的 worker_run_task 函数从阻塞中恢复执行, 并开始处理任务 `_task`, 等到所有任务执行完毕后, 增加 1 个 `_end_semaphore` 信号量的资源
3. `_end_semaphore` 信号量资源大于 0 之后, coordinator_distribute_task 函数从阻塞中恢复执行(做一些清理工作)

```cpp
// --- src/hotspot/share/gc/shared/workerThread.cpp --- //

void WorkerTaskDispatcher::coordinator_distribute_task(WorkerTask *task, uint num_workers) {
    _task = task; // 设置要执行的任务
    _not_finished = num_workers;

    // 唤醒num_workers个worker线程来执行任务
    _start_semaphore.signal(num_workers);

    // 等待所有worker线程执行完毕
    _end_semaphore.wait();

    assert(_not_finished == 0, "%d not finished workers?", _not_finished);
    _task = nullptr;
    _started = 0;
}

// 因为worker线程是有多个的,
// 所以在WorkerThread::run函数中执行的worker_run_task函数是多个并行执行的
void WorkerTaskDispatcher::worker_run_task() {
    // 等待协调器派发任务, 即调用_start_semaphore.signal()增加资源
    _start_semaphore.wait();

    // 多个worker线程并发修改_started的值, 所以需要原子操作
    const uint worker_id = Atomic::fetch_then_add(&_started, 1u);
    WorkerThread::set_worker_id(worker_id);

    // 执行任务
    GCIdMark gc_id_mark(_task->gc_id());
    _task->work(worker_id);

    // 任务执行完毕, 减少未完成任务数
    const uint not_finished = Atomic::sub(&_not_finished, 1u);

    if (not_finished == 0) {
        // 最后一个worker线程执行完毕后唤醒协调器, 即增加 1 个_end_semaphore信号量的资源
        _end_semaphore.signal();
    }
}
```
