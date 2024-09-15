# 执行 GC 并分配对象

在加锁分配对象内存空间时, 会判断是否需要执行 GC, 如果需要执行 GC, 则会调用 do_collection_pause 函数执行 GC 并分配对象内存空间。

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

HeapWord* G1CollectedHeap::do_collection_pause(size_t word_size,
                                               uint gc_count_before,
                                               bool* succeeded,
                                               GCCause::Cause gc_cause) {
  assert_heap_not_locked_and_not_at_safepoint();
  // GC操作: GC并分配对象
  VM_G1CollectForAllocation op(word_size, gc_count_before, gc_cause);
  // 通过VMThread::execute执行GC
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

## VM_G1CollectForAllocation

```cpp
// --- src/hotspot/share/gc/g1/g1VMOperations.hpp --- //

class VM_G1CollectForAllocation : public VM_CollectForAllocation {
  bool _gc_succeeded;

public:
  VM_G1CollectForAllocation(size_t         word_size,
                            uint           gc_count_before,
                            GCCause::Cause gc_cause);
  virtual VMOp_Type type() const { return VMOp_G1CollectForAllocation; }
  virtual void doit();
  bool gc_succeeded() const { return _gc_succeeded; }
};

// --- src/hotspot/share/gc/shared/gcVMOperations.hpp --- //

class VM_CollectForAllocation : public VM_GC_Operation {
 protected:
  // 要分配的对象大小
  size_t    _word_size;
  // 指向对象首地址的指针, 如果分配失败则是null
  HeapWord* _result;

 public:
  VM_CollectForAllocation(size_t word_size, uint gc_count_before, GCCause::Cause cause);

  HeapWord* result() const {
    return _result;
  }
};
```
