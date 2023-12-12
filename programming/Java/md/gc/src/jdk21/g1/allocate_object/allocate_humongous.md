# 分配大对象

```cpp
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp

HeapWord* G1CollectedHeap::attempt_allocation_humongous(size_t word_size) {
  ResourceMark rm; // For retrieving the thread names in log messages.

  // The structure of this method has a lot of similarities to
  // attempt_allocation_slow(). The reason these two were not merged
  // into a single one is that such a method would require several "if
  // allocation is not humongous do this, otherwise do that"
  // conditional paths which would obscure its flow. In fact, an early
  // version of this code did use a unified method which was harder to
  // follow and, as a result, it had subtle bugs that were hard to
  // track down. So keeping these two methods separate allows each to
  // be more readable. It will be good to keep these two in sync as
  // much as possible.

  assert_heap_not_locked_and_not_at_safepoint();
  assert(is_humongous(word_size), "attempt_allocation_humongous() "
         "should only be called for humongous allocations");

  // Humongous objects can exhaust the heap quickly, so we should check if we
  // need to start a marking cycle at each humongous object allocation. We do
  // the check before we do the actual allocation. The reason for doing it
  // before the allocation is that we avoid having to keep track of the newly
  // allocated memory while we do a GC.
  if (policy()->need_to_start_conc_mark("concurrent humongous allocation",
                                        word_size)) {
    collect(GCCause::_g1_humongous_allocation);
  }

  // We will loop until a) we manage to successfully perform the
  // allocation or b) we successfully schedule a collection which
  // fails to perform the allocation. b) is the only case when we'll
  // return null.
  HeapWord* result = nullptr;
  for (uint try_count = 1, gclocker_retry_count = 0; /* we'll return */; try_count += 1) {
    bool should_try_gc;
    uint gc_count_before;


    {
      MutexLocker x(Heap_lock);

      size_t size_in_regions = humongous_obj_size_in_regions(word_size);
      // Given that humongous objects are not allocated in young
      // regions, we'll first try to do the allocation without doing a
      // collection hoping that there's enough space in the heap.
      result = humongous_obj_allocate(word_size);
      if (result != nullptr) {
        policy()->old_gen_alloc_tracker()->
          add_allocated_humongous_bytes_since_last_gc(size_in_regions * HeapRegion::GrainBytes);
        return result;
      }

      // Only try a GC if the GCLocker does not signal the need for a GC. Wait until
      // the GCLocker initiated GC has been performed and then retry. This includes
      // the case when the GC Locker is not active but has not been performed.
      should_try_gc = !GCLocker::needs_gc();
      // Read the GC count while still holding the Heap_lock.
      gc_count_before = total_collections();
    }

    if (should_try_gc) {
      bool succeeded;
      result = do_collection_pause(word_size, gc_count_before, &succeeded, GCCause::_g1_humongous_allocation);
      if (result != nullptr) {
        assert(succeeded, "only way to get back a non-null result");
        log_trace(gc, alloc)("%s: Successfully scheduled collection returning " PTR_FORMAT,
                             Thread::current()->name(), p2i(result));
        size_t size_in_regions = humongous_obj_size_in_regions(word_size);
        policy()->old_gen_alloc_tracker()->
          record_collection_pause_humongous_allocation(size_in_regions * HeapRegion::GrainBytes);
        return result;
      }

      if (succeeded) {
        // We successfully scheduled a collection which failed to allocate. No
        // point in trying to allocate further. We'll just return null.
        log_trace(gc, alloc)("%s: Successfully scheduled collection failing to allocate "
                             SIZE_FORMAT " words", Thread::current()->name(), word_size);
        return nullptr;
      }
      log_trace(gc, alloc)("%s: Unsuccessfully scheduled collection allocating " SIZE_FORMAT "",
                           Thread::current()->name(), word_size);
    } else {
      // Failed to schedule a collection.
      if (gclocker_retry_count > GCLockerRetryAllocationCount) {
        log_warning(gc, alloc)("%s: Retried waiting for GCLocker too often allocating "
                               SIZE_FORMAT " words", Thread::current()->name(), word_size);
        return nullptr;
      }
      log_trace(gc, alloc)("%s: Stall until clear", Thread::current()->name());
      // The GCLocker is either active or the GCLocker initiated
      // GC has not yet been performed. Stall until it is and
      // then retry the allocation.
      GCLocker::stall_until_clear();
      gclocker_retry_count += 1;
    }


    // We can reach here if we were unsuccessful in scheduling a
    // collection (because another thread beat us to it) or if we were
    // stalled due to the GC locker. In either can we should retry the
    // allocation attempt in case another thread successfully
    // performed a collection and reclaimed enough space.
    // Humongous object allocation always needs a lock, so we wait for the retry
    // in the next iteration of the loop, unlike for the regular iteration case.
    // Give a warning if we seem to be looping forever.

    if ((QueuedAllocationWarningCount > 0) &&
        (try_count % QueuedAllocationWarningCount == 0)) {
      log_warning(gc, alloc)("%s: Retried allocation %u times for " SIZE_FORMAT " words",
                             Thread::current()->name(), try_count, word_size);
    }
  }

  ShouldNotReachHere();
  return nullptr;
}
```
