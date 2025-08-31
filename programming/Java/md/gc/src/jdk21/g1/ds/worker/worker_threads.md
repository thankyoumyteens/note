# worker 线程集

其它类一般不会直接使用 WorkerThread 类, 而是会通过 WorkerThreads 来使用 worker 线程。

```cpp
// --- src/hotspot/share/gc/shared/workerThread.hpp --- //

class WorkerThreads : public CHeapObj<mtInternal> {
private:
    // 名称, 用来简单描述这些worker线程是干什么的
    const char *const _name;
    // worker线程集合
    WorkerThread **_workers;
    // 最大worker线程数量
    const uint _max_workers;
    // 创建的worker线程数量
    uint _created_workers;
    // 活动的worker线程数量
    uint _active_workers;
    // 任务调度器
    WorkerTaskDispatcher _dispatcher;

    WorkerThread *create_worker(uint name_suffix);

    void set_indirectly_suspendible_threads();

    void clear_indirectly_suspendible_threads();

protected:
    virtual void on_create_worker(WorkerThread *worker) {}

public:
    WorkerThreads(const char *name, uint max_workers);

    void initialize_workers();

    uint max_workers() const { return _max_workers; }

    uint created_workers() const { return _created_workers; }

    uint active_workers() const { return _active_workers; }

    uint set_active_workers(uint num_workers);

    void threads_do(ThreadClosure *tc) const;

    const char *name() const { return _name; }

    // 使用当前活动的worker线程数量执行任务, 函数会等待任务完成后返回
    void run_task(WorkerTask *task);

    // 使用指定的worker线程数量执行任务, 函数会等待任务完成后返回
    void run_task(WorkerTask *task, uint num_workers);
};
```
