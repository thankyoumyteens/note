# doit 函数

VM_Operation 实际要执行的逻辑会写在 doit 函数中。

```cpp
// --- src/hotspot/share/gc/g1/g1VMOperations.cpp --- //

void VM_G1CollectForAllocation::doit() {
  G1CollectedHeap* g1h = G1CollectedHeap::heap();

  if (_word_size > 0) {
    // 先尝试分配对象
    _result = g1h->attempt_allocation_at_safepoint(_word_size,
                                                   false /* expect_null_cur_alloc_region */);
    if (_result != nullptr) {
      // 如果对象分配成功,
      // 虽然还没做垃圾回收,
      // 也会认为垃圾回收成功了
      _gc_succeeded = true;
      return;
    }
  }

  GCCauseSetter x(g1h, _gc_cause);
  // 执行垃圾回收
  _gc_succeeded = g1h->do_collection_pause_at_safepoint();

  if (_gc_succeeded) {
    if (_word_size > 0) {
      // An allocation had been requested. Do it, eventually trying a stronger
      // kind of GC.
      _result = g1h->satisfy_failed_allocation(_word_size, &_gc_succeeded);
    } else if (g1h->should_upgrade_to_full_gc()) {
      // There has been a request to perform a GC to free some space. We have no
      // information on how much memory has been asked for. In case there are
      // absolutely no regions left to allocate into, do a full compaction.
      _gc_succeeded = g1h->upgrade_to_full_collection();
    }
  }
}
```

## attempt_allocation_at_safepoint

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

HeapWord* G1CollectedHeap::attempt_allocation_at_safepoint(size_t word_size,
                                                           bool expect_null_mutator_alloc_region) {
  assert_at_safepoint_on_vm_thread();
  assert(!_allocator->has_mutator_alloc_region() || !expect_null_mutator_alloc_region,
         "the current alloc region was unexpectedly found to be non-null");

  if (!is_humongous(word_size)) {
    return _allocator->attempt_allocation_locked(word_size);
  } else {
    HeapWord* result = humongous_obj_allocate(word_size);
    if (result != nullptr && policy()->need_to_start_conc_mark("STW humongous allocation")) {
      collector_state()->set_initiate_conc_mark_if_possible(true);
    }
    return result;
  }

  ShouldNotReachHere();
}
```
