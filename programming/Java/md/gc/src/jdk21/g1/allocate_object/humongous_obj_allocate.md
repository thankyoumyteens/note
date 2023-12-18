# 分配大对象

```cpp
/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

/**
 * 分配大对象
 */
HeapWord* G1CollectedHeap::humongous_obj_allocate(size_t word_size) {
  assert_heap_locked_or_at_safepoint(true /* should_be_vm_thread */);

  _verifier->verify_region_sets_optional();
  // 这个大对象需要用几个region存储
  uint obj_regions = (uint) humongous_obj_size_in_regions(word_size);

  // 尝试从空闲region列表寻找可以存放这个大对象的obj_regions个region,
  // 并返回第1个region的指针
  HeapRegion* humongous_start = _hrm.allocate_humongous(obj_regions);
  if (humongous_start == nullptr) {
    // 空闲列表中的region不够分配,
    // 尝试扩大堆空间后重新分配
    humongous_start = _hrm.expand_and_allocate_humongous(obj_regions);
    if (humongous_start != nullptr) {
      log_debug(gc, ergo, heap)("Heap expansion (humongous allocation request). Allocation request: " SIZE_FORMAT "B",
                                word_size * HeapWordSize);
      policy()->record_new_heap_size(num_regions());
    } else {
      // Policy: Potentially trigger a defragmentation GC.
    }
  }

  HeapWord* result = nullptr;
  if (humongous_start != nullptr) {
    // 大对象分配完成, 初始化内存
    result = humongous_obj_allocate_initialize_regions(humongous_start, obj_regions, word_size);
    assert(result != nullptr, "it should always return a valid result");

    // A successful humongous object allocation changes the used space
    // information of the old generation so we need to recalculate the
    // sizes and update the jstat counters here.
    monitoring_support()->update_sizes();
  }

  _verifier->verify_region_sets_optional();

  return result;
}
```















```cpp
///////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////////////////////

/**
 * 分配一个大对象
 */
HeapRegion* HeapRegionManager::allocate_humongous(uint num_regions) {
  // 大对象只占用1个region, 分配起来简单
  if (num_regions == 1) {
    return allocate_free_region(HeapRegionType::Humongous, G1NUMA::AnyNodeIndex);
  }
  // 大对象占用不止1个region
  return allocate_humongous_from_free_list(num_regions);
}

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

    if (numa->is_enabled() && hr->node_index() < numa->num_active_nodes()) {
      numa->update_statistics(G1NUMAStats::NewRegionAlloc, requested_node_index, hr->node_index());
    }
  }

  return hr;
}

HeapRegion* HeapRegionManager::allocate_humongous_from_free_list(uint num_regions) {
  uint candidate = find_contiguous_in_free_list(num_regions);
  if (candidate == G1_NO_HRM_INDEX) {
    return nullptr;
  }
  return allocate_free_regions_starting_at(candidate, num_regions);
}
```

























```cpp
///////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionManager.cpp //
///////////////////////////////////////////////////////////////////

HeapRegion* HeapRegionManager::expand_and_allocate_humongous(uint num_regions) {
  return allocate_humongous_allow_expand(num_regions);
}

HeapRegion* HeapRegionManager::allocate_humongous_allow_expand(uint num_regions) {
  uint candidate = find_contiguous_allow_expand(num_regions);
  if (candidate == G1_NO_HRM_INDEX) {
    return nullptr;
  }
  expand_exact(candidate, num_regions, G1CollectedHeap::heap()->workers());
  return allocate_free_regions_starting_at(candidate, num_regions);
}
```














```cpp
/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

HeapWord*
G1CollectedHeap::humongous_obj_allocate_initialize_regions(HeapRegion* first_hr,
                                                           uint num_regions,
                                                           size_t word_size) {
  assert(first_hr != nullptr, "pre-condition");
  assert(is_humongous(word_size), "word_size should be humongous");
  assert(num_regions * HeapRegion::GrainWords >= word_size, "pre-condition");

  // 大对象所在的第一个region和最后一个region的索引
  uint first = first_hr->hrm_index();
  uint last = first + num_regions - 1;

  // We need to initialize the region(s) we just discovered. This is
  // a bit tricky given that it can happen concurrently with
  // refinement threads refining cards on these regions and
  // potentially wanting to refine the BOT as they are scanning
  // those cards (this can happen shortly after a cleanup; see CR
  // 6991377). So we have to set up the region(s) carefully and in
  // a specific order.

  // The passed in hr will be the "starts humongous" region. The header
  // of the new object will be placed at the bottom of this region.
  HeapWord* new_obj = first_hr->bottom();

  // First, we need to zero the header of the space that we will be
  // allocating. When we update top further down, some refinement
  // threads might try to scan the region. By zeroing the header we
  // ensure that any thread that will try to scan the region will
  // come across the zero klass word and bail out.
  //
  // NOTE: It would not have been correct to have used
  // CollectedHeap::fill_with_object() and make the space look like
  // an int array. The thread that is doing the allocation will
  // later update the object header to a potentially different array
  // type and, for a very short period of time, the klass and length
  // fields will be inconsistent. This could cause a refinement
  // thread to calculate the object size incorrectly.
  Copy::fill_to_words(new_obj, oopDesc::header_size(), 0);

  // Next, update the metadata for the regions.
  set_humongous_metadata(first_hr, num_regions, word_size, true);

  HeapRegion* last_hr = region_at(last);
  size_t used = byte_size(first_hr->bottom(), last_hr->top());

  increase_used(used);

  for (uint i = first; i <= last; ++i) {
    HeapRegion *hr = region_at(i);
    _humongous_set.add(hr);
    _hr_printer.alloc(hr);
  }

  return new_obj;
}
```
