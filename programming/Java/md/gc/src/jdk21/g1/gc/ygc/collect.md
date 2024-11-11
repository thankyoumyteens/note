# 执行 GC

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::collect() {
    // Do timing/tracing/statistics/pre- and post-logging/verification work not
    // directly related to the collection. They should not be accounted for in
    // collection work timing.

    // The G1YoungGCTraceTime message depends on collector state, so must come after
    // determining collector state.
    G1YoungGCTraceTime tm(this, _gc_cause);

    // JFR
    // JFR 是 Java Flight Recorder 的缩写，它是 Java 平台的一个性能诊断工具，用于收集应用程序运行时的数据
    G1YoungGCJFRTracerMark jtm(gc_timer_stw(), gc_tracer_stw(), _gc_cause);
    // JStat/MXBeans
    // JStat 是一个监视 Java 虚拟机的命令行工具，它可以用来监视 Java 虚拟机的各种运行时信息
    // MXBeans 是 Java Management Extensions 的一部分，它是一种用于管理和监控 Java 虚拟机的标准 API
    G1YoungGCMonitoringScope ms(monitoring_support(),
                                !collection_set()->candidates()->is_empty() /* all_memory_pools_affected */);
    // Create the heap printer before internal pause timing to have
    // heap information printed as last part of detailed GC log.
    G1HeapPrinterMark hpm(_g1h);
    // Young GC internal pause timing
    G1YoungGCNotifyPauseMark npm(this);

    // 设置worker线程数, 并启动worker线程
    // worker是实际执行GC的工作线程
    set_young_collection_default_active_worker_threads();

    // 在进行其它操作之前, 先等待并发标记线程的根分区扫描执行完成
    // 避免在并发标记线程扫描时, Young GC把对象移走
    wait_for_root_region_scanning();

    G1YoungGCVerifierMark vm(this);
    {
        // 这里是实际开始回收的地方

        // 记录 Young GC 实际开始的时间
        policy()->record_young_collection_start();

        // 选择回收集
        pre_evacuate_collection_set(jtm.evacuation_info());

        // 记录每个worker线程执行GC的结果
        // _g1h G1堆的指针
        // workers()->active_workers() worker线程数
        // collection_set() 回收集
        // _evac_failure_regions 用来记录每个分区是否疏散(evacuation)失败,
        //                       并记录疏散失败的原因, 用来加快 post evacuation 阶段的处理速度
        G1ParScanThreadStateSet per_thread_states(_g1h,
                                                  workers()->active_workers(),
                                                  collection_set(),
                                                  &_evac_failure_regions);

        // 进行 Mixed GC 时, 会有部分老年代分区加入到回收集, 这些老年代分区称为 optional region
        bool may_do_optional_evacuation = collection_set()->optional_region_length() != 0;
        // Actually do the work...
        // 实际执行回收
        evacuate_initial_collection_set(&per_thread_states, may_do_optional_evacuation);

        if (may_do_optional_evacuation) {
            // 回收老年代分区, Young GC 阶段不会执行到这里
            evacuate_optional_collection_set(&per_thread_states);
        }
        // 后续处理工作
        post_evacuate_collection_set(jtm.evacuation_info(), &per_thread_states);

        // Refine the type of a concurrent mark operation now that we did the
        // evacuation, eventually aborting it.
        _concurrent_operation_is_full_mark = policy()->concurrent_operation_is_full_mark("Revise IHOP");

        // Need to report the collection pause now since record_collection_pause_end()
        // modifies it to the next state.
        jtm.report_pause_type(collector_state()->young_gc_pause_type(_concurrent_operation_is_full_mark));

        policy()->record_young_collection_end(_concurrent_operation_is_full_mark, evacuation_failed());
    }
    TASKQUEUE_STATS_ONLY(_g1h->task_queues()->print_and_reset_taskqueue_stats("Oop Queue");)
}
```

## 设置 worker 线程数

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

### 计算要使用的 worker 线程数

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

### 启动 worker 线程

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

## 先等待并发标记线程的根分区扫描执行完成

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::wait_for_root_region_scanning() {
    Ticks start = Ticks::now();
    // 需要阻塞等待并发标记线程扫描完根分区
    // 因为在GC期间会移动对象
    // 所以需要在GC之前确保所有对象都已经被正确扫描
    bool waited = concurrent_mark()->wait_until_root_region_scan_finished();
    Tickspan wait_time;
    if (waited) {
        // 记录等了多久
        wait_time = (Ticks::now() - start);
    }
    phase_times()->record_root_region_scan_wait_time(wait_time.seconds() * MILLIUNITS);
}
```

## 选择回收集

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::pre_evacuate_collection_set(G1EvacInfo *evacuation_info) {
    {
        Ticks start = Ticks::now();
        G1PreEvacuateCollectionSetBatchTask cl;
        G1CollectedHeap::heap()->run_batch_task(&cl);
        phase_times()->record_pre_evacuate_prepare_time_ms((Ticks::now() - start).seconds() * 1000.0);
    }

    // Needs log buffers flushed.
    // 选择回收集
    calculate_collection_set(evacuation_info, policy()->max_pause_time_ms());

    // Please see comment in g1CollectedHeap.hpp and
    // G1CollectedHeap::ref_processing_init() to see how
    // reference processing currently works in G1.
    ref_processor_stw()->start_discovery(false /* always_clear */);

    _evac_failure_regions.pre_collection(_g1h->max_reserved_regions());

    _g1h->gc_prologue(false);

    // Initialize the GC alloc regions.
    // 初始化垃圾回收器分配的分区
    allocator()->init_gc_alloc_regions(evacuation_info);

    {
        Ticks start = Ticks::now();
        rem_set()->prepare_for_scan_heap_roots();
        phase_times()->record_prepare_heap_roots_time_ms((Ticks::now() - start).seconds() * 1000.0);
    }

    {
        G1PrepareEvacuationTask g1_prep_task(_g1h);
        Tickspan task_time = run_task_timed(&g1_prep_task);

        _g1h->set_young_gen_card_set_stats(g1_prep_task.all_card_set_stats());
        _g1h->set_humongous_stats(g1_prep_task.humongous_total(), g1_prep_task.humongous_candidates());

        phase_times()->record_register_regions(task_time.seconds() * 1000.0);
    }

    assert(_g1h->verifier()->check_region_attr_table(), "Inconsistency in the region attributes table.");

#if COMPILER2_OR_JVMCI
    DerivedPointerTable::clear();
#endif

    if (collector_state()->in_concurrent_start_gc()) {
        concurrent_mark()->pre_concurrent_start(_gc_cause);
    }

    evac_failure_injector()->arm_if_needed();
}

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
    // 遍历_mutator_alloc_regions
    // _mutator_alloc_regions保存分配给mutator线程的分区
    // _mutator_alloc_regions的长度是NUMA节点的数量
    // 每一个元素对应一个NUMA内存节点
    for (uint i = 0; i < _num_alloc_regions; i++) {
        // 把分区退休
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
    // _alloc_region指向当前正在分配内存的分区
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
    // 如果是 Young GC 则跳过, 因为Young GC 阶段不会选择老年代分区
    // 根据剩余可用时间选择一部分老年代分区加入回收集
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
    // 根据eden分区数预测eden区域执行GC要耗费时间
    double predicted_eden_time = _policy->predict_young_region_other_time_ms(eden_region_length) +
                                 _policy->predict_eden_copy_time_ms(eden_region_length);
    // 根据用户指定的期望暂停时间计算剩余可用的时间
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

    // 遍历_survivor_gc_alloc_regions
    // _survivor_gc_alloc_regions是垃圾回收器分配的分区, 用来存放幸存者对象
    // _survivor_gc_alloc_regions的长度是NUMA节点的数量
    // 每一个元素对应一个NUMA内存节点
    for (uint i = 0; i < _num_alloc_regions; i++) {
        // 把 _alloc_region 设置成 _dummy_region
        survivor_gc_alloc_region(i)->init();
    }

    // _old_gc_alloc_region也是垃圾回收器分配的分区, 用来存放老年代对象
    _old_gc_alloc_region.init();
    // _old_gc_alloc_region在退休后会咱是放到_retained_old_gc_alloc_region中
    // 如果_retained_old_gc_alloc_region还能用, 就把它重新设置成_old_gc_alloc_region
    reuse_retained_old_region(evacuation_info,
                              &_old_gc_alloc_region,
                              &_retained_old_gc_alloc_region);
}
```

## 实际执行回收

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

## 后续处理工作

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::post_evacuate_collection_set(G1EvacInfo *evacuation_info,
                                                    G1ParScanThreadStateSet *per_thread_states) {
    G1GCPhaseTimes *p = phase_times();

    // Process any discovered reference objects - we have
    // to do this _before_ we retire the GC alloc regions
    // as we may have to copy some 'reachable' referent
    // objects (and their reachable sub-graphs) that were
    // not copied during the pause.
    process_discovered_references(per_thread_states);

    G1STWIsAliveClosure is_alive(_g1h);
    G1KeepAliveClosure keep_alive(_g1h);

    WeakProcessor::weak_oops_do(workers(), &is_alive, &keep_alive, p->weak_phase_times());

    allocator()->release_gc_alloc_regions(evacuation_info);

    post_evacuate_cleanup_1(per_thread_states);

    post_evacuate_cleanup_2(per_thread_states, evacuation_info);

    _evac_failure_regions.post_collection();

    assert_used_and_recalculate_used_equal(_g1h);

    _g1h->rebuild_free_region_list();

    _g1h->record_obj_copy_mem_stats();

    evacuation_info->set_bytes_used(_g1h->bytes_used_during_gc());

    _g1h->prepare_for_mutator_after_young_collection();

    _g1h->gc_epilogue(false);

    _g1h->expand_heap_after_young_collection();
}
```
