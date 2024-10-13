# Young GC

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

bool G1CollectedHeap::do_collection_pause_at_safepoint() {
  assert_at_safepoint_on_vm_thread();
  guarantee(!is_gc_active(), "collection is not reentrant");

  // 在 JVM 执行垃圾回收前, GCLocker 会先判断当前是否有线程在临界区内,
  // 如果有, GCLocker 会丢弃这次 GC,
  // 等到所有线程都退出临界区后, 会把这次 GC 补上
  if (GCLocker::check_active_before_gc()) {
    return false;
  }

  do_collection_pause_at_safepoint_helper();
  return true;
}

void G1CollectedHeap::do_collection_pause_at_safepoint_helper() {
  ResourceMark rm;

  IsGCActiveMark active_gc_mark;
  GCIdMark gc_id_mark;
  SvcGCMarker sgcm(SvcGCMarker::MINOR);

  GCTraceCPUTime tcpu(_gc_tracer_stw);

  _bytes_used_during_gc = 0;
  // 判断是否要开始并发标记
  policy()->decide_on_concurrent_start_pause();
  // in_concurrent_start_gc() 返回 _in_concurrent_start_gc 的值(bool)
  // _in_concurrent_start_gc 的值会在前面的 decide_on_concurrent_start_pause() 中决定
  // 把它保存到变量中, 因为稍后启动并发标记线程(G1ConcurrentMarkThread)后,
  // _in_concurrent_start_gc 的值可能会在别的地方修改
  bool should_start_concurrent_mark_operation = collector_state()->in_concurrent_start_gc();

  // 执行GC
  G1YoungCollector collector(gc_cause());
  collector.collect();

  // 此时可以开启并发标记线程了,
  // 因为过早开启并发标记线程会导致并发标记的日志和STW期间的日志混到一起
  if (should_start_concurrent_mark_operation) {
    verifier()->verify_bitmap_clear(true /* above_tams_only */);
    // 注意: start_concurrent_cycle() 函数执行后, 并发标记线程可能就会开始并发地运行了
    // 确保在这之后执行的任何操作, 都不会假设只有GC线程在运行
    // 但是实际上并发标记工作直到调用SuspendibleThreadSet::desynchronize()函数退出安全点后才会开始
    start_concurrent_cycle(collector.concurrent_operation_is_full_mark());
    // 把_is_idle设置为false
    // _is_idle为true时表示垃圾回收器处于空闲状态
    ConcurrentGCBreakpoints::notify_idle_to_active();
  }
}
```

## 判断是否启动并发标记

```cpp
// --- src/hotspot/share/gc/g1/g1Policy.cpp --- //

// 是否把本次STW作为并发标记的初始标记阶段
void G1Policy::decide_on_concurrent_start_pause() {

  // in_concurrent_start_gc() 返回 _in_concurrent_start_gc 的值(bool)
  // 首先, in_concurrent_start_gc() 应该返回flse
  // 我们会在这个函数里设置 _in_concurrent_start_gc 为 true
  // _in_concurrent_start_gc 在 STW 结束后会被设置回 false
  assert(!collector_state()->in_concurrent_start_gc(), "pre-condition");

  // 如果并发标记线程正在被终止, 就不启动并发标记
  if (_g1h->concurrent_mark_is_terminating()) {
    return;
  }

  // initiate_conc_mark_if_possible() 返回 _initiate_conc_mark_if_possible 的值(bool)
  // 在 GC 结束的阶段, 会检查堆的空间占用, 来决定下一次 STW 是否需要并发标记
  // 如果需要, 就会把 _initiate_conc_mark_if_possible 设置为 true
  if (collector_state()->initiate_conc_mark_if_possible()) {
    // 在前一次 GC STW 的时候, 如果堆的空间占用超出了发起并发标记的阈值,
    // 或者用户线程明确请求开启发起并发标记,
    // 那么就会开启并发标记阶段

    GCCause::Cause cause = _g1h->gc_cause();
    if ((cause != GCCause::_wb_breakpoint) && ConcurrentGCBreakpoints::is_controlled()) {
      log_debug(gc, ergo)("Do not initiate concurrent cycle (whitebox controlled)");
    } else if (!about_to_start_mixed_phase() && collector_state()->in_young_only_phase()) {
      // bool G1Policy::about_to_start_mixed_phase() const {
      //   return _g1h->concurrent_mark()->cm_thread()->in_progress() || collector_state()->in_young_gc_before_mixed();
      // }
      // 当前没有正在执行的并发标记, 且处于执行 Mixed GC 之前的 Young GC 阶段
      // 则启动新的并发标记过程
      // void G1Policy::initiate_conc_mark() {
      //   collector_state()->set_in_concurrent_start_gc(true);
      //   collector_state()->set_initiate_conc_mark_if_possible(false);
      // }
      initiate_conc_mark();
      log_debug(gc, ergo)("Initiate concurrent cycle (concurrent cycle initiation requested)");
    } else if (_g1h->is_user_requested_concurrent_full_gc(cause) ||
               (cause == GCCause::_codecache_GC_threshold) ||
               (cause == GCCause::_codecache_GC_aggressive) ||
               (cause == GCCause::_wb_breakpoint)) {
      // 启动并发标记
      // 并发标记只能在 young only GC 阶段开始
      // 因为 Mixed GC 也会复用 Young GC 的代码,
      // 所以把只执行 Young GC 的阶段称为 young only GC
      collector_state()->set_in_young_only_phase(true);
      collector_state()->set_in_young_gc_before_mixed(false);

      // 最终执行到这里时, 可能即将开始一个带有CSet的混合阶段
      // 后续的再标记阶段可能会改变这个CSet中分区的 "撤离效率", 并导致后来的断言失败
      // 既然并发标记会重建CSet, 在这里只需直接丢弃即可
      abandon_collection_set_candidates();
      abort_time_to_mixed_tracking();
      // 启动新的并发标记过程
      initiate_conc_mark();
      log_debug(gc, ergo)("Initiate concurrent cycle (%s requested concurrent cycle)",
                          (cause == GCCause::_wb_breakpoint) ? "run_to breakpoint" : "user");
    } else {
      // 上一个周期的并发标记线程还没执行完
      // 如果立即启动新的标记, 会导致重复
      // In particular, the concurrent marking thread might
      // be in the process of clearing the next marking bitmap (which
      // we will use for the next cycle if we start one). Starting a
      // cycle now will be bad given that parts of the marking
      // information might get cleared by the marking thread. And we
      // cannot wait for the marking thread to finish the cycle as it
      // periodically yields while clearing the next marking bitmap
      // and, if it's in a yield point, it's waiting for us to
      // finish. So, at this point we will not start a cycle and we'll
      // let the concurrent marking thread complete the last one.
      log_debug(gc, ergo)("Do not initiate concurrent cycle (concurrent cycle already in progress)");
    }
  }
  // 结果一致性检查
  // We do not allow concurrent start to be piggy-backed on a mixed GC.
  assert(!collector_state()->in_concurrent_start_gc() ||
         collector_state()->in_young_only_phase(), "sanity");
  // We also do not allow mixed GCs during marking.
  assert(!collector_state()->mark_or_rebuild_in_progress() || collector_state()->in_young_only_phase(), "sanity");
}
```
