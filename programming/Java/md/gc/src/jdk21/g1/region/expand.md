# 堆空间扩容

```cpp
/////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////

bool G1CollectedHeap::expand(size_t expand_bytes, WorkerThreads* pretouch_workers, double* expand_time_ms) {
  // 根据操作系统的内存页大小向上对齐
  size_t aligned_expand_bytes = ReservedSpace::page_align_size_up(expand_bytes);
  // 根据一个region的大小向上对齐
  aligned_expand_bytes = align_up(aligned_expand_bytes,
                                       HeapRegion::GrainBytes);

  log_debug(gc, ergo, heap)("Expand the heap. requested expansion amount: " SIZE_FORMAT "B expansion amount: " SIZE_FORMAT "B",
                            expand_bytes, aligned_expand_bytes);

  if (is_maximal_no_gc()) {
    // 没有可用的堆空间
    log_debug(gc, ergo, heap)("Did not expand the heap (heap already fully expanded)");
    return false;
  }

  double expand_heap_start_time_sec = os::elapsedTime();
  // 计算需要增加的region数量
  uint regions_to_expand = (uint)(aligned_expand_bytes / HeapRegion::GrainBytes);
  assert(regions_to_expand > 0, "Must expand by at least one region");
  // 扩容
  uint expanded_by = _hrm.expand_by(regions_to_expand, pretouch_workers);

  if (expand_time_ms != nullptr) {
    *expand_time_ms = (os::elapsedTime() - expand_heap_start_time_sec) * MILLIUNITS;
  }

  assert(expanded_by > 0, "must have failed during commit.");
  // 实际扩容的字节数
  size_t actual_expand_bytes = expanded_by * HeapRegion::GrainBytes;
  assert(actual_expand_bytes <= aligned_expand_bytes, "post-condition");
  policy()->record_new_heap_size(num_regions());

  return true;
}

///////////////////////////////////////////////////
// src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////

uint HeapRegionManager::expand_by(uint num_regions, WorkerThreads* pretouch_workers) {
  assert(num_regions > 0, "Must expand at least 1 region");

  // 首先把Inactive状态的region恢复成Active状态
  uint expanded = expand_inactive(num_regions);

  // 如果不够, 继续从Uncommitted状态的内存中分配region
  if (expanded < num_regions) {
    expanded += expand_any(num_regions - expanded, pretouch_workers);
  }

  verify_optional();
  // 返回扩容的region数
  return expanded;
}

uint HeapRegionManager::expand_inactive(uint num_regions) {
  uint offset = 0;
  uint expanded = 0;

  do {
    HeapRegionRange regions = _committed_map.next_inactive_range(offset);
    if (regions.length() == 0) {
      // No more unavailable regions.
      break;
    }

    uint to_expand = MIN2(num_regions - expanded, regions.length());
    reactivate_regions(regions.start(), to_expand);
    expanded += to_expand;
    offset = regions.end();
  } while (expanded < num_regions);

  return expanded;
}

uint HeapRegionManager::expand_any(uint num_regions, WorkerThreads* pretouch_workers) {
  assert(num_regions > 0, "Must expand at least 1 region");

  uint offset = 0;
  uint expanded = 0;

  do {
    HeapRegionRange regions = _committed_map.next_committable_range(offset);
    if (regions.length() == 0) {
      // No more unavailable regions.
      break;
    }

    uint to_expand = MIN2(num_regions - expanded, regions.length());
    expand(regions.start(), to_expand, pretouch_workers);
    expanded += to_expand;
    offset = regions.end();
  } while (expanded < num_regions);

  return expanded;
}
```
