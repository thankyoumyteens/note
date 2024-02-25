# 扩大堆空间

```cpp
/////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

bool G1CollectedHeap::expand_single_region(uint node_index) {
  uint expanded_by = _hrm.expand_on_preferred_node(node_index);

  if (expanded_by == 0) {
    assert(is_maximal_no_gc(), "Should be no regions left, available: %u", _hrm.available());
    log_debug(gc, ergo, heap)("Did not expand the heap (heap already fully expanded)");
    return false;
  }

  policy()->record_new_heap_size(num_regions());
  return true;
}
```