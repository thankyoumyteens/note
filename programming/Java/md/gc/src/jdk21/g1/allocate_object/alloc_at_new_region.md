# 申请新 region 分配

当前线程拿到锁后, 会再尝试分配一次对象, 如果失败了, 则会申请一个新的 region, 并在其中分配对象。

1. 废弃当前 region
2. 申请新 region, 并在新 rgion 中分配

```cpp
// --- src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp --- //

inline HeapWord* G1AllocRegion::attempt_allocation_using_new_region(size_t min_word_size,
                                                                    size_t desired_word_size,
                                                                    size_t* actual_word_size) {
  // 废弃当前region
  retire(true /* fill_up */);
  // 申请新region并分配
  HeapWord* result = new_alloc_region_and_allocate(desired_word_size, false /* force */);
  if (result != nullptr) {
    *actual_word_size = desired_word_size;
    trace("alloc locked (second attempt)", min_word_size, desired_word_size, *actual_word_size, result);
    return result;
  }
  trace("alloc locked failed", min_word_size, desired_word_size);
  return nullptr;
}
```

## 废弃当前 region

dummy region: 不是真正的 region 只是一个标记。它不是 java 堆的一部分, 它的 top 和 end 指针相等, 不可以分配任何对象。JVM 用 `_alloc_region` 指针指向当前正在分配对象的 region。当 `_alloc_region` 指向 dummy region 时, 表示当前没有可用的 region。

1. 

```cpp
// --- src/hotspot/share/gc/g1/g1AllocRegion.cpp --- //

size_t G1AllocRegion::retire(bool fill_up) {
  assert_alloc_region(_alloc_region != nullptr, "not initialized properly");

  size_t waste = 0;

  trace("retiring");
  HeapRegion* alloc_region = _alloc_region;
  if (alloc_region != _dummy_region) {
    waste = retire_internal(alloc_region, fill_up);
    reset_alloc_region();
  }
  trace("retired");

  return waste;
}
```

## 申请新 region

```cpp
// --- src/hotspot/share/gc/g1/g1AllocRegion.cpp --- //

HeapWord* G1AllocRegion::new_alloc_region_and_allocate(size_t word_size,
                                                       bool force) {
  assert_alloc_region(_alloc_region == _dummy_region, "pre-condition");
  assert_alloc_region(_used_bytes_before == 0, "pre-condition");

  trace("attempting region allocation");
  // 申请一个新region
  HeapRegion* new_alloc_region = allocate_new_region(word_size, force);
  if (new_alloc_region != nullptr) {
    // 重置新region的_pre_dummy_top指针
    // _pre_dummy_top的作用:
    // 当本线程需要舍弃一个region时, 其他的线程可能还准备向这个region中分配对象,
    // JVM会在这个要舍弃的region末尾分配一个dummy对象, 用来表示它已经不再使用,
    // _pre_dummy_top指针指向最后一个非dummy对象, 便于查找这个region中的最后一个对象
    new_alloc_region->reset_pre_dummy_top();
    // 记录region已经使用的空间大小
    _used_bytes_before = new_alloc_region->used();
    // 分配对象
    HeapWord* result = allocate(new_alloc_region, word_size);
    assert_alloc_region(result != nullptr, "the allocation should succeeded");

    OrderAccess::storestore();
    // 设置_alloc_region指向这个新的region
    // _alloc_region指向的region是当前正在用于分配对象内存的region
    update_alloc_region(new_alloc_region);
    trace("region allocation successful");
    return result;
  } else {
    trace("region allocation failed");
    return nullptr;
  }
  ShouldNotReachHere();
}
```

## 分配对象

```cpp
// --- src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp --- //

inline HeapWord* G1AllocRegion::allocate(HeapRegion* alloc_region,
                                         size_t word_size) {
  assert(alloc_region != nullptr, "pre-condition");

  return alloc_region->allocate(word_size);
}

// --- src/hotspot/share/gc/g1/heapRegion.inline.hpp --- //

inline HeapWord* HeapRegion::allocate(size_t word_size) {
  size_t temp;
  return allocate(word_size, word_size, &temp);
}

inline HeapWord* HeapRegion::allocate(size_t min_word_size,
                                      size_t desired_word_size,
                                      size_t* actual_word_size) {
  return allocate_impl(min_word_size, desired_word_size, actual_word_size);
}

inline HeapWord* HeapRegion::allocate_impl(size_t min_word_size,
                                           size_t desired_word_size,
                                           size_t* actual_size) {
  HeapWord* obj = top();
  size_t available = pointer_delta(end(), obj);
  size_t want_to_allocate = MIN2(available, desired_word_size);
  if (want_to_allocate >= min_word_size) {
    // 分配对象的内存, 更新region的top指针
    HeapWord* new_top = obj + want_to_allocate;
    set_top(new_top);
    assert(is_object_aligned(obj) && is_object_aligned(new_top), "checking alignment");
    *actual_size = want_to_allocate;
    return obj;
  } else {
    return nullptr;
  }
}
```
