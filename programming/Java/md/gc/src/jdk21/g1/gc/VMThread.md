# VMThread

VMThread 就是的 JVM 线程, 只有一个实例, JVM 运行过程中只会被创建一次, 并且随着 JVM 销毁的时候被销毁。

VMThread 会开启一个无限循环, 然后不断地从一个 VM_Operation 队列中取出 VM_Operation 并且执行, 如果没有 VM_Operation 就等待一会。

VM_Operation 是通过其他线程放入到队列中的, 比如要执行 GC 的时候:

```cpp
/////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

/**
 * 执行 GC 并分配对象
 */
HeapWord* G1CollectedHeap::do_collection_pause(size_t word_size,
                                               uint gc_count_before,
                                               bool* succeeded,
                                               GCCause::Cause gc_cause) {
  assert_heap_not_locked_and_not_at_safepoint();
  // GC操作: GC并分配对象
  VM_G1CollectForAllocation op(word_size, gc_count_before, gc_cause);
  // 通过VMThread::execute把VM_G1CollectForAllocation放入VM_Operation队列中
  VMThread::execute(&op);

  HeapWord* result = op.result();
  bool ret_succeeded = op.prologue_succeeded() && op.gc_succeeded();
  assert(result == nullptr || ret_succeeded,
         "the result should be null if the VM did not succeed");
  *succeeded = ret_succeeded;

  assert_heap_not_locked();
  return result;
}
```
