# 申请新region

```cpp
///////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1AllocRegion.cpp //
///////////////////////////////////////////////////////////////

HeapRegion* MutatorAllocRegion::allocate_new_region(size_t word_size,
                                                    bool force) {
  return _g1h->new_mutator_alloc_region(word_size, force, _node_index);
}

/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

HeapRegion* G1CollectedHeap::new_mutator_alloc_region(size_t word_size,
                                                      bool force,
                                                      uint node_index) {
  assert_heap_locked_or_at_safepoint(true /* should_be_vm_thread */);
  // 判断新生代region是否达到阈值
  bool should_allocate = policy()->should_allocate_mutator_region();
  if (force || should_allocate) {
    // 分配一个新region
    HeapRegion* new_alloc_region = new_region(word_size,
                                              HeapRegionType::Eden,
                                              false /* do_expand */,
                                              node_index);
    if (new_alloc_region != nullptr) {
      // 把新分配的region标记为eden
      set_region_short_lived_locked(new_alloc_region);
      // 打印一些信息
      _hr_printer.alloc(new_alloc_region, !should_allocate);
      // 更新rset的状态
      _policy->remset_tracker()->update_at_allocate(new_alloc_region);
      return new_alloc_region;
    }
  }
  return nullptr;
}

//////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////////////////////

/**
 * 判断新生代region是否达到阈值
 */
bool G1Policy::should_allocate_mutator_region() const {
  // uint young_regions_count() const { return _eden.length() + _survivor.length(); }
  uint young_list_length = _g1h->young_regions_count();
  // _young_list_target_length: 新生代region的阈值, 在GC之后会重新计算得到一个合理的值
  return young_list_length < young_list_target_length();
}

/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

/**
 * 分配一个新region
 */
HeapRegion* G1CollectedHeap::new_region(size_t word_size,
                                        HeapRegionType type,
                                        bool do_expand,
                                        uint node_index) {
  assert(!is_humongous(word_size) || word_size <= HeapRegion::GrainWords,
         "the only time we use this to allocate a humongous region is "
         "when we are allocating a single humongous region");
  // 从空闲region列表中获取一个region
  HeapRegion* res = _hrm.allocate_free_region(type, node_index);

  if (res == nullptr && do_expand) {
    // 空闲region列表中没有region了

    // Currently, only attempts to allocate GC alloc regions set
    // do_expand to true. So, we should only reach here during a
    // safepoint.
    assert(SafepointSynchronize::is_at_safepoint(), "invariant");

    log_debug(gc, ergo, heap)("Attempt heap expansion (region allocation request failed). Allocation request: " SIZE_FORMAT "B",
                              word_size * HeapWordSize);

    assert(word_size * HeapWordSize < HeapRegion::GrainBytes,
           "This kind of expansion should never be more than one region. Size: " SIZE_FORMAT,
           word_size * HeapWordSize);
    // 扩大堆空间
    if (expand_single_region(node_index)) {
      // Given that expand_single_region() succeeded in expanding the heap, and we
      // always expand the heap by an amount aligned to the heap
      // region size, the free list should in theory not be empty.
      // In either case allocate_free_region() will check for null.

      // 堆空间扩容后, 空闲region列表理论上就不是空的了,
      // 再次尝试从空闲region列表中获取一个region
      res = _hrm.allocate_free_region(type, node_index);
    }
  }
  return res;
}

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
    // Try to allocate with requested node index.
    hr = _free_list.remove_region_with_node_index(from_head, requested_node_index);
  }

  if (hr == nullptr) {
    // If there's a single active node or we did not get a region from our requested node,
    // try without requested node index.
    hr = _free_list.remove_region(from_head);
  }

  if (hr != nullptr) {
    assert(hr->next() == nullptr, "Single region should not have next");
    assert(is_available(hr->hrm_index()), "Must be committed");

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
 * 取出空闲region列表的第一个region
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

/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

void G1CollectedHeap::set_region_short_lived_locked(HeapRegion* hr) {
  _eden.add(hr);
  _policy->set_region_eden(hr);
}

////////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1RemSetTrackingPolicy.cpp //
////////////////////////////////////////////////////////////////////////

void G1RemSetTrackingPolicy::update_at_allocate(HeapRegion* r) {
  if (r->is_young()) {
    // Always collect remembered set for young regions.
    r->rem_set()->set_state_complete();
  } else if (r->is_humongous()) {
    // Collect remembered sets for humongous regions by default to allow eager reclaim.
    r->rem_set()->set_state_complete();
  } else if (r->is_old()) {
    // By default, do not create remembered set for new old regions.
    r->rem_set()->set_state_untracked();
  } else {
    guarantee(false, "Unhandled region %u with heap region type %s", r->hrm_index(), r->get_type_str());
  }
}
```