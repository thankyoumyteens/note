# 预备疏散回收集阶段

预备疏散回收集阶段(Pre Evacuate Collection Set)执行一些垃圾回收的准备工作: 断开 mutator 线程与 TLAB 的连接，选择本次垃圾回收的回收集，以及其他一些小的准备工作。

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::pre_evacuate_collection_set(G1EvacInfo *evacuation_info) {
    {
        Ticks start = Ticks::now();
        // 断开 mutator 线程与 TLAB 的连接
        G1PreEvacuateCollectionSetBatchTask cl;
        G1CollectedHeap::heap()->run_batch_task(&cl);
        phase_times()->record_pre_evacuate_prepare_time_ms((Ticks::now() - start).seconds() * 1000.0);
    }

    // 计算回收集
    calculate_collection_set(evacuation_info, policy()->max_pause_time_ms());

    // 处理引用类型
    ref_processor_stw()->start_discovery(false /* always_clear */);

    // 初始化疏散失败的分区数
    _evac_failure_regions.pre_collection(_g1h->max_reserved_regions());

    // 记录发生的GC次数
    _g1h->gc_prologue(false);

    // 初始化垃圾回收器分配的分区
    allocator()->init_gc_alloc_regions(evacuation_info);

    {
        Ticks start = Ticks::now();
        rem_set()->prepare_for_scan_heap_roots();
        phase_times()->record_prepare_heap_roots_time_ms((Ticks::now() - start).seconds() * 1000.0);
    }

    {
        // 记录分区中记忆集的状态, 并把符合条件的大对象加入提前回收的候选分区
        G1PrepareEvacuationTask g1_prep_task(_g1h);
        Tickspan task_time = run_task_timed(&g1_prep_task);

        // 记录统计信息
        _g1h->set_young_gen_card_set_stats(g1_prep_task.all_card_set_stats());
        _g1h->set_humongous_stats(g1_prep_task.humongous_total(), g1_prep_task.humongous_candidates());

        phase_times()->record_register_regions(task_time.seconds() * 1000.0);
    }

    assert(_g1h->verifier()->check_region_attr_table(), "Inconsistency in the region attributes table.");

#if COMPILER2_OR_JVMCI
    DerivedPointerTable::clear();
#endif

    // 是否要开启并发标记
    if (collector_state()->in_concurrent_start_gc()) {
        concurrent_mark()->pre_concurrent_start(_gc_cause);
    }

    evac_failure_injector()->arm_if_needed();
}
```

## 断开 mutator 线程与 TLAB 的连接

```cpp
// run_batch_task 最终会执行到这里
// 调用栈:
// G1PreEvacuateCollectionSetBatchTask::JavaThreadRetireTLABAndFlushLogs::RetireTLABAndFlushLogsClosure::do_thread(Thread *) g1YoungGCPreEvacuateTasks.cpp:60
// G1JavaThreadsListClaimer::apply(ThreadClosure *) g1CollectedHeap.inline.hpp:72
// G1PreEvacuateCollectionSetBatchTask::JavaThreadRetireTLABAndFlushLogs::do_work(unsigned int) g1YoungGCPreEvacuateTasks.cpp:88
// G1BatchedTask::work(unsigned int) g1BatchedTask.cpp:95
// WorkerTaskDispatcher::worker_run_task() workerThread.cpp:74
// WorkerThread::run() workerThread.cpp:210
// Thread::call_run() thread.cpp:217
// thread_native_entry(Thread *) os_bsd.cpp:580

// --- src/hotspot/share/gc/g1/g1YoungGCPreEvacuateTasks.cpp --- //

struct RetireTLABAndFlushLogsClosure : public ThreadClosure {
    void do_thread(Thread *thread) override {
        assert(thread->is_Java_thread(), "must be");
        BarrierSet::barrier_set()->make_parsable((JavaThread *) thread);
        if (UseTLAB) {
            // 退休当前mutator线程的TLAB
            thread->tlab().retire(&_tlab_stats);
        }

        G1DirtyCardQueueSet &qset = G1BarrierSet::dirty_card_queue_set();
        _refinement_stats += qset.concatenate_log_and_stats(thread);
    }
};
```

## 计算回收集

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::calculate_collection_set(G1EvacInfo *evacuation_info, double target_pause_time_ms) {
    // 释放mutator分配的分区
    // 确定回收集之前需要先让当前正在用于分配对象的分区退休(不能再继续用于分配对象)
    // 因为这个分区也可能被选中加入到回收集中
    allocator()->release_mutator_alloc_regions();
    // 确定回收集
    collection_set()->finalize_initial_collection_set(target_pause_time_ms, survivor_regions());
    // 设置JFR信息
    evacuation_info->set_collection_set_regions(collection_set()->region_length() +
                                                collection_set()->optional_region_length());

    concurrent_mark()->verify_no_collection_set_oops();

    if (hr_printer()->is_active()) {
        G1PrintCollectionSetClosure cl(hr_printer());
        collection_set()->iterate(&cl);
        collection_set()->iterate_optional(&cl);
    }
}
```

## 释放 mutator 分配的分区

```cpp

// --- src/hotspot/share/gc/g1/g1Allocator.cpp --- //

void G1Allocator::release_mutator_alloc_regions() {
    // 遍历_mutator_alloc_regions数组
    // _mutator_alloc_regions的长度是NUMA节点的数量
    // 每一个元素对应一个NUMA内存节点
    // _mutator_alloc_regions的每个元素内部的_alloc_region指向当前正在用来分配内存的分区
    for (uint i = 0; i < _num_alloc_regions; i++) {
        // 把分区退休, 并加入回收集
        mutator_alloc_region(i)->release();
        assert(mutator_alloc_region(i)->get() == nullptr, "post-condition");
    }
}

HeapRegion *MutatorAllocRegion::release() {
    // 释放当前正在分配内存的分区
    HeapRegion *ret = G1AllocRegion::release();

    // 释放保留的分配分区
    if (_retained_alloc_region != nullptr) {
        _wasted_bytes += retire_internal(_retained_alloc_region, false);
        _retained_alloc_region = nullptr;
    }
    log_debug(gc, alloc, region)("Mutator Allocation stats, regions: %u, wasted size: " SIZE_FORMAT "%s (%4.1f%%)",
                                 count(),
                                 byte_size_in_proper_unit(_wasted_bytes),
                                 proper_unit_for_byte_size(_wasted_bytes),
                                 percent_of(_wasted_bytes, count() * HeapRegion::GrainBytes));
    return ret;
}

HeapRegion *G1AllocRegion::release() {
    trace("releasing");
    // _alloc_region指向当前正在用于分配内存的分区
    HeapRegion *alloc_region = _alloc_region;
    // 把_alloc_region分区退休, 并加入到回收集
    // 分区的剩余空间不填充dummy对象
    retire(false /* fill_up */);
    assert_alloc_region(_alloc_region == _dummy_region, "post-condition of retire()");
    // 重置_alloc_region指针
    _alloc_region = nullptr;
    trace("released");
    // 返回当前正在分配内存的分区
    return (alloc_region == _dummy_region) ? nullptr : alloc_region;
}
```

## 确定回收集

```cpp
// --- src/hotspot/share/gc/g1/g1CollectionSet.cpp --- //

void G1CollectionSet::finalize_initial_collection_set(double target_pause_time_ms, G1SurvivorRegions *survivor) {
    // 预测新生代分区回收耗时, 返回GC的剩余可用时间
    double time_remaining_ms = finalize_young_part(target_pause_time_ms, survivor);
    // 根据剩余可用时间选择一部分老年代分区加入回收集
    // (如果是 Young GC 则跳过, 因为Young GC 阶段不会选择老年代分区)
    finalize_old_part(time_remaining_ms);
}

double G1CollectionSet::finalize_young_part(double target_pause_time_ms, G1SurvivorRegions *survivors) {
    Ticks start_time = Ticks::now();

    finalize_incremental_building();

    guarantee(target_pause_time_ms > 0.0,
              "target_pause_time_ms = %1.6lf should be positive", target_pause_time_ms);

    // 此时卡表中的脏卡片的数量
    size_t pending_cards = _policy->pending_cards_at_gc_start();

    log_trace(gc, ergo, cset)("Start choosing CSet. Pending cards: " SIZE_FORMAT " target pause time: %1.2fms",
                              pending_cards, target_pause_time_ms);

    // eden分区数量
    uint eden_region_length = _g1h->eden_regions_count();
    // 上一次垃圾回收产生的survivor分区数量
    uint survivor_region_length = survivors->length();
    // 保存到G1CollectionSet对象的成员变量中
    init_region_lengths(eden_region_length, survivor_region_length);

    verify_young_cset_indices();

    // 根据pending_cards预测执行GC要耗费的基础时间
    double predicted_base_time_ms = _policy->predict_base_time_ms(pending_cards);
    // 根据eden分区数预测eden区执行GC要耗费的时间
    double predicted_eden_time = _policy->predict_young_region_other_time_ms(eden_region_length) +
                                 _policy->predict_eden_copy_time_ms(eden_region_length);
    // 根据用户指定的暂停时间目标计算剩余可用的时间
    double remaining_time_ms = MAX2(target_pause_time_ms - (predicted_base_time_ms + predicted_eden_time), 0.0);

    log_trace(gc, ergo, cset)("Added young regions to CSet. Eden: %u regions, Survivors: %u regions, "
                              "predicted eden time: %1.2fms, predicted base time: %1.2fms, target pause time: %1.2fms, remaining time: %1.2fms",
                              eden_region_length, survivor_region_length,
                              predicted_eden_time, predicted_base_time_ms, target_pause_time_ms, remaining_time_ms);

    // 把所有survivor分区转换为eden分区
    survivors->convert_to_eden();

    phase_times()->record_young_cset_choice_time_ms((Ticks::now() - start_time).seconds() * 1000.0);
    // 返回GC的剩余可用时间
    return remaining_time_ms;
}
```

## 初始化垃圾回收器分配的分区

```cpp
// --- src/hotspot/share/gc/g1/g1Allocator.cpp --- //

void G1Allocator::init_gc_alloc_regions(G1EvacInfo *evacuation_info) {
    assert_at_safepoint_on_vm_thread();

    _survivor_is_full = false;
    _old_is_full = false;

    // 遍历_survivor_gc_alloc_regions数组
    // _survivor_gc_alloc_regions的长度是NUMA节点的数量
    // 每一个元素对应一个NUMA内存节点
    // _survivor_gc_alloc_regions的每个元素内部的_alloc_region指向垃圾回收器分配的分区,
    // 用来存放幸存者对象
    for (uint i = 0; i < _num_alloc_regions; i++) {
        // 把 _alloc_region 设置成 _dummy_region
        survivor_gc_alloc_region(i)->init();
    }

    // _old_gc_alloc_region内部的_alloc_region指向垃圾回收器分配的分区, 用来存放老年代对象
    // 把_old_gc_alloc_region 的_alloc_region初始化成_dummy_region
    _old_gc_alloc_region.init();
    // _old_gc_alloc_region内部指向的分区在退休后会暂时放到_retained_old_gc_alloc_region中
    // 如果_retained_old_gc_alloc_region还能用, 就让_old_gc_alloc_region重新指向它
    reuse_retained_old_region(evacuation_info,
                              &_old_gc_alloc_region,
                              &_retained_old_gc_alloc_region);
}

void G1Allocator::reuse_retained_old_region(G1EvacInfo *evacuation_info,
                                            OldGCAllocRegion *old,
                                            HeapRegion **retained_old) {
    HeapRegion *retained_region = *retained_old;
    *retained_old = nullptr;

    // 如果retained_region符合下面的要求, 就让_old_gc_alloc_region重新指向它
    // 1. retained_region不在回收集中
    // 2. retained_region没满
    // 3. retained_region不是空的
    // 4. retained_region不是大对象分区
    if (retained_region != nullptr &&
        !retained_region->in_collection_set() &&
        !(retained_region->top() == retained_region->end()) &&
        !retained_region->is_empty() &&
        !retained_region->is_humongous()) {
        // retained_region退休后会加入_old_set
        // 现在把它从_old_set集合中移除
        _g1h->old_set_remove(retained_region);
        // 让_old_gc_alloc_region重新指向retained_region
        old->set(retained_region);
        _g1h->hr_printer()->reuse(retained_region);
        evacuation_info->set_alloc_regions_used_before(retained_region->used());
    }
}
```

## 记录分区中记忆集的状态, 并把符合条件的大对象加入提前回收的候选分区

```cpp
// --- src/hotspot/share/gc/g1/heapRegionManager.cpp --- //

// run_task_timed最终会调用到这里
// 多个worker线程并行处理
void
HeapRegionManager::par_iterate(HeapRegionClosure *blk, HeapRegionClaimer *hrclaimer, const uint start_index) const {
    const uint n_regions = hrclaimer->n_regions();
    for (uint count = 0; count < n_regions; count++) {
        // 要认领的分区索引
        const uint index = (start_index + count) % n_regions;
        assert(index < n_regions, "sanity");
        // 如果分区不是active状态，则跳过
        if (!is_available(index)) {
            continue;
        }
        HeapRegion *r = _regions.get_by_index(index);
        // 如果这个分区被其它worker线程认领了，则跳过
        if (hrclaimer->is_region_claimed(index)) {
            continue;
        }
        // 尝试认领这个分区(CAS操作)
        if (!hrclaimer->claim_region(index)) {
            // 如果认领失败，则跳过
            continue;
        }
        // 认领成功
        // 记录分区中记忆集的状态
        // 将符合条件的大对象加入提前回收的候选分区
        bool res = blk->do_heap_region(r);
        if (res) {
            return;
        }
    }
}

// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

class G1PrepareEvacuationTask : public WorkerTask {
    class G1PrepareRegionsClosure : public HeapRegionClosure {
    public:
        virtual bool do_heap_region(HeapRegion *hr) {
            // 准备进行扫描
            _g1h->rem_set()->prepare_region_for_scan(hr);

            // 收集采样信息
            sample_card_set_size(hr);

            // 检查是否是大对象分区的第一个分区, 如果不是则为true
            if (!hr->is_starts_humongous()) {
                // 记录当前分区的记忆集是否被跟踪
                _g1h->register_region_with_region_attr(hr);
                return false;
            }

            // 处理大对象分区的第一个分区
            uint index = hr->hrm_index();
            // 判断是否加入大对象候选分区(不在回收集中, 但是也要在当前GC中处理)
            if (humongous_region_is_candidate(hr)) {
                // 标记这个分区是一个大对象候选分区
                _g1h->register_humongous_candidate_region_with_region_attr(index);
                _worker_humongous_candidates++;
                // 后续会处理这些分区的记忆集
            } else {
                // 记录当前分区的记忆集是否被跟踪
                _g1h->register_region_with_region_attr(hr);
            }
            log_debug(gc, humongous)(
                    "Humongous region %u (object size %zu @ " PTR_FORMAT ") remset %zu code roots %zu marked %d reclaim candidate %d type array %d",
                    index,
                    cast_to_oop(hr->bottom())->size() * HeapWordSize,
                    p2i(hr->bottom()),
                    hr->rem_set()->occupied(),
                    hr->rem_set()->code_roots_list_length(),
                    _g1h->concurrent_mark()->mark_bitmap()->is_marked(hr->bottom()),
                    _g1h->is_humongous_reclaim_candidate(index),
                    cast_to_oop(hr->bottom())->is_typeArray()
            );
            _worker_humongous_total++;

            return false;
        }

        G1MonotonicArenaMemoryStats card_set_stats() const {
            return _card_set_stats;
        }
    };
};

class G1PrepareEvacuationTask : public WorkerTask {
    class G1PrepareRegionsClosure : public HeapRegionClosure {
        void sample_card_set_size(HeapRegion *hr) {
            if (hr->is_young() || hr->is_starts_humongous()) {
                _card_set_stats.add(hr->rem_set()->card_set_memory_stats());
            }
        }

        bool humongous_region_is_candidate(HeapRegion *region) const {
            assert(region->is_starts_humongous(), "Must start a humongous object");

            // region是大对象分区的第一个分区

            // 获取分区中的第一个对象(分区中第一个对象的起始地址和分区的起始地址是相同的)
            oop obj = cast_to_oop(region->bottom());

            // 检查这个大对象

            if (_g1h->is_obj_dead(obj, region)) {
                return false;
            }

            // 判断分区的记忆集是否更新完成
            if (!region->rem_set()->is_complete()) {
                return false;
            }
            // 判断是否要提前回收(Eager Reclaim)这个大对象
            // is_typeArray()判断对象是不是原始类型的数组
            // 对于原始类型的大数组，只要这些大数组不再被其他对象引用, G1在任何GC停顿(包括Young GC)都会尝试进行回收
            return obj->is_typeArray() &&
                   _g1h->is_potential_eager_reclaim_candidate(region);
        }
    };
};

// --- src/hotspot/share/gc/g1/g1RemSet.cpp --- //

void G1RemSet::prepare_region_for_scan(HeapRegion *r) {
    // 获取当前分区的索引
    uint hrm_index = r->hrm_index();

    r->prepare_remset_for_scan();

    // Only update non-collection set old regions, others must have already been set
    // to null (don't scan) in the initialization.
    if (r->in_collection_set()) {
        // _scan_top数组中, 索引为hrm_index的元素应该为nullptr
        assert_scan_top_is_null(hrm_index);
    } else if (r->is_old_or_humongous()) {
        // 把_scan_top数组中, 索引为hrm_index的元素的值设置为当前分区的top指针
        // 当前分区的top指针指向下一个可分配对象的地址
        _scan_state->set_scan_top(hrm_index, r->top());
    } else {
        // _scan_top数组中, 索引为hrm_index的元素应该为nullptr
        assert_scan_top_is_null(hrm_index);
        assert(r->is_free(),
               "Region %u should be free region but is %s", hrm_index, r->get_type_str());
    }
}
```
