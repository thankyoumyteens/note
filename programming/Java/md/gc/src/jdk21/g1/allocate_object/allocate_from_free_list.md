# 分配占用多个 region 的大对象

```cpp
///////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////////////////////

/**
 * 寻找多个region用于分配占用多个region的大对象
 */
HeapRegion* HeapRegionManager::allocate_humongous_from_free_list(uint num_regions) {
  // 寻找连续的region用于分配大对象
  uint candidate = find_contiguous_in_free_list(num_regions);
  // candidate是连续的region中第一个region的index
  if (candidate == G1_NO_HRM_INDEX) {
    // 没找到
    return nullptr;
  }
  // 分配大对象
  return allocate_free_regions_starting_at(candidate, num_regions);
}

/**
 * 寻找连续的region用于分配占用多个region的大对象
 * 返回的index是连续的region中第一个region的index
 */
uint HeapRegionManager::find_contiguous_in_free_list(uint num_regions) {
  // G1_NO_HRM_INDEX的值是-1
  uint candidate = G1_NO_HRM_INDEX;
  HeapRegionRange range(0,0);

  do {
    // G1CommittedRegionMap记录了region的3种状态: 
    //   1. Uncommitted
    //   2. Active
    //   3. Inactive
    // Active和Inactive状态的region都属于committed
    // 处于Active状态的region可以用于分配对象
    // 3种状态之间的转换:
    //   Uncommitted -> Active      (activate())
    //   Active      -> Inactive    (deactivate())
    //   Inactive    -> Active      (reactivate())
    //   Inactive    -> Uncommitted (uncommit())

    // _committed_map 记录了堆中属于committed的region
    // next_active_range()查找active状态的region的范围
    range = _committed_map.next_active_range(range.end());
    // TODO
    candidate = find_contiguous_in_range(range.start(), range.end(), num_regions);
  } while (candidate == G1_NO_HRM_INDEX && range.end() < reserved_length());

  return candidate;
}

/**
 * 查找active状态的region的范围
 */
HeapRegionRange G1CommittedRegionMap::next_active_range(uint offset) const {

  // CHeapBitMap _active;
  // _active是一个位图, 记录了那些region是active的
  // 从offset开始查找第一个active的region(可以分配对象的region)
  uint start = (uint) _active.find_first_set_bit(offset);
  if (start == max_length()) {
    // 没有active的region, 返回一个无效范围
    return HeapRegionRange(max_length(), max_length());
  }

  // 在_active位图中, 查找从start开始第一个为0的bit位, 
  // 1表示region是active的, 0表示region是inactive的
  uint end = (uint) _active.find_first_clear_bit(start);
  verify_active_range(start, end);
  // 返回一串连续的active的region的范围
  return HeapRegionRange(start, end);
}

// TODO
uint HeapRegionManager::find_contiguous_in_range(uint start, uint end, uint num_regions) {
  assert(start <= end, "precondition");
  assert(num_regions >= 1, "precondition");
  uint candidate = start;       // First region in candidate sequence.
  uint unchecked = candidate;   // First unchecked region in candidate.
  // While the candidate sequence fits in the range...
  while (num_regions <= (end - candidate)) {
    // Walk backward over the regions for the current candidate.
    for (uint i = candidate + num_regions - 1; true; --i) {
      if (is_available(i) && !at(i)->is_free()) {
        // Region i can't be used, so restart with i+1 as the start
        // of a new candidate sequence, and with the region after the
        // old candidate sequence being the first unchecked region.
        unchecked = candidate + num_regions;
        candidate = i + 1;
        break;
      } else if (i == unchecked) {
        // All regions of candidate sequence have passed check.
        assert_contiguous_range(candidate, num_regions);
        return candidate;
      }
    }
  }
  return G1_NO_HRM_INDEX;
}

inline HeapRegion* HeapRegionManager::allocate_free_regions_starting_at(uint first, uint num_regions) {
  HeapRegion* start = at(first);
  _free_list.remove_starting_at(start, num_regions);
  return start;
}
```
