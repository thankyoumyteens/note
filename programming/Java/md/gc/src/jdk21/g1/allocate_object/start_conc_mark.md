# 开启并发标记

```cpp
//////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////////////////////

/**
 * 是否需要开启并发标记
 */
bool G1Policy::need_to_start_conc_mark(const char* source, size_t alloc_word_size) {
  // 如果并发标记线程正在执行或者处于开始 Mixed GC 之前的最后一次 Young GC,
  // 则无需启动并发标记
  if (about_to_start_mixed_phase()) {
    return false;
  }
  // 启动并发标记的阈值
  // 当前非新生代的region已使用的内存空间需要大于这个值, 才能开启并发标记
  size_t marking_initiating_used_threshold = _ihop_control->get_conc_mark_start_threshold();
  // 非新生代的region已使用的内存空间
  // 即 old region 和 humongous region 用了多少
  size_t cur_used_bytes = _g1h->non_young_capacity_bytes();
  size_t alloc_byte_size = alloc_word_size * HeapWordSize;
  size_t marking_request_bytes = cur_used_bytes + alloc_byte_size;

  bool result = false;
  if (marking_request_bytes > marking_initiating_used_threshold) {
    result = collector_state()->in_young_only_phase() && !collector_state()->in_young_gc_before_mixed();
    log_debug(gc, ergo, ihop)("%s occupancy: " SIZE_FORMAT "B allocation request: " SIZE_FORMAT "B threshold: " SIZE_FORMAT "B (%1.2f) source: %s",
                              result ? "Request concurrent cycle initiation (occupancy higher than threshold)" : "Do not request concurrent cycle initiation (still doing mixed collections)",
                              cur_used_bytes, alloc_byte_size, marking_initiating_used_threshold, (double) marking_initiating_used_threshold / _g1h->capacity() * 100, source);
  }
  return result;
}

bool G1Policy::about_to_start_mixed_phase() const {
  // G1ConcurrentMark* _cm; 用于执行并发标记的类
  // G1ConcurrentMarkThread* _cm_thread; 执行并发标记的线程
  // in_progress() 返回并发标记线程是否正在执行
  // 
  // G1CollectorState _collector_state; 用于判断当前处于Young GC 还是 Mixed GC
  // in_young_gc_before_mixed() 是否处于开始 Mixed GC 之前的最后一次 Young GC
  return _g1h->concurrent_mark()->cm_thread()->in_progress() || collector_state()->in_young_gc_before_mixed();
}

/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

/**
 * 执行GC
 */
void G1CollectedHeap::collect(GCCause::Cause cause) {
  try_collect(cause, collection_counters(this));
}

bool G1CollectedHeap::try_collect(GCCause::Cause cause,
                                  const G1GCCounters& counters_before) {
  // 判断是否需要执行Full GC
  if (should_do_concurrent_full_gc(cause)) {
    return try_collect_concurrently(cause,
                                    counters_before.total_collections(),
                                    counters_before.old_marking_cycles_started());
  } else if (GCLocker::should_discard(cause, counters_before.total_collections())) {
    // 被其他线程抢先执行GC, 舍弃本次GC
    return false;
  } else if (cause == GCCause::_gc_locker || cause == GCCause::_wb_young_gc
             DEBUG_ONLY(|| cause == GCCause::_scavenge_alot)) {

    // word_size为0, 表示执行GC后不需要分配对象内存
    VM_G1CollectForAllocation op(0,     /* word_size */
                                 counters_before.total_collections(),
                                 cause);
    // 交给VMThread执行GC
    VMThread::execute(&op);
    return op.gc_succeeded();
  } else {
    // 执行Full GC
    return try_collect_fullgc(cause, counters_before);
  }
}
```
