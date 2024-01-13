# 从空闲 region 列表获取 region

```cpp
///////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////////////////////

/**
 * 从空闲region列表中获取一个region
 */
HeapRegion* HeapRegionManager::allocate_free_region(HeapRegionType type, uint requested_node_index) {
  HeapRegion* hr = nullptr;
  bool from_head = !type.is_young();
  G1NUMA* numa = G1NUMA::numa();

  if (requested_node_index != G1NUMA::AnyNodeIndex && numa->is_enabled()) {
    // 如果开启了NUMA, 则从指定的NUMA node上获取region
    hr = _free_list.remove_region_with_node_index(from_head, requested_node_index);
  }

  if (hr == nullptr) {
    // 不使用NUMA获取region
    hr = _free_list.remove_region(from_head);
  }

  if (hr != nullptr) {
    assert(hr->next() == nullptr, "Single region should not have next");
    assert(is_available(hr->hrm_index()), "Must be committed");

    if (numa->is_enabled() && hr->node_index() < numa->num_active_nodes()) {
      // 更新NUMA的统计信息
      numa->update_statistics(G1NUMAStats::NewRegionAlloc, requested_node_index, hr->node_index());
    }
  }

  return hr;
}

//////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionSet.inline.hpp //
//////////////////////////////////////////////////////////////////////

/**
 * 取出空闲region列表的一个region
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
    // 从头节点取
    hr = remove_from_head_impl();
  } else {
    // 从尾节点取
    hr = remove_from_tail_impl();
  }

  if (_last == hr) {
    _last = nullptr;
  }

  // 更新空闲region列表的长度
  remove(hr);

  // 维护NUMA中用到的信息
  decrease_length(hr->node_index());

  return hr;
}

/**
 * 取出头节点的region, 并把它移出空闲region列表
 */
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

/**
 * 取出尾节点的region, 并把它移出空闲region列表
 */
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

inline void HeapRegionSetBase::remove(HeapRegion* hr) {
  check_mt_safety();
  verify_region(hr);
  assert_heap_region_set(hr->next() == nullptr, "should already be unlinked");
  assert_heap_region_set(hr->prev() == nullptr, "should already be unlinked");

  hr->set_containing_set(nullptr);
  assert_heap_region_set(_length > 0, "pre-condition");
  // _length用来记录空闲列表中有几个region
  _length--;
}
```
