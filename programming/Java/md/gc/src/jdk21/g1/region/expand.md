# 堆空间扩容

```cpp
/////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////

bool G1CollectedHeap::expand(size_t expand_bytes, WorkerThreads* pretouch_workers, double* expand_time_ms) {
  // 根据操作系统的内存页大小向上对齐
  size_t aligned_expand_bytes = ReservedSpace::page_align_size_up(expand_bytes);
  // 根据region的大小向上对齐
  aligned_expand_bytes = align_up(aligned_expand_bytes,
                                       HeapRegion::GrainBytes);

  log_debug(gc, ergo, heap)("Expand the heap. requested expansion amount: " SIZE_FORMAT "B expansion amount: " SIZE_FORMAT "B",
                            expand_bytes, aligned_expand_bytes);

  // 获取状态为uncommitted的region数量
  // return _regions.length() - _committed_map.num_active()
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
  // 记录扩容的耗时
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

/**
 * 按region数扩容
 */
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
```

## 把 Inactive 状态的 region 恢复成 Active 状态

```cpp
///////////////////////////////////////////////////
// src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////

uint HeapRegionManager::expand_inactive(uint num_regions) {
  uint offset = 0;
  uint expanded = 0;

  do {
    // 找出Inactive状态的region
    HeapRegionRange regions = _committed_map.next_inactive_range(offset);
    if (regions.length() == 0) {
      // 没找到Inactive状态的region
      break;
    }
    // 两种情况:
    //   1. regions数量很多, 只需要使用num_regions个
    //   2. regions数量比较少, 只能使用regions.length()个
    uint to_expand = MIN2(num_regions - expanded, regions.length());
    // 把region恢复成Active状态
    reactivate_regions(regions.start(), to_expand);
    expanded += to_expand;
    offset = regions.end();
  } while (expanded < num_regions);
  // 返回扩容了几个region
  return expanded;
}

//////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CommittedRegionMap.cpp //
//////////////////////////////////////////////////////

/**
 * 找出Inactive状态的region
 */
HeapRegionRange G1CommittedRegionMap::next_inactive_range(uint offset) const {
  // 从offset偏移量开始, 在位图_inactive中找到第一个为true的索引(Inactive状态的region)
  uint start = (uint) _inactive.find_first_set_bit(offset);
  // return _regions.length()
  if (start == max_length()) {
    // 没找到
    return HeapRegionRange(max_length(), max_length());
  }
  // 从start开始找到第一个为false的索引
  uint end = (uint) _inactive.find_first_clear_bit(start);
  verify_inactive_range(start, end);
  // start到end的范围都是Inactive状态的region
  return HeapRegionRange(start, end);
}

///////////////////////////////////////////////////
// src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////

/**
 * 把region恢复成Active状态
 */
void HeapRegionManager::reactivate_regions(uint start, uint num_regions) {
  assert(num_regions > 0, "No point in calling this for zero regions");
  // 清理一些辅助的数据结构
  clear_auxiliary_data_structures(start, num_regions);
  // 把region恢复成Active状态
  _committed_map.reactivate(start, start + num_regions);
  // 重新初始化region
  initialize_regions(start, num_regions);
}

//////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CommittedRegionMap.cpp //
//////////////////////////////////////////////////////

void G1CommittedRegionMap::reactivate(uint start, uint end) {
  verify_active_count(start, end, 0);
  verify_inactive_count(start, end, (end - start));

  log_debug(gc, heap, region)("Reactivate regions [%u, %u)", start, end);
  // 把_active位图中start到end范围的标志位都设置为true
  active_set_range(start, end);
  // 把_inactive位图中start到end范围的标志位都设置为false
  inactive_clear_range(start, end);
}
```

## 从 Uncommitted 状态的内存中分配 region

```cpp
///////////////////////////////////////////////////
// src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////

uint HeapRegionManager::expand_any(uint num_regions, WorkerThreads* pretouch_workers) {
  assert(num_regions > 0, "Must expand at least 1 region");

  uint offset = 0;
  uint expanded = 0;

  do {
    // 找出Uncommitted的region
    HeapRegionRange regions = _committed_map.next_committable_range(offset);
    if (regions.length() == 0) {
      // 没找到
      break;
    }

    uint to_expand = MIN2(num_regions - expanded, regions.length());
    // 扩容
    expand(regions.start(), to_expand, pretouch_workers);
    expanded += to_expand;
    offset = regions.end();
  } while (expanded < num_regions);

  return expanded;
}

//////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CommittedRegionMap.cpp //
//////////////////////////////////////////////////////

HeapRegionRange G1CommittedRegionMap::next_committable_range(uint offset) const {
  // 确保没有Inactive状态的region
  verify_no_inactive_regons();

  // 此时, _active中为false的region都是Uncommitted的
  uint start = (uint) _active.find_first_clear_bit(offset);
  if (start == max_length()) {
    // 没找到
    return HeapRegionRange(max_length(), max_length());
  }
  // 确定Uncommitted的region的范围
  uint end = (uint) _active.find_first_set_bit(start);
  verify_free_range(start, end);

  return HeapRegionRange(start, end);
}

///////////////////////////////////////////////////
// src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////

void HeapRegionManager::expand(uint start, uint num_regions, WorkerThreads* pretouch_workers) {
  
  commit_regions(start, num_regions, pretouch_workers);
  for (uint i = start; i < start + num_regions; i++) {
    HeapRegion* hr = _regions.get_by_index(i);
    if (hr == nullptr) {
      // 创建一个HeapRegion对象
      hr = new_heap_region(i);
      OrderAccess::storestore();
      _regions.set_by_index(i, hr);
      _allocated_heapregions_length = MAX2(_allocated_heapregions_length, i + 1);
    }
    // 打印日志
    G1CollectedHeap::heap()->hr_printer()->commit(hr);
  }
  // 把region设置成Active状态, 并初始化region
  activate_regions(start, num_regions);
}

void HeapRegionManager::commit_regions(uint index, size_t num_regions, WorkerThreads* pretouch_workers) {
  guarantee(num_regions > 0, "Must commit more than zero regions");
  guarantee(num_regions <= available(),
            "Cannot commit more than the maximum amount of regions");

  _heap_mapper->commit_regions(index, num_regions, pretouch_workers);

  // Also commit auxiliary data
  _bitmap_mapper->commit_regions(index, num_regions, pretouch_workers);

  _bot_mapper->commit_regions(index, num_regions, pretouch_workers);
  _cardtable_mapper->commit_regions(index, num_regions, pretouch_workers);
}
```
