# 分配大对象

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

HeapWord* G1CollectedHeap::attempt_allocation_humongous(size_t word_size) {
  ResourceMark rm;

  assert_heap_not_locked_and_not_at_safepoint();
  assert(is_humongous(word_size), "attempt_allocation_humongous() "
         "should only be called for humongous allocations");

  // 大对象会占用大量堆空间, 所以在每个大对象分配之前, 检查是否需要开启并发标记
  if (policy()->need_to_start_conc_mark("concurrent humongous allocation",
                                        word_size)) {
    // 开启并发标记, 并执行GC
    collect(GCCause::_g1_humongous_allocation);
  }

  // 加锁分配对象
  HeapWord* result = nullptr;
  for (uint try_count = 1, gclocker_retry_count = 0 ; ; try_count += 1) {
    bool should_try_gc;
    uint gc_count_before;

    {
      // 加锁
      MutexLocker x(Heap_lock);

      size_t size_in_regions = humongous_obj_size_in_regions(word_size);
      // 大对象不会分配在新生代region中, 
      // 大对象一般比较少, 可能会有足够的空间, 先直接尝试分配
      result = humongous_obj_allocate(word_size);
      if (result != nullptr) {
        policy()->old_gen_alloc_tracker()->
          add_allocated_humongous_bytes_since_last_gc(size_in_regions * HeapRegion::GrainBytes);
        return result;
      }

      // 加锁分配失败, 且GCLocker稍后不会补上GC时, 需要执行一次GC
      should_try_gc = !GCLocker::needs_gc();
      // 获取之前已经执行的GC次数
      gc_count_before = total_collections();
    }

    if (should_try_gc) {
      bool succeeded;
      // 执行GC并分配对象的内存, GCCause标记需要分配大对象
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
        // GC执行成功, 还是不够分配对象, 内存空间不足
        log_trace(gc, alloc)("%s: Successfully scheduled collection failing to allocate "
                             SIZE_FORMAT " words", Thread::current()->name(), word_size);
        return nullptr;
      }
      log_trace(gc, alloc)("%s: Unsuccessfully scheduled collection allocating " SIZE_FORMAT "",
                           Thread::current()->name(), word_size);
    } else {
      // 本来要执行的GC被GCLocker阻止了
      if (gclocker_retry_count > GCLockerRetryAllocationCount) {
        log_warning(gc, alloc)("%s: Retried waiting for GCLocker too often allocating "
                               SIZE_FORMAT " words", Thread::current()->name(), word_size);
        return nullptr;
      }
      log_trace(gc, alloc)("%s: Stall until clear", Thread::current()->name());
      // 当前线程需要等待GCLocker处理完成, 然后在下一轮循环重新尝试分配对象的内存
      GCLocker::stall_until_clear();
      gclocker_retry_count += 1;
    }

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
