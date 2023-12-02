# 计算对象的新地址

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1MarkSweep.cpp

```cpp
void G1MarkSweep::mark_sweep_phase2() {
  GCTraceTime tm("phase 2", G1Log::fine() && Verbose, true, gc_timer(), gc_tracer()->gc_id());
  GenMarkSweep::trace("2");

  prepare_compaction();
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1MarkSweep_ext.cpp

```cpp
void G1MarkSweep::prepare_compaction() {
  G1PrepareCompactClosure blk;
  G1MarkSweep::prepare_compaction_work(&blk);
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1MarkSweep.cpp

```cpp
void G1MarkSweep::prepare_compaction_work(G1PrepareCompactClosure* blk) {
  G1CollectedHeap* g1h = G1CollectedHeap::heap();
  g1h->heap_region_iterate(blk);
  blk->update_sets();
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
void G1CollectedHeap::heap_region_iterate(HeapRegionClosure* cl) const {
  _hrm.iterate(cl);
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegionManager.cpp

```cpp
void HeapRegionManager::iterate(HeapRegionClosure* blk) const {
  uint len = max_length();

  for (uint i = 0; i < len; i++) {
    if (!is_available(i)) {
      continue;
    }
    bool res = blk->doHeapRegion(at(i));
    if (res) {
      blk->incomplete();
      return;
    }
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1MarkSweep.cpp

```cpp
bool G1PrepareCompactClosure::doHeapRegion(HeapRegion* hr) {
  if (hr->isHumongous()) {
    if (hr->startsHumongous()) {
      oop obj = oop(hr->bottom());
      if (obj->is_gc_marked()) {
        obj->forward_to(obj);
      } else  {
        free_humongous_region(hr);
      }
    } else {
      assert(hr->continuesHumongous(), "Invalid humongous.");
    }
  } else {
    prepare_for_compaction(hr, hr->end());
  }
  return false;
}

void G1PrepareCompactClosure::prepare_for_compaction(HeapRegion* hr, HeapWord* end) {
  if (!is_cp_initialized()) {
    _cp.space = hr;
    _cp.threshold = hr->initialize_threshold();
  }
  prepare_for_compaction_work(&_cp, hr, end);
}

void G1PrepareCompactClosure::prepare_for_compaction_work(CompactPoint* cp,
                                                          HeapRegion* hr,
                                                          HeapWord* end) {
  // 最终调用SCAN_AND_FORWARD()
  hr->prepare_for_compaction(cp);
  _mrbs->clear(MemRegion(hr->compaction_top(), end));
}
```

SCAN_AND_FORWARD()函数定义在 hotspot/src/share/vm/memory/space.hpp 中。这一部分代码是用宏实现的, 主要的工作就是计算每个对象对应新位置的指针, 这个指针表示如果移除垃圾对象之后，它应该在的位置。
