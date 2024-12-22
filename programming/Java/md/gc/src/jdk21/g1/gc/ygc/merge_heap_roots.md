# 合并堆根阶段

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

## 执行合并堆根任务

```cpp
// --- src/hotspot/share/gc/g1/g1RemSet.cpp --- //

class G1MergeHeapRootsTask : public WorkerTask {
public:
    virtual void work(uint worker_id) {

    }
};
```
