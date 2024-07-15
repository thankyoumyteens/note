# VMThread

在 JVM 创建时，将会在全局范围内创建一个单例原生线程 VMThread(虚拟机线程)。该线程的一个重要职责是：维护一个虚拟机操作队列(VMOperationQueue)，接受其他线程请求虚拟机级别的操作 (VM_Operation)，如执行 GC 等任务。

VMThread 会开启一个无限循环, 然后不断地从虚拟机操作队列中取出 VM_Operation 并且执行这个 VM_Operation。

VM_Operation 是通过其他线程放入到队列中的, 最常见的就是执行 GC。比如 GCLocker 执行 GC 的时候, 会调用对应的 CollectedHeap 中的 collect 函数:

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

void G1CollectedHeap::collect(GCCause::Cause cause) {
  try_collect(cause, collection_counters(this));
}

bool G1CollectedHeap::try_collect(GCCause::Cause cause,
                                  const G1GCCounters& counters_before) {
  // 根据不同的GCCause, 执行不同的逻辑
  if (should_do_concurrent_full_gc(cause)) {
    // 执行并行的 Full GC
    return try_collect_concurrently(cause,
                                    counters_before.total_collections(),
                                    counters_before.old_marking_cycles_started());
  } else if (GCLocker::should_discard(cause, counters_before.total_collections())) {
    // 在GCLocker发起的GC执行之前, 有其它线程已经执行了GC
    return false;
  } else if (cause == GCCause::_gc_locker || cause == GCCause::_wb_young_gc
             DEBUG_ONLY(|| cause == GCCause::_scavenge_alot)) {
    // 执行GC
    // word_size为0, 表示GC完成后不会申请新的region
    // VM_Operation是VM_G1CollectForAllocation的祖先类
    VM_G1CollectForAllocation op(0,     /* word_size */
                                 counters_before.total_collections(),
                                 cause);
    // 通过VMThread::execute把VM_G1CollectForAllocation放入VM_Operation队列中
    VMThread::execute(&op);
    return op.gc_succeeded();
  } else {
    // 执行 Full GC
    return try_collect_fullgc(cause, counters_before);
  }
}
```
