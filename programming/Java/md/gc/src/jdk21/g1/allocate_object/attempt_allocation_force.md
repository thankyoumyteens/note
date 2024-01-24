# 扩容新生代

```cpp
////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Allocator.inline.hpp //
////////////////////////////////////////////////////////////////////

inline HeapWord* G1Allocator::attempt_allocation_force(size_t word_size) {
  uint node_index = current_node_index();
  // mutator_alloc_region()返回MutatorAllocRegion
  // MutatorAllocRegion是G1AllocRegion的子类,
  return mutator_alloc_region(node_index)->attempt_allocation_force(word_size);
}

//////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp //
//////////////////////////////////////////////////////////////////////

inline HeapWord* G1AllocRegion::attempt_allocation_force(size_t word_size) {
  assert_alloc_region(_alloc_region != nullptr, "not initialized properly");

  trace("forcing alloc", word_size, word_size);
  // 申请新region并分配对象
  // 与attempt_allocation_using_new_region()类似
  // 区别是第二个参数force为true, 表示即使达到最大region个数, 也要尝试分配新的region
  HeapWord* result = new_alloc_region_and_allocate(word_size, true /* force */);
  if (result != nullptr) {
    trace("alloc forced", word_size, word_size, word_size, result);
    return result;
  }
  trace("alloc forced failed", word_size, word_size);
  return nullptr;
}

///////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1AllocRegion.cpp //
///////////////////////////////////////////////////////////////

HeapWord* G1AllocRegion::new_alloc_region_and_allocate(size_t word_size,
                                                       bool force) {
  assert_alloc_region(_alloc_region == _dummy_region, "pre-condition");
  assert_alloc_region(_used_bytes_before == 0, "pre-condition");

  trace("attempting region allocation");
  // 申请一个新region
  // G1AllocRegion中的allocate_new_region()不允许force为true
  // 这里调用的是MutatorAllocRegion中的allocate_new_region()
  HeapRegion* new_alloc_region = allocate_new_region(word_size, force);
  if (new_alloc_region != nullptr) {
    // 重置新region的_pre_dummy_top指针
    new_alloc_region->reset_pre_dummy_top();
    // 记录region已经使用的空间大小
    _used_bytes_before = new_alloc_region->used();
    // 分配对象
    HeapWord* result = allocate(new_alloc_region, word_size);
    assert_alloc_region(result != nullptr, "the allocation should succeeded");

    OrderAccess::storestore();
    // 设置_alloc_region指向这个新的region
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
