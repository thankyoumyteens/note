# 是否作为并发标记的初始标记阶段

```cpp
// --- src/hotspot/share/gc/g1/g1Policy.cpp --- //

void G1Policy::decide_on_concurrent_start_pause() {
    // in_concurrent_start_gc() 返回 _in_concurrent_start_gc 的值(bool值)
    // 首先, in_concurrent_start_gc() 应该返回flse
    // 我们会在这个函数里设置 _in_concurrent_start_gc 为 true
    // _in_concurrent_start_gc 在 STW 结束后会被设置回 false
    assert(!collector_state()->in_concurrent_start_gc(), "pre-condition");

    // 如果并发标记线程正在被终止, 就不启动并发标记
    if (_g1h->concurrent_mark_is_terminating()) {
        return;
    }

    // initiate_conc_mark_if_possible() 返回 _initiate_conc_mark_if_possible 的值(bool值)
    // 在 GC 结束的阶段, 会检查堆的空间占用, 来决定下一次 STW 是否需要并发标记
    // 如果需要, 就会把 _initiate_conc_mark_if_possible 设置为 true
    if (collector_state()->initiate_conc_mark_if_possible()) {
        // 在前一次 GC STW 的时候, 如果堆的空间占用超出了发起并发标记的阈值,
        // 或者用户线程明确请求开启发起并发标记,
        // 那么就会开启并发标记阶段

        GCCause::Cause cause = _g1h->gc_cause();
        if ((cause != GCCause::_wb_breakpoint) &&
            ConcurrentGCBreakpoints::is_controlled()) {
            log_debug(gc, ergo)("Do not initiate concurrent cycle (whitebox controlled)");
        } else if (!about_to_start_mixed_phase() && collector_state()->in_young_only_phase()) {
            // 当前没有正在执行的并发标记, 且处于执行 Mixed GC 之前的 Young GC 阶段
            // 则启动新的并发标记过程
            initiate_conc_mark();
            log_debug(gc, ergo)("Initiate concurrent cycle (concurrent cycle initiation requested)");
        } else if (_g1h->is_user_requested_concurrent_full_gc(cause) ||
                   (cause == GCCause::_codecache_GC_threshold) ||
                   (cause == GCCause::_codecache_GC_aggressive) ||
                   (cause == GCCause::_wb_breakpoint)) {
            // 启动并发标记
            // 并发标记只能在 young only GC 阶段开始
            // 因为 Mixed GC 也会复用 Young GC 的代码,
            // 所以把只执行 Young GC 的阶段称为 young only GC 阶段
            collector_state()->set_in_young_only_phase(true);
            collector_state()->set_in_young_gc_before_mixed(false);

            // 最终执行到这里时, 可能即将开始一个带有回收集的混合阶段
            // 后续的再标记阶段可能会改变这个回收集中分区的 "撤离效率", 并导致后来的断言失败
            // 既然并发标记会重建回收集, 在这里只需直接丢弃即可
            abandon_collection_set_candidates();
            abort_time_to_mixed_tracking();
            // 启动新的并发标记过程
            initiate_conc_mark();
            log_debug(gc, ergo)("Initiate concurrent cycle (%s requested concurrent cycle)",
                                (cause == GCCause::_wb_breakpoint) ? "run_to breakpoint" : "user");
        } else {
            // 上一个周期的并发标记线程还没执行完
            // 如果立即启动新的标记, 会导致重复
            log_debug(gc, ergo)("Do not initiate concurrent cycle (concurrent cycle already in progress)");
        }
    }
    // 结果一致性检查
    assert(!collector_state()->in_concurrent_start_gc() ||
           collector_state()->in_young_only_phase(), "sanity");
    assert(!collector_state()->mark_or_rebuild_in_progress() || collector_state()->in_young_only_phase(), "sanity");
}
```
