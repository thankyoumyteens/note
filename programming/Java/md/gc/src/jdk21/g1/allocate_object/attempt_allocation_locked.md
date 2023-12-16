# 拿到锁后分配

```cpp
////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Allocator.inline.hpp //
////////////////////////////////////////////////////////////////////

/**
 * 拿到锁后, 首先尝试分配对象
 */
inline HeapWord* G1Allocator::attempt_allocation_locked(size_t word_size) {
  uint node_index = current_node_index();
  HeapWord* result = mutator_alloc_region(node_index)->attempt_allocation_locked(word_size);

  assert(result != nullptr || mutator_alloc_region(node_index)->get() == nullptr,
         "Must not have a mutator alloc region if there is no memory, but is " PTR_FORMAT, p2i(mutator_alloc_region(node_index)->get()));
  return result;
}

//////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp //
//////////////////////////////////////////////////////////////////////

inline HeapWord* G1AllocRegion::attempt_allocation_locked(size_t word_size) {
  size_t temp;
  return attempt_allocation_locked(word_size, word_size, &temp);
}

inline HeapWord* G1AllocRegion::attempt_allocation_locked(size_t min_word_size,
                                                          size_t desired_word_size,
                                                          size_t* actual_word_size) {
  // 在当前region分配对象
  HeapWord* result = attempt_allocation(min_word_size, desired_word_size, actual_word_size);
  if (result != nullptr) {
    return result;
  }

  // 申请一个新的region, 并在其中分配对象
  return attempt_allocation_using_new_region(min_word_size, desired_word_size, actual_word_size);
}
```
