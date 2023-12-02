# 移动对象

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1MarkSweep.cpp

```cpp
void G1MarkSweep::mark_sweep_phase4() {
  G1CollectedHeap* g1h = G1CollectedHeap::heap();
  G1SpaceCompactClosure blk;
  // 便利region, 移动对象
  g1h->heap_region_iterate(&blk);
}

class G1SpaceCompactClosure: public HeapRegionClosure {
public:
  bool doHeapRegion(HeapRegion* hr) {
    if (hr->isHumongous()) {
      if (hr->startsHumongous()) {
        oop obj = oop(hr->bottom());
        if (obj->is_gc_marked()) {
          obj->init_mark();
        } else {
          assert(hr->is_empty(), "Should have been cleared in phase 2.");
        }
        hr->reset_during_compaction();
      }
    } else {
      hr->compact();
    }
    return false;
  }
};
```

> jdk8u60-master\hotspot\src\share\vm\memory\space.cpp

```cpp
void CompactibleSpace::compact() {
  SCAN_AND_COMPACT(obj_size);
}
```

SCAN_AND_COMPACT() 位于 hotspot/src/share/vm/memory/space.inline.hpp。这个宏的主要工作就是: 把对象复制到新的地址, 然后重新设置对象头。
