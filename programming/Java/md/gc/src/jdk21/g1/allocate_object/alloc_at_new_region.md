# 申请新分区分配

当前线程拿到锁后, 会再尝试分配一次, 如果失败了, 则会申请一个新的分区, 并在其中分配内存。

1. 废弃当前分区
2. 申请新分区, 并在新分区中分配

```cpp
// --- src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp --- //

inline HeapWord *G1AllocRegion::attempt_allocation_using_new_region(size_t min_word_size,
                                                                    size_t desired_word_size,
                                                                    size_t *actual_word_size) {
    // 废弃当前分区
    retire(true /* fill_up */);
    // 申请新分区并分配
    HeapWord *result = new_alloc_region_and_allocate(desired_word_size, false /* force */);
    if (result != nullptr) {
        *actual_word_size = desired_word_size;
        trace("alloc locked (second attempt)", min_word_size, desired_word_size, *actual_word_size, result);
        return result;
    }
    trace("alloc locked failed", min_word_size, desired_word_size);
    return nullptr;
}
```

## 废弃当前分区

dummy region: 不是真正的分区, 只是一个标记。它不是 java 堆的一部分, 它的 top 和 end 指针相等, 不可以分配任何内存。JVM 用 `_alloc_region` 指针指向当前正在分配内存的分区。当 `_alloc_region` 指向 dummy region 时, 表示当前没有可用的分区。

1. 将当前分区的剩余空间全部填充为 dummy 对象, 避免其它线程继续在其中分配任何内存
2. 设置 `_pre_dummy_top` 指针, 指向有效内存的最后一位地址, 用来区分出正常的对象和 dummy 对象
3. 废弃当前分区

```cpp
// --- src/hotspot/share/gc/g1/g1AllocRegion.cpp --- //

size_t G1AllocRegion::retire(bool fill_up) {
    assert_alloc_region(_alloc_region != nullptr, "not initialized properly");

    size_t waste = 0;

    trace("retiring");
    HeapRegion *alloc_region = _alloc_region;
    if (alloc_region != _dummy_region) {
        waste = retire_internal(alloc_region, fill_up);
        reset_alloc_region();
    }
    trace("retired");

    return waste;
}

// --- src/hotspot/share/gc/g1/g1AllocRegion.cpp --- //

size_t G1AllocRegion::retire_internal(HeapRegion *alloc_region, bool fill_up) {
    size_t waste = 0;
    assert_alloc_region(!alloc_region->is_empty(),
                        "the alloc region should never be empty");

    if (fill_up) {
        // 把剩余的空间填满dummy对象
        waste = fill_up_remaining_space(alloc_region);
    }

    assert_alloc_region(alloc_region->used() >= _used_bytes_before, "invariant");
    size_t allocated_bytes = alloc_region->used() - _used_bytes_before;
    // 废弃分区
    retire_region(alloc_region, allocated_bytes);
    _used_bytes_before = 0;

    return waste;
}

size_t G1AllocRegion::fill_up_remaining_space(HeapRegion *alloc_region) {
    assert(alloc_region != nullptr && alloc_region != _dummy_region,
           "pre-condition");
    size_t result = 0;

    // 分区的剩余空间
    size_t free_word_size = alloc_region->free() / HeapWordSize;

    // 如果剩余空间不足min_word_size_to_fill的话
    // 就不够任何对象分配了, 所以也就不用填充dummy对象了
    size_t min_word_size_to_fill = CollectedHeap::min_fill_size();

    while (free_word_size >= min_word_size_to_fill) {
        // 把剩余空间都分配成dummy对象
        HeapWord *dummy = par_allocate(alloc_region, free_word_size);
        if (dummy != nullptr) {
            // 填充dummy对象
            alloc_region->fill_with_dummy_object(dummy, free_word_size);
            // 设置_pre_dummy_top指针, 用来区分出正常的对象和dummy对象
            alloc_region->set_pre_dummy_top(dummy);
            result += free_word_size * HeapWordSize;
            break;
        }

        // 被其它线程干扰(其它线程在这个分区分配内存),
        // 重新查询剩余空间, 以决定是否继续分配dummy对象
        free_word_size = alloc_region->free() / HeapWordSize;
    }
    result += alloc_region->free();

    assert(alloc_region->free() / HeapWordSize < min_word_size_to_fill,
           "post-condition");
    return result;
}
```

## 申请新分区

1. 申请一个新分区
2. 把 `_pre_dummy_top` 指针指向 null
3. 在新的分区中分配内存
4. 设置 `_alloc_region` 指向这个新的分区, 以后都会在这个分区中分配

```cpp
// --- src/hotspot/share/gc/g1/g1AllocRegion.cpp --- //

HeapWord *G1AllocRegion::new_alloc_region_and_allocate(size_t word_size,
                                                       bool force) {
    assert_alloc_region(_alloc_region == _dummy_region, "pre-condition");
    assert_alloc_region(_used_bytes_before == 0, "pre-condition");

    trace("attempting region allocation");
    // 申请一个新分区
    // 这里调用的是G1AllocRegion中的allocate_new_region()
    HeapRegion *new_alloc_region = allocate_new_region(word_size, force);
    if (new_alloc_region != nullptr) {
        // 新分区没有dummy对象, 把_pre_dummy_top指针指向null
        new_alloc_region->reset_pre_dummy_top();
        // 记录分区的大小
        _used_bytes_before = new_alloc_region->used();
        // 在新分区中分配内存
        HeapWord *result = allocate(new_alloc_region, word_size);
        assert_alloc_region(result != nullptr, "the allocation should succeeded");

        OrderAccess::storestore();
        // 设置_alloc_region指向这个新的分区
        // _alloc_region指向的分区是当前正在用于分配内存的分区
        update_alloc_region(new_alloc_region);
        trace("region allocation successful");
        return result;
    } else {
        trace("region allocation failed");
        return nullptr;
    }
    ShouldNotReachHere();
}

HeapRegion *G1GCAllocRegion::allocate_new_region(size_t word_size,
                                                 bool force) {
    assert(!force, "not supported for GC alloc regions");
    return _g1h->new_gc_alloc_region(word_size, _purpose, _node_index);
}
```

## 在新分区中分配内存

由于此时线程已经持有锁, 直接修改 top 指针即可。

```cpp
// --- src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp --- //

inline HeapWord *G1AllocRegion::allocate(HeapRegion *alloc_region,
                                         size_t word_size) {
    assert(alloc_region != nullptr, "pre-condition");

    return alloc_region->allocate(word_size);
}

// --- src/hotspot/share/gc/g1/heapRegion.inline.hpp --- //

inline HeapWord *HeapRegion::allocate(size_t word_size) {
    size_t temp;
    return allocate(word_size, word_size, &temp);
}

inline HeapWord *HeapRegion::allocate(size_t min_word_size,
                                      size_t desired_word_size,
                                      size_t *actual_word_size) {
    return allocate_impl(min_word_size, desired_word_size, actual_word_size);
}

inline HeapWord *HeapRegion::allocate_impl(size_t min_word_size,
                                           size_t desired_word_size,
                                           size_t *actual_size) {
    HeapWord *obj = top();
    size_t available = pointer_delta(end(), obj);
    size_t want_to_allocate = MIN2(available, desired_word_size);
    if (want_to_allocate >= min_word_size) {
        // 此时线程已经持有锁, 直接修改分区的top指针
        HeapWord *new_top = obj + want_to_allocate;
        set_top(new_top);
        assert(is_object_aligned(obj) && is_object_aligned(new_top), "checking alignment");
        *actual_size = want_to_allocate;
        return obj;
    } else {
        return nullptr;
    }
}
```
