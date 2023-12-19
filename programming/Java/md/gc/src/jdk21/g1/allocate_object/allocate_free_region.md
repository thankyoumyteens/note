# 分配占用 1 个 region 的大对象

```cpp
///////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////////////////////

/**
 * 分配占用1个region的大对象
 */
HeapRegion* HeapRegionManager::allocate_free_region(HeapRegionType type, uint requested_node_index) {
  HeapRegion* hr = nullptr;
  bool from_head = !type.is_young();
  G1NUMA* numa = G1NUMA::numa();
  // 判断是否使用NUMA技术
  if (requested_node_index != G1NUMA::AnyNodeIndex && numa->is_enabled()) {
    // Try to allocate with requested node index.
    hr = _free_list.remove_region_with_node_index(from_head, requested_node_index);
  }

  if (hr == nullptr) {
    // 取出空闲region列表的第一个region给大对象分配
    hr = _free_list.remove_region(from_head);
  }

  if (hr != nullptr) {
    assert(hr->next() == nullptr, "Single region should not have next");
    assert(is_available(hr->hrm_index()), "Must be committed");
    // 更新NUMA技术的统计信息
    if (numa->is_enabled() && hr->node_index() < numa->num_active_nodes()) {
      numa->update_statistics(G1NUMAStats::NewRegionAlloc, requested_node_index, hr->node_index());
    }
  }

  return hr;
}

//////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionSet.inline.hpp //
//////////////////////////////////////////////////////////////////////

/**
 * 取出空闲region列表的第一个region给大对象分配
 */
inline HeapRegion* FreeRegionList::remove_region(bool from_head) {
  check_mt_safety();
  verify_optional();

  if (is_empty()) {
    return nullptr;
  }
  assert_free_region_list(length() > 0 && _head != nullptr && _tail != nullptr, "invariant");

  HeapRegion* hr;

  if (from_head) {
    hr = remove_from_head_impl();
  } else {
    hr = remove_from_tail_impl();
  }

  if (_last == hr) {
    _last = nullptr;
  }

  // remove() will verify the region and check mt safety.
  remove(hr);

  decrease_length(hr->node_index());

  return hr;
}

inline HeapRegion* FreeRegionList::remove_from_head_impl() {
  HeapRegion* result = _head;
  _head = result->next();
  if (_head == nullptr) {
    _tail = nullptr;
  } else {
    _head->set_prev(nullptr);
  }
  result->set_next(nullptr);
  return result;
}

inline HeapRegion* FreeRegionList::remove_from_tail_impl() {
  HeapRegion* result = _tail;

  _tail = result->prev();
  if (_tail == nullptr) {
    _head = nullptr;
  } else {
    _tail->set_next(nullptr);
  }
  result->set_prev(nullptr);
  return result;
}
```
