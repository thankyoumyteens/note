# 设置 worker 线程

1. 计算本次 GC 需要多少线程并行处理
2. 启动这些线程

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::set_young_collection_default_active_worker_threads() {
    // 计算要使用的worker线程数
    // max_workers 在G1堆初始化时被设置成JVM参数ParallelGCThreads指定的值(不指定则是0)
    // active_workers 默认为0
    // number_of_non_daemon_threads 用于记录JVM中不是守护线程的Java线程数
    uint active_workers = WorkerPolicy::calc_active_workers(workers()->max_workers(),
                                                            workers()->active_workers(),
                                                            Threads::number_of_non_daemon_threads());
    // 启动worker线程
    active_workers = workers()->set_active_workers(active_workers);
    log_info(gc, task)("Using %u workers of %u for evacuation", active_workers, workers()->max_workers());
}
```

## 计算要使用的 worker 线程数

```cpp
// --- src/hotspot/share/gc/shared/workerPolicy.cpp --- //

uint WorkerPolicy::calc_active_workers(uintx total_workers,
                                       uintx active_workers,
                                       uintx application_workers) {
    // 如果用户通过JVM参数ParallelGCThreads指定了GC线程的数量, 则直接使用

    // JVM参数UseDynamicNumberOfGCThreads表示动态改变GC线程数
    // 如果是false, 则使用所有的worker线程

    uint new_active_workers;
    if (!UseDynamicNumberOfGCThreads || !FLAG_IS_DEFAULT(ParallelGCThreads)) {
        new_active_workers = total_workers;
    } else {
        uintx min_workers = (total_workers == 1) ? 1 : 2;
        // 计算需要多少worker线程
        new_active_workers = calc_default_active_workers(total_workers,
                                                         min_workers,
                                                         active_workers,
                                                         application_workers);
    }
    assert(new_active_workers > 0, "Always need at least 1");
    return new_active_workers;
}

// 计算规则:
//   根据Java线程数计算需要的GC线程数
//   根据堆的大小计算需要的GC线程数
//   取二者最大值
uint WorkerPolicy::calc_default_active_workers(uintx total_workers,
                                               const uintx min_workers,
                                               uintx active_workers,
                                               uintx application_workers) {

    uintx new_active_workers = total_workers;
    uintx prev_active_workers = active_workers;
    uintx active_workers_by_JT = 0;
    uintx active_workers_by_heap_size = 0;

    // 根据Java线程数计算需要的GC线程数
    // GCWorkersPerJavaThread的值是2
    // JT: Java Thread
    active_workers_by_JT =
            MAX2((uintx) GCWorkersPerJavaThread * application_workers,
                 min_workers);

    // 根据堆的大小计算需要的GC线程数
    active_workers_by_heap_size =
            MAX2((size_t) 2U, Universe::heap()->capacity() / HeapSizePerGCThread);

    // 取二者最大值
    uintx max_active_workers =
            MAX2(active_workers_by_JT, active_workers_by_heap_size);

    new_active_workers = MIN2(max_active_workers, (uintx) total_workers);

    // 如果新的worker线程数小于之前的worker线程数, 则稍微增加一些新的worker线程数
    // 比如 new_active_workers = 5, prev_active_workers = 10
    // 则调整后 new_active_workers = (5 + 10) / 2 = 7
    if (new_active_workers < prev_active_workers) {
        new_active_workers =
                MAX2(min_workers, (prev_active_workers + new_active_workers) / 2);
    }

    assert(min_workers <= total_workers, "Minimum workers not consistent with total workers");
    assert(new_active_workers >= min_workers, "Minimum workers not observed");
    assert(new_active_workers <= total_workers, "Total workers not observed");

    log_trace(gc, task)("WorkerPolicy::calc_default_active_workers() : "
                        "active_workers(): " UINTX_FORMAT "  new_active_workers: " UINTX_FORMAT "  "
                        "prev_active_workers: " UINTX_FORMAT "\n"
                        " active_workers_by_JT: " UINTX_FORMAT "  active_workers_by_heap_size: " UINTX_FORMAT,
                        active_workers, new_active_workers, prev_active_workers,
                        active_workers_by_JT, active_workers_by_heap_size);
    assert(new_active_workers > 0, "Always need at least 1");
    return new_active_workers;
}
```

## 启动 worker 线程

```cpp
// --- src/hotspot/share/gc/shared/workerThread.cpp --- //

uint WorkerThreads::set_active_workers(uint num_workers) {
    assert(num_workers > 0 && num_workers <= _max_workers,
           "Invalid number of active workers %u (should be 1-%u)",
           num_workers, _max_workers);

    while (_created_workers < num_workers) {
        // 当前worker线程数小于需要的worker线程数
        // 创建新的worker线程
        WorkerThread *const worker = create_worker(_created_workers);
        if (worker == nullptr) {
            log_error(gc, task)("Failed to create worker thread");
            break;
        }

        _workers[_created_workers] = worker;
        _created_workers++;
    }

    _active_workers = MIN2(_created_workers, num_workers);

    log_trace(gc, task)("%s: using %d out of %d workers", _name, _active_workers, _max_workers);

    return _active_workers;
}

WorkerThread *WorkerThreads::create_worker(uint name_suffix) {
    if (is_init_completed() && InjectGCWorkerCreationFailure) {
        return nullptr;
    }

    WorkerThread *const worker = new WorkerThread(_name, name_suffix, &_dispatcher);

    // 通过操作系统的系统调用创建worker线程
    if (!os::create_thread(worker, os::gc_thread)) {
        delete worker;
        return nullptr;
    }

    on_create_worker(worker);

    os::start_thread(worker);

    return worker;
}
```
