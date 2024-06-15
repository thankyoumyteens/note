# 申请新 region

在分配对象内存时, 如果当前 region 的剩余空间不足以分配这个对象时, 会申请一个新的 region 来分配。

```cpp
// --- src/hotspot/share/gc/g1/g1AllocRegion.cpp --- //

HeapRegion* MutatorAllocRegion::allocate_new_region(size_t word_size,
                                                    bool force) {
  return _g1h->new_mutator_alloc_region(word_size, force, _node_index);
}

// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

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

// --- src/hotspot/share/gc/g1/g1Policy.cpp --- //

/**
 * 判断新生代region是否达到阈值
 */
bool G1Policy::should_allocate_mutator_region() const {
  // uint young_regions_count() const { return _eden.length() + _survivor.length(); }
  uint young_list_length = _g1h->young_regions_count();
  // _young_list_target_length: 新生代region的阈值, 在GC之后会重新计算得到一个合理的值
  return young_list_length < young_list_target_length();
}

// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

/**
 * 把新分配的region标记为eden
 */
void G1CollectedHeap::set_region_short_lived_locked(HeapRegion* hr) {
  _eden.add(hr);
  _policy->set_region_eden(hr);
}
```

## 分配一个新 region

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

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
```

## 更新 rset 的状态

```cpp
// --- src/hotspot/share/gc/g1/g1RemSetTrackingPolicy.cpp --- //

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
