# 扩容后重新分配

```cpp
///////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////////////////////

HeapRegion* HeapRegionManager::expand_and_allocate_humongous(uint num_regions) {
  return allocate_humongous_allow_expand(num_regions);
}

HeapRegion* HeapRegionManager::allocate_humongous_allow_expand(uint num_regions) {
  uint candidate = find_contiguous_allow_expand(num_regions);
  if (candidate == G1_NO_HRM_INDEX) {
    // 堆中没有足够的空闲region
    return nullptr;
  }
  // 把找到的region放入空闲列表
  expand_exact(candidate, num_regions, G1CollectedHeap::heap()->workers());
  // 返回第1个region的指针
  return allocate_free_regions_starting_at(candidate, num_regions);
}

uint HeapRegionManager::find_contiguous_allow_expand(uint num_regions) {
  // available()返回iuncommitted的region个数
  if (num_regions > available()) {
    return G1_NO_HRM_INDEX;
  }
  // 从整个堆空间中查找可以分配大对象的region列表
  // reserved_length()返回G1堆中的region数量
  return find_contiguous_in_range(0, reserved_length(), num_regions);
}

/**
 * 返回可以分配大对象的region列表的起始region
 */
uint HeapRegionManager::find_contiguous_in_range(uint start, uint end, uint num_regions) {
  assert(start <= end, "precondition");
  assert(num_regions >= 1, "precondition");
  // 把start作为候选region
  uint candidate = start;
  // 待检查的region
  uint unchecked = candidate;

  while (num_regions <= (end - candidate)) {
    // 从第num_regions个region往前遍历
    for (uint i = candidate + num_regions - 1; true; --i) {
      // 检查region是否active且空闲
      if (is_available(i) && !at(i)->is_free()) {
        // 跳过num_regions个region
        unchecked = candidate + num_regions;
        candidate = i + 1;
        break;
      } else if (i == unchecked) {
        // unchecked是起始region, i从后往前遍历,
        // i == unchecked时, 大对象所需的region已经检查完成
        assert_contiguous_range(candidate, num_regions);
        return candidate;
      }
    }
  }
  // 没找到
  return G1_NO_HRM_INDEX;
}

void HeapRegionManager::expand_exact(uint start, uint num_regions, WorkerThreads* pretouch_workers) {
  assert(num_regions != 0, "Need to request at least one region");
  uint end = start + num_regions;

  for (uint i = start; i < end; i++) {
    // 如果region i是inactive状态的, 在它变为uncommitted之前, 尝试重新设为active
    if (_committed_map.inactive(i)) {
      // 加锁
      MutexLocker uc(Uncommit_lock, Mutex::_no_safepoint_check_flag);
      // region i的状态可能在等待锁时改变, 再次检查
      if (_committed_map.inactive(i)) {
        // 把region设为active
        reactivate_regions(i, 1);
      }
    }
    // 在等待锁的时候, region i已经被其他线程变为uncommitted了
    if (!_committed_map.active(i)) {
      expand(i, 1, pretouch_workers);
    }

    assert(at(i)->is_free(), "Region must be free at this point");
  }

  verify_optional();
}

void HeapRegionManager::expand(uint start, uint num_regions, WorkerThreads* pretouch_workers) {
  commit_regions(start, num_regions, pretouch_workers);
  for (uint i = start; i < start + num_regions; i++) {
    HeapRegion* hr = _regions.get_by_index(i);
    if (hr == nullptr) {
      // 从堆空间分配一个新的region
      hr = new_heap_region(i);
      OrderAccess::storestore();
      _regions.set_by_index(i, hr);
      _allocated_heapregions_length = MAX2(_allocated_heapregions_length, i + 1);
    }
    G1CollectedHeap::heap()->hr_printer()->commit(hr);
  }
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

//////////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionManager.inline.hpp //
//////////////////////////////////////////////////////////////////////////

inline HeapRegion* HeapRegionManager::allocate_free_regions_starting_at(uint first, uint num_regions) {
  // 获取索引对应的region
  HeapRegion* start = at(first);
  // 从空闲列表中删除分配给大对象的region
  _free_list.remove_starting_at(start, num_regions);
  return start;
}
```
