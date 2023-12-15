# 计算新的 TLAB 大小

```cpp
///////////////////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/threadLocalAllocBuffer.inline.hpp //
///////////////////////////////////////////////////////////////////////////////////

inline size_t ThreadLocalAllocBuffer::compute_size(size_t obj_size) {
  // 为了避免内存碎片, 新的TLAB会比之前分配的更小
  // Compute the size for the new TLAB.
  // The "last" tlab may be smaller to reduce fragmentation.
  // unsafe_max_tlab_alloc is just a hint.
  const size_t available_size = Universe::heap()->unsafe_max_tlab_alloc(thread()) / HeapWordSize;
  size_t new_tlab_size = MIN3(available_size, desired_size() + align_object_size(obj_size), max_size());

  // Make sure there's enough room for object and filler int[].
  if (new_tlab_size < compute_min_size(obj_size)) {
    // If there isn't enough room for the allocation, return failure.
    log_trace(gc, tlab)("ThreadLocalAllocBuffer::compute_size(" SIZE_FORMAT ") returns failure",
                        obj_size);
    return 0;
  }
  log_trace(gc, tlab)("ThreadLocalAllocBuffer::compute_size(" SIZE_FORMAT ") returns " SIZE_FORMAT,
                      obj_size, new_tlab_size);
  return new_tlab_size;
}

inline size_t ThreadLocalAllocBuffer::compute_min_size(size_t obj_size) {
  const size_t aligned_obj_size = align_object_size(obj_size);
  const size_t size_with_reserve = aligned_obj_size + alignment_reserve();
  return MAX2(size_with_reserve, heap_word_size(MinTLABSize));
}
```
