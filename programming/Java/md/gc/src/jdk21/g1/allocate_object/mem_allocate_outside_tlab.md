# 直接在堆中分配对象

当对象太大或者 JVM 判断现有的 TLAB 还可以分配更多小一点的对象时, 当前对象会直接在 TLAB 外面(堆中)分配。

```cpp
// --- src/hotspot/share/gc/shared/memAllocator.cpp --- //

HeapWord *MemAllocator::mem_allocate_outside_tlab(Allocation &allocation) const {
    allocation._allocated_outside_tlab = true;
    // 在堆中分配对象内存
    HeapWord *mem = Universe::heap()->mem_allocate(_word_size, &allocation._overhead_limit_exceeded);
    if (mem == nullptr) {
        // 堆中分配失败
        return mem;
    }

    size_t size_in_bytes = _word_size * HeapWordSize;
    // 更新线程的_allocated_bytes属性
    // _allocated_bytes记录了这个线程一共分配了多少内存
    _thread->incr_allocated_bytes(size_in_bytes);

    return mem;
}
```

在堆中分配的对象也分两种情况

1. 对象特别大, 需要分配到 humongous region 中, humongous region 由 1 个或多个 region 组成
2. 不那么大的对象, 分配到新生代 region 中

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

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
```

## 分配普通对象

JVM 会先使用 CAS 分配对象的内存, 如果 CAS 失败, 才会真正加锁分配。

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

inline HeapWord *G1CollectedHeap::attempt_allocation(size_t min_word_size,
                                                     size_t desired_word_size,
                                                     size_t *actual_word_size) {
    assert_heap_not_locked_and_not_at_safepoint();
    assert(!is_humongous(desired_word_size), "attempt_allocation() should not "
                                             "be called for humongous allocation requests");

    // 尝试使用CAS在堆中分配一块内存
    HeapWord *result = _allocator->attempt_allocation(min_word_size, desired_word_size, actual_word_size);

    // CAS分配失败
    if (result == nullptr) {
        *actual_word_size = desired_word_size;
        // 在堆中加锁分配一块desired_word_size大小的内存(可能会执行垃圾回收)
        result = attempt_allocation_slow(desired_word_size);
    }

    assert_heap_not_locked();
    if (result != nullptr) {
        assert(*actual_word_size != 0, "Actual size must have been set here");
        // 分配成功, 把卡表中对应的卡片标记为dirty
        dirty_young_block(result, *actual_word_size);
    } else {
        // 分配失败, 设置实际分配的大小为0
        *actual_word_size = 0;
    }

    return result;
}
```
