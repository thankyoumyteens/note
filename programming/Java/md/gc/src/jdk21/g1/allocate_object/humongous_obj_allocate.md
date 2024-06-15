# 分配大对象

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

/**
 * 分配大对象
 */
HeapWord* G1CollectedHeap::humongous_obj_allocate(size_t word_size) {
  assert_heap_locked_or_at_safepoint(true /* should_be_vm_thread */);

  _verifier->verify_region_sets_optional();
  // 这个大对象需要用几个region存储
  uint obj_regions = (uint) humongous_obj_size_in_regions(word_size);

  // 尝试从空闲region列表寻找可以存放这个大对象的obj_regions个region,
  // 并返回第1个region的指针
  HeapRegion* humongous_start = _hrm.allocate_humongous(obj_regions);
  if (humongous_start == nullptr) {
    // 空闲列表中没找到合适的region,
    // 尝试扩大堆空间后重新分配
    humongous_start = _hrm.expand_and_allocate_humongous(obj_regions);
    if (humongous_start != nullptr) {
      log_debug(gc, ergo, heap)("Heap expansion (humongous allocation request). Allocation request: " SIZE_FORMAT "B",
                                word_size * HeapWordSize);
      policy()->record_new_heap_size(num_regions());
    } else {
      // Policy: Potentially trigger a defragmentation GC.
    }
  }

  HeapWord* result = nullptr;
  if (humongous_start != nullptr) {
    // 大对象分配完成, 初始化内存
    result = humongous_obj_allocate_initialize_regions(humongous_start, obj_regions, word_size);
    assert(result != nullptr, "it should always return a valid result");
    // A successful humongous object allocation changes the used space
    // information of the old generation so we need to recalculate the
    // sizes and update the jstat counters here.
    monitoring_support()->update_sizes();
  }

  _verifier->verify_region_sets_optional();

  return result;
}
```
