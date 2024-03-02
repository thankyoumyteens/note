# 堆空间扩容

```cpp
bool G1CollectedHeap::expand(size_t expand_bytes, WorkerThreads* pretouch_workers, double* expand_time_ms) {
  // 根据操作系统的内存页大小向上对齐
  size_t aligned_expand_bytes = ReservedSpace::page_align_size_up(expand_bytes);
  // 根据一个region的大小向上对齐
  aligned_expand_bytes = align_up(aligned_expand_bytes,
                                       HeapRegion::GrainBytes);

  log_debug(gc, ergo, heap)("Expand the heap. requested expansion amount: " SIZE_FORMAT "B expansion amount: " SIZE_FORMAT "B",
                            expand_bytes, aligned_expand_bytes);

  if (is_maximal_no_gc()) {
    log_debug(gc, ergo, heap)("Did not expand the heap (heap already fully expanded)");
    return false;
  }

  double expand_heap_start_time_sec = os::elapsedTime();
  uint regions_to_expand = (uint)(aligned_expand_bytes / HeapRegion::GrainBytes);
  assert(regions_to_expand > 0, "Must expand by at least one region");

  uint expanded_by = _hrm.expand_by(regions_to_expand, pretouch_workers);
  if (expand_time_ms != nullptr) {
    *expand_time_ms = (os::elapsedTime() - expand_heap_start_time_sec) * MILLIUNITS;
  }

  assert(expanded_by > 0, "must have failed during commit.");

  size_t actual_expand_bytes = expanded_by * HeapRegion::GrainBytes;
  assert(actual_expand_bytes <= aligned_expand_bytes, "post-condition");
  policy()->record_new_heap_size(num_regions());

  return true;
}
```
