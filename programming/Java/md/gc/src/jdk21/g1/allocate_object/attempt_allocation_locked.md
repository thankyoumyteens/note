# 拿到锁后分配

```cpp
////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Allocator.inline.hpp //
////////////////////////////////////////////////////////////////////

/**
 * 拿到锁后, 首先尝试分配对象
 */
inline HeapWord* G1Allocator::attempt_allocation_locked(size_t word_size) {
  uint node_index = current_node_index();
  HeapWord* result = mutator_alloc_region(node_index)->attempt_allocation_locked(word_size);

  assert(result != nullptr || mutator_alloc_region(node_index)->get() == nullptr,
         "Must not have a mutator alloc region if there is no memory, but is " PTR_FORMAT, p2i(mutator_alloc_region(node_index)->get()));
  return result;
}

//////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp //
//////////////////////////////////////////////////////////////////////

inline HeapWord* G1AllocRegion::attempt_allocation_locked(size_t word_size) {
  size_t temp;
  return attempt_allocation_locked(word_size, word_size, &temp);
}

inline HeapWord* G1AllocRegion::attempt_allocation_locked(size_t min_word_size,
                                                          size_t desired_word_size,
                                                          size_t* actual_word_size) {
  HeapWord* result = attempt_allocation(min_word_size, desired_word_size, actual_word_size);
  if (result != nullptr) {
    return result;
  }

  return attempt_allocation_using_new_region(min_word_size, desired_word_size, actual_word_size);
}
```












```cpp
//////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp //
//////////////////////////////////////////////////////////////////////

inline HeapWord* G1AllocRegion::attempt_allocation(size_t min_word_size,
                                                   size_t desired_word_size,
                                                   size_t* actual_word_size) {
  HeapRegion* alloc_region = _alloc_region;
  assert_alloc_region(alloc_region != nullptr, "not initialized properly");
  // 分配对象内存
  HeapWord* result = par_allocate(alloc_region, min_word_size, desired_word_size, actual_word_size);
  if (result != nullptr) {
    trace("alloc", min_word_size, desired_word_size, *actual_word_size, result);
    return result;
  }
  trace("alloc failed", min_word_size, desired_word_size);
  return nullptr;
}

inline HeapWord* G1AllocRegion::par_allocate(HeapRegion* alloc_region,
                                             size_t min_word_size,
                                             size_t desired_word_size,
                                             size_t* actual_word_size) {
  assert(alloc_region != nullptr, "pre-condition");
  assert(!alloc_region->is_empty(), "pre-condition");

  return alloc_region->par_allocate(min_word_size, desired_word_size, actual_word_size);
}

///////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegion.inline.hpp //
///////////////////////////////////////////////////////////////////

inline HeapWord* HeapRegion::par_allocate(size_t min_word_size,
                                          size_t desired_word_size,
                                          size_t* actual_word_size) {
  return par_allocate_impl(min_word_size, desired_word_size, actual_word_size);
}

inline HeapWord* HeapRegion::par_allocate_impl(size_t min_word_size,
                                               size_t desired_word_size,
                                               size_t* actual_size) {
  do {
    HeapWord* obj = top();
    size_t available = pointer_delta(end(), obj);
    size_t want_to_allocate = MIN2(available, desired_word_size);
    if (want_to_allocate >= min_word_size) {
      HeapWord* new_top = obj + want_to_allocate;
      HeapWord* result = Atomic::cmpxchg(&_top, obj, new_top);
      // result can be one of two:
      //  the old top value: the exchange succeeded
      //  otherwise: the new value of the top is returned.
      if (result == obj) {
        assert(is_object_aligned(obj) && is_object_aligned(new_top), "checking alignment");
        *actual_size = want_to_allocate;
        return obj;
      }
    } else {
      return nullptr;
    }
  } while (true);
}
```





















```cpp
//////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp //
//////////////////////////////////////////////////////////////////////

inline HeapWord* G1AllocRegion::attempt_allocation_using_new_region(size_t min_word_size,
                                                                    size_t desired_word_size,
                                                                    size_t* actual_word_size) {
  retire(true /* fill_up */);
  HeapWord* result = new_alloc_region_and_allocate(desired_word_size, false /* force */);
  if (result != nullptr) {
    *actual_word_size = desired_word_size;
    trace("alloc locked (second attempt)", min_word_size, desired_word_size, *actual_word_size, result);
    return result;
  }
  trace("alloc locked failed", min_word_size, desired_word_size);
  return nullptr;
}

///////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1AllocRegion.cpp //
///////////////////////////////////////////////////////////////

HeapWord* G1AllocRegion::new_alloc_region_and_allocate(size_t word_size,
                                                       bool force) {
  assert_alloc_region(_alloc_region == _dummy_region, "pre-condition");
  assert_alloc_region(_used_bytes_before == 0, "pre-condition");

  trace("attempting region allocation");
  HeapRegion* new_alloc_region = allocate_new_region(word_size, force);
  if (new_alloc_region != nullptr) {
    new_alloc_region->reset_pre_dummy_top();
    // Need to do this before the allocation
    _used_bytes_before = new_alloc_region->used();
    HeapWord* result = allocate(new_alloc_region, word_size);
    assert_alloc_region(result != nullptr, "the allocation should succeeded");

    OrderAccess::storestore();
    // Note that we first perform the allocation and then we store the
    // region in _alloc_region. This is the reason why an active region
    // can never be empty.
    update_alloc_region(new_alloc_region);
    trace("region allocation successful");
    return result;
  } else {
    trace("region allocation failed");
    return nullptr;
  }
  ShouldNotReachHere();
}

HeapRegion* G1GCAllocRegion::allocate_new_region(size_t word_size,
                                                 bool force) {
  assert(!force, "not supported for GC alloc regions");
  return _g1h->new_gc_alloc_region(word_size, _purpose, _node_index);
}

/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

HeapRegion* G1CollectedHeap::new_gc_alloc_region(size_t word_size, G1HeapRegionAttr dest, uint node_index) {
  assert(FreeList_lock->owned_by_self(), "pre-condition");

  if (!has_more_regions(dest)) {
    return nullptr;
  }

  HeapRegionType type;
  if (dest.is_young()) {
    type = HeapRegionType::Survivor;
  } else {
    type = HeapRegionType::Old;
  }

  HeapRegion* ne/////////////////////////////////////////////////////////////////
w_alloc_region = new_region(word_size,
                                            type,
                                            true /* do_expand */,
                                            node_index);

  if (new_alloc_region != nullptr) {
    if (type.is_survivor()) {
      new_alloc_region->set_survivor();
      _survivor.add(new_alloc_region);
      register_new_survivor_region_with_region_attr(new_alloc_region);
    } else {
      new_alloc_region->set_old();
    }
    _policy->remset_tracker()->update_at_allocate(new_alloc_region);
    register_region_with_region_attr(new_alloc_region);
    _hr_printer.alloc(new_alloc_region);
    return new_alloc_region;
  }
  return nullptr;
}
```
