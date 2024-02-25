# 直接在 region 中分配

```cpp
//////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/shared/memAllocator.cpp //
//////////////////////////////////////////////////////////////////

/**
 * 直接在region中分配对象内存
 */
HeapWord* MemAllocator::mem_allocate_outside_tlab(Allocation& allocation) const {
  allocation._allocated_outside_tlab = true;
  HeapWord* mem = Universe::heap()->mem_allocate(_word_size, &allocation._overhead_limit_exceeded);
  if (mem == nullptr) {
    return mem;
  }

  size_t size_in_bytes = _word_size * HeapWordSize;
  _thread->incr_allocated_bytes(size_in_bytes);

  return mem;
}

/////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

HeapWord*
G1CollectedHeap::mem_allocate(size_t word_size,
                              bool*  gc_overhead_limit_was_exceeded) {
  assert_heap_not_locked_and_not_at_safepoint();

  if (is_humongous(word_size)) {
    // 分配大对象
    return attempt_allocation_humongous(word_size);
  }
  size_t dummy = 0;
  // 分配普通对象
  return attempt_allocation(word_size, word_size, &dummy);
}

inline HeapWord* G1CollectedHeap::attempt_allocation(size_t min_word_size,
                                                     size_t desired_word_size,
                                                     size_t* actual_word_size) {
  assert_heap_not_locked_and_not_at_safepoint();
  assert(!is_humongous(desired_word_size), "attempt_allocation() should not "
         "be called for humongous allocation requests");
  // 使用CAS分配对象的内存空间
  HeapWord* result = _allocator->attempt_allocation(min_word_size, desired_word_size, actual_word_size);

  if (result == nullptr) {
    *actual_word_size = desired_word_size;
    // CAS分配失败, 加锁分配
    result = attempt_allocation_slow(desired_word_size);
  }

  assert_heap_not_locked();
  if (result != nullptr) {
    // 对象分配成功
    assert(*actual_word_size != 0, "Actual size must have been set here");
    // 在全局卡表中标记这个对象属于新生代region
    dirty_young_block(result, *actual_word_size);
  } else {
    *actual_word_size = 0;
  }

  return result;
}
```
