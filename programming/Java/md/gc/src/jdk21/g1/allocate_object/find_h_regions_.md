# 寻找可以分配大对象的region

```cpp
///////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////////////////////

/**
 * 寻找可以分配大对象的region
 * 这里只返回region, 不会分配
 */
HeapRegion* HeapRegionManager::allocate_humongous(uint num_regions) {
  // 大对象只占用1个region, 分配起来简单, 
  // 直接从空闲region列表中拿一个region给这个大对象分配
  if (num_regions == 1) {
    return allocate_free_region(HeapRegionType::Humongous, G1NUMA::AnyNodeIndex);
  }
  // 大对象占用不止1个region
  return allocate_humongous_from_free_list(num_regions);
}
```
