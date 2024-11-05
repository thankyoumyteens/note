# 执行垃圾回收并分配对象

通过 VMThread::execute 执行 GC。

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

HeapWord *G1CollectedHeap::do_collection_pause(size_t word_size,
                                               uint gc_count_before,
                                               bool *succeeded,
                                               GCCause::Cause gc_cause) {
    assert_heap_not_locked_and_not_at_safepoint();
    // 执行垃圾回收并分配内存
    VM_G1CollectForAllocation op(word_size, gc_count_before, gc_cause);
    // 通过VMThread::execute执行任务op
    VMThread::execute(&op);

    // 分配的内存的起始地址
    HeapWord *result = op.result();
    bool ret_succeeded = op.prologue_succeeded() && op.gc_succeeded();
    assert(result == nullptr || ret_succeeded,
           "the result should be null if the VM did not succeed");
    *succeeded = ret_succeeded;

    assert_heap_not_locked();
    return result;
}
```
