# 填充dummy对象

```cpp
// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/threadLocalAllocBuffer.cpp
void ThreadLocalAllocBuffer::retire_before_allocation() {
  _refill_waste += (unsigned int)remaining();
  retire();
}

size_t ThreadLocalAllocBuffer::remaining() {
  if (end() == nullptr) {
    return 0;
  }

  return pointer_delta(hard_end(), top());
}

void ThreadLocalAllocBuffer::retire(ThreadLocalAllocStats* stats) {
  if (stats != nullptr) {
    accumulate_and_reset_statistics(stats);
  }

  if (end() != nullptr) {
    //   void invariants() const { assert(top() >= start() && top() <= end(), "invalid tlab"); }
    invariants();
    // 记录这个线程已经申请的空间
    //   void incr_allocated_bytes(jlong size) { _allocated_bytes += size; }
    // size_t used_bytes() const                      { return pointer_delta(top(), start(), 1); }
    thread()->incr_allocated_bytes(used_bytes());
    // 填充dummy对象
    insert_filler();
    // 把TLAB相关指针置空, 丢弃当前TLAB的管理权
    initialize(nullptr, nullptr, nullptr);
  }
}

void ThreadLocalAllocBuffer::accumulate_and_reset_statistics(ThreadLocalAllocStats* stats) {
  Thread* thr     = thread();
  size_t capacity = Universe::heap()->tlab_capacity(thr);
  size_t used     = Universe::heap()->tlab_used(thr);

  _gc_waste += (unsigned)remaining();
  size_t total_allocated = thr->allocated_bytes();
  size_t allocated_since_last_gc = total_allocated - _allocated_before_last_gc;
  _allocated_before_last_gc = total_allocated;

  print_stats("gc");

  if (_number_of_refills > 0) {
    // Update allocation history if a reasonable amount of eden was allocated.
    bool update_allocation_history = used > 0.5 * capacity;

    if (update_allocation_history) {
      // Average the fraction of eden allocated in a tlab by this
      // thread for use in the next resize operation.
      // _gc_waste is not subtracted because it's included in
      // "used".
      // The result can be larger than 1.0 due to direct to old allocations.
      // These allocations should ideally not be counted but since it is not possible
      // to filter them out here we just cap the fraction to be at most 1.0.
      // Keep alloc_frac as float and not double to avoid the double to float conversion
      float alloc_frac = MIN2(1.0f, allocated_since_last_gc / (float) used);
      _allocation_fraction.sample(alloc_frac);
    }

    stats->update_fast_allocations(_number_of_refills,
                                   _allocated_size,
                                   _gc_waste,
                                   _refill_waste);
  } else {
    assert(_number_of_refills == 0 && _refill_waste == 0 && _gc_waste == 0,
           "tlab stats == 0");
  }

  stats->update_slow_allocations(_slow_allocations);

  reset_statistics();
}

void ThreadLocalAllocBuffer::insert_filler() {
  assert(end() != nullptr, "Must not be retired");
  if (top() < hard_end()) {
    Universe::heap()->fill_with_dummy_object(top(), hard_end(), true);
  }
}

void ThreadLocalAllocBuffer::initialize(HeapWord* start,
                                        HeapWord* top,
                                        HeapWord* end) {
  set_start(start);
  set_top(top);
  set_pf_top(top);
  set_end(end);
  set_allocation_end(end);
  invariants();
}
```

```cpp
// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/collectedHeap.cpp
void CollectedHeap::fill_with_dummy_object(HeapWord* start, HeapWord* end, bool zap) {
  CollectedHeap::fill_with_object(start, end, zap);
}
```