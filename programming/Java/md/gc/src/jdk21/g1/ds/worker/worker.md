# worker 线程

```cpp
// --- src/hotspot/share/gc/shared/workerThread.hpp --- //

class WorkerThread : public NamedThread {
    friend class WorkerTaskDispatcher;

private:
    // worker线程的id
    // #define THREAD_LOCAL __thread
    // __thread 是 GCC 和 Clang 等编译器支持的线程局部存储关键字，用于声明线程局部变量
    // 线程局部变量与全局变量类似，但每个线程有自己的副本，不同线程对该变量的修改不会相互影响
    // 线程局部变量的访问通常比全局变量略慢，因为需要通过线程 ID 来定位变量
    // 但与使用锁保护的共享变量相比，性能通常更好
    static THREAD_LOCAL uint _worker_id;

    // 用于调度worker线程
    WorkerTaskDispatcher *const _dispatcher;

    static void set_worker_id(uint worker_id) { _worker_id = worker_id; }

public:
    static uint worker_id() { return _worker_id; }

    WorkerThread(const char *name_prefix, uint which, WorkerTaskDispatcher *dispatcher);

    bool is_Worker_thread() const override { return true; }

    const char *type_name() const override { return "WorkerThread"; }

    // worker线程的入口
    void run() override;
};
```
