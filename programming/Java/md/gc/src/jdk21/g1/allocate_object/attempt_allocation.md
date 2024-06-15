# CAS 分配

```cpp
// --- src/hotspot/share/gc/g1/g1Allocator.inline.hpp --- //

// 使用CAS分配对象的内存空间
inline HeapWord* G1Allocator::attempt_allocation(size_t min_word_size,
                                                 size_t desired_word_size,
                                                 size_t* actual_word_size) {
  uint node_index = current_node_index();
  // 先试试看保留region够不够分配这个对象
  // mutator_alloc_region()选择一个region给当前mutator分配内存
  HeapWord* result = mutator_alloc_region(node_index)->attempt_retained_allocation(min_word_size, desired_word_size, actual_word_size);
  if (result != nullptr) {
    return result;
  }

  // 保留region不够分配这个对象, 在当前region中分配
  return mutator_alloc_region(node_index)->attempt_allocation(min_word_size, desired_word_size, actual_word_size);
}

// --- src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp --- //

/**
 * 在保留region中分配
 */
inline HeapWord* MutatorAllocRegion::attempt_retained_allocation(size_t min_word_size,
                                                                 size_t desired_word_size,
                                                                 size_t* actual_word_size) {
  // HeapRegion* volatile _retained_alloc_region;
  // _retained_alloc_region指向保留的region
  // 加锁分配对象时, 如果region的空间不够分配, 可能会申请一个新的region,
  // 这样原来的region在被回收之前就不会再分配对象, 会造成空间的浪费,
  // 所以如果原来的region空间还足够大, 它就会成为保留region,
  // 用来分配小一点的对象
  if (_retained_alloc_region != nullptr) {
    HeapWord* result = par_allocate(_retained_alloc_region, min_word_size, desired_word_size, actual_word_size);
    if (result != nullptr) {
      trace("alloc retained", min_word_size, desired_word_size, *actual_word_size, result);
      return result;
    }
  }
  return nullptr;
}

/**
 * 在当前region中分配
 */
inline HeapWord* G1AllocRegion::attempt_allocation(size_t min_word_size,
                                                   size_t desired_word_size,
                                                   size_t* actual_word_size) {
  HeapRegion* alloc_region = _alloc_region;
  assert_alloc_region(alloc_region != nullptr, "not initialized properly");

  HeapWord* result = par_allocate(alloc_region, min_word_size, desired_word_size, actual_word_size);
  if (result != nullptr) {
    trace("alloc", min_word_size, desired_word_size, *actual_word_size, result);
    return result;
  }
  trace("alloc failed", min_word_size, desired_word_size);
  return nullptr;
}

inline HeapWord* G1AllocRegion::par_allocate(HeapRegion* alloc_region,
                                             size_t min_word_size,
                                             size_t desired_word_size,
                                             size_t* actual_word_size) {
  assert(alloc_region != nullptr, "pre-condition");
  assert(!alloc_region->is_empty(), "pre-condition");

  return alloc_region->par_allocate(min_word_size, desired_word_size, actual_word_size);
}

inline HeapWord* HeapRegion::par_allocate(size_t min_word_size,
                                          size_t desired_word_size,
                                          size_t* actual_word_size) {
  return par_allocate_impl(min_word_size, desired_word_size, actual_word_size);
}

// --- src/hotspot/share/gc/g1/heapRegion.inline.hpp --- //

/**
 * 使用CAS分配对象内存
 */
inline HeapWord* HeapRegion::par_allocate_impl(size_t min_word_size,
                                               size_t desired_word_size,
                                               size_t* actual_size) {
  do {
    // top指针指向这个region的剩余空间的起始位置
    HeapWord* obj = top();
    // 计算这个region还有多大的空闲内存
    size_t available = pointer_delta(end(), obj);
    size_t want_to_allocate = MIN2(available, desired_word_size);
    // 判断这个region够不够分配这个对象
    if (want_to_allocate >= min_word_size) {
      // 堆中也是使用指针碰撞分配内存, 分配对象内存时只需要移动top指针即可
      HeapWord* new_top = obj + want_to_allocate;
      // CAS操作
      // _top: 要修改的地址
      // obj: 当前值
      // new_top: 新值
      HeapWord* result = Atomic::cmpxchg(&_top, obj, new_top);
      // CAS操作如果成功会返回旧值, 如果失败会返回新值
      if (result == obj) {
        // CAS操作成功
        assert(is_object_aligned(obj) && is_object_aligned(new_top), "checking alignment");
        *actual_size = want_to_allocate;
        return obj;
      }
    } else {
      return nullptr;
    }
    // CAS操作失败, 等待下次循环重试
  } while (true);
}
```
