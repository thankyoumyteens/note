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
        G1CollectedHeap *g1h = G1CollectedHeap::heap();
        G1GCPhaseTimes *p = g1h->phase_times();

        G1GCPhaseTimes::GCParPhases merge_remset_phase = _initial_evacuation ?
                                                         G1GCPhaseTimes::MergeRS :
                                                         G1GCPhaseTimes::OptMergeRS;

        {
            G1GCParPhaseTimesTracker x(p, merge_remset_phase, worker_id,
                                       !_initial_evacuation /* allow_multiple_record */);

            {
                // 处理需要提前回收的部分大对象分区
                // _fast_reclaim_handled 控制只能由一个worker线程处理大对象分区
                if (_initial_evacuation &&
                    g1h->has_humongous_reclaim_candidates() &&
                    !_fast_reclaim_handled &&
                    !Atomic::cmpxchg(&_fast_reclaim_handled, false, true)) {

                    G1GCParPhaseTimesTracker subphase_x(p, G1GCPhaseTimes::MergeER, worker_id);

                    // 把候选的大对象分区的记忆集合并到卡表中
                    G1FlushHumongousCandidateRemSets cl(_scan_state);
                    // 遍历堆中的分区, 内部会调用cl的do_heap_region_index函数
                    g1h->heap_region_iterate(&cl);
                    G1MergeCardSetStats stats = cl.stats();

                    for (uint i = 0; i < G1GCPhaseTimes::MergeRSContainersSentinel; i++) {
                        p->record_or_add_thread_work_item(merge_remset_phase, worker_id, stats.merged(i), i);
                    }
                }
            }
TODO
    }
};
```

## 遍历堆中的分区

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

void G1CollectedHeap::heap_region_iterate(HeapRegionIndexClosure *cl) const {
    _hrm.iterate(cl);
}

// --- src/hotspot/share/gc/g1/heapRegionManager.cpp --- //

void HeapRegionManager::iterate(HeapRegionIndexClosure *blk) const {
    uint len = reserved_length();

    for (uint i = 0; i < len; i++) {
        if (!is_available(i)) {
            continue;
        }
        bool res = blk->do_heap_region_index(i);
        if (res) {
            blk->set_incomplete();
            return;
        }
    }
}
```

## 把候选的大对象分区的记忆集合并到卡表中

```cpp
class G1FlushHumongousCandidateRemSets : public HeapRegionIndexClosure {
    bool do_heap_region_index(uint region_index) override {
        G1CollectedHeap *g1h = G1CollectedHeap::heap();

        // 确保这个分区是当前回收集的候选分区
        if (!g1h->region_attr(region_index).is_humongous_candidate()) {
            return false;
        }

        // 获取当前分区
        HeapRegion *r = g1h->region_at(region_index);
        if (r->rem_set()->is_empty()) {
            return false;
        }

        guarantee(r->rem_set()->occupancy_less_or_equal_than(G1EagerReclaimRemSetThreshold),
                    "Found a not-small remembered set here. This is inconsistent with previous assumptions.");

        // 把候选的大对象分区的记忆集合并到卡表中
        _cl.merge_card_set_for_region(r);

        r->rem_set()->clear_locked(true /* only_cardset */);
        r->rem_set()->set_state_complete();
#ifdef ASSERT
        G1HeapRegionAttr region_attr = g1h->region_attr(region_index);
        assert(region_attr.remset_is_tracked(), "must be");
#endif
        assert(r->rem_set()->is_empty(), "At this point any humongous candidate remembered set must be empty.");

        return false;
    }
};

// --- src/hotspot/share/gc/g1/g1RemSet.cpp --- //

class G1MergeCardSetClosure : public HeapRegionClosure {
    void merge_card_set_for_region(HeapRegion *r) {
        assert(r->in_collection_set() || r->is_starts_humongous(), "must be");

        HeapRegionRemSet *rem_set = r->rem_set();
        if (!rem_set->is_empty()) {
            // 遍历记忆集, 合并到卡表
            // 就是把记忆集中记录的卡片在卡表中标记为脏
            rem_set->iterate_for_merge(*this);
        }
    }
};
```

## 遍历回收集中的分区

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

void G1CollectedHeap::collection_set_iterate_increment_from(HeapRegionClosure *cl,
                                                            HeapRegionClaimer *hr_claimer,
                                                            uint worker_id) {
    _collection_set.iterate_incremental_part_from(cl, hr_claimer, worker_id);
}

// --- src/hotspot/share/gc/g1/g1CollectionSet.cpp --- //

void G1CollectionSet::iterate_incremental_part_from(HeapRegionClosure *cl,
                                                    HeapRegionClaimer *hr_claimer,
                                                    uint worker_id) const {
    iterate_part_from(cl, hr_claimer, _inc_part_start, increment_length(), worker_id);
}

void G1CollectionSet::iterate_part_from(HeapRegionClosure *cl,
                                        HeapRegionClaimer *hr_claimer,
                                        size_t offset,
                                        size_t length,
                                        uint worker_id) const {
    _g1h->par_iterate_regions_array(cl,
                                    hr_claimer,
                                    // 回收集就是分区索引的数组
                                    &_collection_set_regions[offset],
                                    length,
                                    worker_id);
}

// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

void G1CollectedHeap::par_iterate_regions_array(HeapRegionClosure *cl,
                                                HeapRegionClaimer *hr_claimer,
                                                const uint regions[],
                                                size_t length,
                                                uint worker_id) const {
    assert_at_safepoint();
    // length是要处理的回收集数组的长度
    if (length == 0) {
        return;
    }
    uint total_workers = workers()->active_workers();

    // 每个worker线程都会从不同的位置开始处理, 但最终每个worker线程最终都会尝试处理数组内所有的分区
    // 比如: worker_id = 2, length = 10, total_workers = 5
    // worker_id = 2的线程会从回收集数组中索引为2的分区(第3个分区)开始处理,
    // 处理完第3个分区后, 继续处理后续的分区（如果hr_claimer不为空, 则会判断某个分区是否正在被其它worker线程处理, 如果是则跳过该分区)
    // 到达数组末尾后, 再从数组开头继续处理, 直到走过一圈再回到start_pos为止
    size_t start_pos = (worker_id * length) / total_workers;
    size_t cur_pos = start_pos;

    do {
        uint region_idx = regions[cur_pos];
        // 在合并堆根阶段, hr_claimer传入的是nullptr
        if (hr_claimer == nullptr || hr_claimer->claim_region(region_idx)) {
            HeapRegion *r = region_at(region_idx);
            bool result = cl->do_heap_region(r);
            guarantee(!result, "Must not cancel iteration");
        }

        cur_pos++;
        if (cur_pos == length) {
            cur_pos = 0;
        }
    } while (cur_pos != start_pos);
}
```

## G1MergeCardSetClosure
