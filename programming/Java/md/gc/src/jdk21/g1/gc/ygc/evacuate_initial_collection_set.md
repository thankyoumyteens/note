# 实际执行回收

- 合并堆根阶段(Merge Heap Roots)，G1 从回收集分区中创建一个统一的记忆集，以便后续进行并行处理。这一步骤从记忆集中去除了许多原本需要在后续以更高代价过滤掉的重复项
- 疏散回收集阶段(Evacuate Collection Set)包含了大部分的工作: G1 从根开始移动对象。根的引用是指从回收集外部指向回收集内的引用，这些引用可能来自某些虚拟机内部的数据结构（外部根）、代码（代码根）或 Java 堆的其余部分（堆根）。对于所有根，G1 将它所引用的回收集中的对象复制到其目标位置，并将这些对象的引用作为新的根进行处理，直到没有更多的根为止。这些阶段各自的时间可以通过使用 `-Xlog:gc+phases=debug` 日志记录选项来观察，分别在扩展根扫描（Ext Root Scanning）、代码根扫描（Code Root Scan）、堆根扫描（Scan Heap Roots）和对象复制（Object Copy）子阶段中查看。G1 可能会根据需要重复主要疏散阶段，以处理可选的回收集

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::evacuate_initial_collection_set(G1ParScanThreadStateSet *per_thread_states,
                                                       bool has_optional_evacuation_work) {
    G1GCPhaseTimes *p = phase_times();

    {
        Ticks start = Ticks::now();
        rem_set()->merge_heap_roots(true /* initial_evacuation */);
        p->record_merge_heap_roots_time((Ticks::now() - start).seconds() * 1000.0);
    }

    Tickspan task_time;
    const uint num_workers = workers()->active_workers();

    Ticks start_processing = Ticks::now();
    {
        G1RootProcessor root_processor(_g1h, num_workers);
        G1EvacuateRegionsTask g1_par_task(_g1h,
                                          per_thread_states,
                                          task_queues(),
                                          &root_processor,
                                          num_workers,
                                          has_optional_evacuation_work);
        task_time = run_task_timed(&g1_par_task);
        // Closing the inner scope will execute the destructor for the
        // G1RootProcessor object. By subtracting the WorkerThreads task from the total
        // time of this scope, we get the "NMethod List Cleanup" time. This list is
        // constructed during "STW two-phase nmethod root processing", see more in
        // nmethod.hpp
    }
    Tickspan total_processing = Ticks::now() - start_processing;

    p->record_initial_evac_time(task_time.seconds() * 1000.0);
    p->record_or_add_nmethod_list_cleanup_time((total_processing - task_time).seconds() * 1000.0);

    rem_set()->complete_evac_phase(has_optional_evacuation_work);
}
```

## 合并堆根阶段

```cpp
// --- src/hotspot/share/gc/g1/g1RemSet.cpp --- //

void G1RemSet::merge_heap_roots(bool initial_evacuation) {
    G1CollectedHeap *g1h = G1CollectedHeap::heap();

    {
        Ticks start = Ticks::now();

        // 初始化扫描状态
        _scan_state->prepare_for_merge_heap_roots();

        // 记录时间
        Tickspan total = Ticks::now() - start;
        if (initial_evacuation) {
            g1h->phase_times()->record_prepare_merge_heap_roots_time(total.seconds() * 1000.0);
        } else {
            g1h->phase_times()->record_or_add_optional_prepare_merge_heap_roots_time(total.seconds() * 1000.0);
        }
    }

    WorkerThreads *workers = g1h->workers();
    // 增量回收(回收新生代+老年代分区)时回收集增加的分区数
    size_t const increment_length = g1h->collection_set()->increment_length();

    // worker线程数
    // 增量回收时需要增加worker线程
    uint const num_workers = initial_evacuation ? workers->active_workers() :
                             MIN2(workers->active_workers(), (uint) increment_length);

    {
        // 执行合并堆根任务
        G1MergeHeapRootsTask cl(_scan_state, num_workers, initial_evacuation);
        log_debug(gc, ergo)("Running %s using %u workers for " SIZE_FORMAT " regions",
                            cl.name(), num_workers, increment_length);
        workers->run_task(&cl, num_workers);
    }

    print_merge_heap_roots_stats();
}

class G1RemSetScanState : public CHeapObj<mtGC> {
    void prepare_for_merge_heap_roots() {
        assert(_next_dirty_regions->size() == 0, "next dirty regions must be empty");

        // 重置堆保留分区的扫描状态
        // 0表示这个分区还没有被扫描
        for (size_t i = 0; i < _max_reserved_regions; i++) {
            _card_table_scan_state[i] = 0;
        }

        // memset用来给一块指定内存空间进行赋值
        // 参数1: 指向某一内存空间的指针
        // 参数2: 要填充的值
        // 参数3: 要填充的字节数
        ::memset(_region_scan_chunks, false, _num_total_scan_chunks * sizeof(*_region_scan_chunks));
    }
};
```

### 执行合并堆根任务
