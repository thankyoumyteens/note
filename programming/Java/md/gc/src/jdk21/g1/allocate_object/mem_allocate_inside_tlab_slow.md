# 申请新的 TLAB

每个 TLAB 都会维护一个 refill_waste_limit, 用于判断当前 TLAB 不够分配对象时, 是否需要申请新的 TLAB。

假设要分配的对象 a 的大小为 10k, refill_waste_limit 是 5k:

1. 如果当前 TLAB 剩余空间为 3k, 那么这个 TLAB 就会被舍弃, 当前线程会申请一个新的 TLAB 来为对象 a 分配空间
2. 如果当前 TLAB 剩余空间为 6k(或者其它大于 5k 的值), 那么这个 TLAB 就会被保留, 等待分配其它较小的对象, 本次这个对象 a 会直接在堆中加锁分配内存空间

```cpp
// --- src/hotspot/share/gc/shared/memAllocator.cpp --- //

// 申请一个新的TLAB, 并在新的TLAB中分配对象内存
HeapWord *MemAllocator::mem_allocate_inside_tlab_slow(Allocation &allocation) const {
    HeapWord *mem = nullptr;
    // 拿到当前线程的TLAB
    ThreadLocalAllocBuffer &tlab = _thread->tlab();

    // TLAB剩余的空间是否大于refill_waste_limit
    if (tlab.free() > tlab.refill_waste_limit()) {
        // 保留这个TLAB

        // 增大refill_waste_limit, 以避免频繁在堆中直接分配对象
        tlab.record_slow_allocation(_word_size);
        // 返回null, 后续会直接在堆中分配这个对象
        return nullptr;
    }

    // 创建一个新的TLAB来为对象分配空间, 并丢弃旧的TLAB
    // 计算新的TLAB的大小
    // 为了避免内存碎片, 新的TLAB会比之前分配的更小
    size_t new_tlab_size = tlab.compute_size(_word_size);

    // 丢弃当前TLAB中剩余的空间
    // 把当前TLAB中剩余的空间填充为dummy对象, 以便在GC时能够识别这些空间
    tlab.retire_before_allocation();

    // 堆内存不足, 新的TLAB创建失败
    if (new_tlab_size == 0) {
        return nullptr;
    }

    // 计算新TLAB所需的最小空间
    // _word_size是要分配的对象的大小, 新的TLAB的最小也要能容纳这个对象
    size_t min_tlab_size = ThreadLocalAllocBuffer::compute_min_size(_word_size);
    // 为新的TLAB分配内存
    // 新的TLAB大小在 [min_tlab_size, new_tlab_size] 范围内则创建成功, 否则创建失败
    // 由于是新的TLAB, 对象从头开始分配,
    // 所以mem既是TLAB的起始地址, 又是新分配的对象的起始地址
    mem = Universe::heap()->allocate_new_tlab(min_tlab_size, new_tlab_size, &allocation._allocated_tlab_size);
    if (mem == nullptr) {
        // 新的TLAB创建失败
        assert(allocation._allocated_tlab_size == 0,
               "Allocation failed, but actual size was updated. min: " SIZE_FORMAT
                       ", desired: " SIZE_FORMAT ", actual: " SIZE_FORMAT,
               min_tlab_size, new_tlab_size, allocation._allocated_tlab_size);
        return nullptr;
    }
    assert(allocation._allocated_tlab_size != 0, "Allocation succeeded but actual size not updated. mem at: "
            PTR_FORMAT " min: " SIZE_FORMAT ", desired: " SIZE_FORMAT,
           p2i(mem), min_tlab_size, new_tlab_size);

    if (ZeroTLAB) {
        // 如果开启了ZeroTLAB, 就把整个TLAB内存空间初始化为0
        Copy::zero_to_words(mem, allocation._allocated_tlab_size);
    } else {
#ifdef ASSERT
        // 否则填充新对象的内存区域
        // 为了让并发的GC线程扫描时可以直接跳过这个新分配的对象
        size_t hdr_size = oopDesc::header_size();
        // 把除了对象头以外的整个TLAB用 0xBAADBABE 填充
        Copy::fill_to_words(mem + hdr_size, allocation._allocated_tlab_size - hdr_size, badHeapWordVal);
#endif // ASSERT
    }

    // 初始化新TLAB的相关字段
    tlab.fill(mem, mem + _word_size, allocation._allocated_tlab_size);
    // 返回对象的起始地址
    return mem;
}
```

## 为新的 TLAB 分配内存

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

HeapWord *G1CollectedHeap::allocate_new_tlab(size_t min_size,
                                             size_t requested_size,
                                             size_t *actual_size) {
    assert_heap_not_locked_and_not_at_safepoint();
    assert(!is_humongous(requested_size), "we do not allow humongous TLABs");

    // 为新的TLAB分配内存
    return attempt_allocation(min_size, requested_size, actual_size);
}

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

## 初始化新 TLAB 的相关字段

```cpp
// --- src/hotspot/share/gc/shared/threadLocalAllocBuffer.cpp --- //

void ThreadLocalAllocBuffer::fill(HeapWord *start,
                                  HeapWord *top,
                                  size_t new_size) {
    _number_of_refills++;
    _allocated_size += new_size;
    print_stats("fill");
    assert(top <= start + new_size - alignment_reserve(), "size too small");

    // 初始化TLAB
    initialize(start, top, start + new_size - alignment_reserve());

    // 为新的TLAB重置refill_waste_limit值
    set_refill_waste_limit(initial_refill_waste_limit());
}
```
