# 执行 GC

一次垃圾回收由四个阶段组成:

- 预备疏散回收集阶段(Pre Evacuate Collection Set)执行一些垃圾回收的准备工作: 断开 mutator 线程与 TLAB 的连接，选择本次垃圾回收的回收集，以及其他一些小的准备工作
- 合并堆根阶段(Merge Heap Roots)，G1 从回收集分区中创建一个统一的记忆集，以便后续进行并行处理。这一步骤从记忆集中去除了许多原本需要在后续以更高代价过滤掉的重复项
- 疏散回收集阶段(Evacuate Collection Set)包含了大部分的工作: G1 从根开始移动对象。根的引用是指从回收集外部指向回收集内的引用，这些引用可能来自某些虚拟机内部的数据结构（外部根）、代码（代码根）或 Java 堆的其余部分（堆根）。对于所有根，G1 将它所引用的回收集中的对象复制到其目标位置，并将这些对象的引用作为新的根进行处理，直到没有更多的根为止。这些阶段各自的时间可以通过使用 `-Xlog:gc+phases=debug` 日志记录选项来观察，分别在扩展根扫描（Ext Root Scanning）、代码根扫描（Code Root Scan）、堆根扫描（Scan Heap Roots）和对象复制（Object Copy）子阶段中查看。G1 可能会根据需要重复主要疏散阶段，以处理可选的回收集
- 疏散回收集后阶段(Post Evacuate Collection Set)包括清理工作，如引用处理和为接下来的 mutator 阶段做准备

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::collect() {
    G1YoungGCTraceTime tm(this, _gc_cause);

    // JFR
    // JFR 是 Java Flight Recorder 的缩写，它是 Java 平台的一个性能诊断工具，用于收集应用程序运行时的数据
    G1YoungGCJFRTracerMark jtm(gc_timer_stw(), gc_tracer_stw(), _gc_cause);
    // JStat/MXBeans
    // JStat 是一个监视 Java 虚拟机的命令行工具，它可以用来监视 Java 虚拟机的各种运行时信息
    // MXBeans 是 Java Management Extensions 的一部分，它是一种用于管理和监控 Java 虚拟机的标准 API
    G1YoungGCMonitoringScope ms(monitoring_support(),
                                !collection_set()->candidates()->is_empty() /* all_memory_pools_affected */);
    G1HeapPrinterMark hpm(_g1h);
    // 记录Young GC的暂停时间
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

        // 预备疏散回收集阶段
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
        // 实际执行回收
        // 1. 合并堆根阶段
        // 2. 疏散回收集阶段
        evacuate_initial_collection_set(&per_thread_states, may_do_optional_evacuation);

        if (may_do_optional_evacuation) {
            // 回收老年代分区, Young GC 阶段不会执行到这里
            evacuate_optional_collection_set(&per_thread_states);
        }
        // 疏散回收集后阶段
        post_evacuate_collection_set(jtm.evacuation_info(), &per_thread_states);

        _concurrent_operation_is_full_mark = policy()->concurrent_operation_is_full_mark("Revise IHOP");

        jtm.report_pause_type(collector_state()->young_gc_pause_type(_concurrent_operation_is_full_mark));

        policy()->record_young_collection_end(_concurrent_operation_is_full_mark, evacuation_failed());
    }
    TASKQUEUE_STATS_ONLY(_g1h->task_queues()->print_and_reset_taskqueue_stats("Oop Queue");)
}
```
