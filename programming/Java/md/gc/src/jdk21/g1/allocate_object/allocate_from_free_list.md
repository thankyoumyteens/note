# 分配占用多个 region 的大对象

```cpp
///////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////////////////////

/**
 * 寻找多个region用于分配占用多个region的大对象
 */
HeapRegion* HeapRegionManager::allocate_humongous_from_free_list(uint num_regions) {
  uint candidate = find_contiguous_in_free_list(num_regions);
  if (candidate == G1_NO_HRM_INDEX) {
    return nullptr;
  }
  return allocate_free_regions_starting_at(candidate, num_regions);
}
```
