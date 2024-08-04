# 加锁分配

在 CAS 分配中, 会不断循环直到分配成功, 如果 CAS 分配失败了, 那么一定是内存不足导致的。

此时需要加锁分配, 加锁分配的过程:

1. 获取锁, 如果锁被其他线程持有, 本线程会阻塞等待
2. 在当前线索等待锁的过程中, 其它线索可能已经申请了垃圾回收, 并且 JVM 执行完成了垃圾回收
3. 所以当前线程获取到锁后, 首先再尝试一次对象分配
4. 如果还是分配失败, 那么就表示没有其它线程发起垃圾回收, 或者内存空间确实不足了
5. 此时线程会准备执行一次垃圾回收
6. 在执行垃圾回收之前, 当前线程会判断一下 GCLocker 是否会执行垃圾回收
7. 如果 GCLocker 会在稍后执行垃圾回收, 那么本线程就不需要重复执行了, 只需要阻塞等待 GCLocker 执行完垃圾回收后再分配对象即可。在阻塞之前本线程还会再尝试一下: 如果新生代还没用完(还可以申请新的 region), 本线程会扩容新生代(申请一个新 region), 并在新申请的 region 中分配对象。还是失败的话, 就会开始阻塞等待 GCLocker 的垃圾回收了
8. 如果 GCLocker 不行垃圾回收, 那么本线程会自己执行垃圾回收并分配对象的内存

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

/**
 * CAS分配失败, 加锁分配
 */
HeapWord* G1CollectedHeap::attempt_allocation_slow(size_t word_size) {
  ResourceMark rm; // For retrieving the thread names in log messages.

  assert_heap_not_locked_and_not_at_safepoint();
  assert(!is_humongous(word_size), "attempt_allocation_slow() should not "
         "be called for humongous allocation requests");


  // 无限循环, 直到分配成功或内存不足
  HeapWord* result = nullptr;
  for (uint try_count = 1, gclocker_retry_count = 0 ; ; try_count += 1) {
    bool should_try_gc;
    uint gc_count_before;

    {
      // MutexLocker的构造函数会加锁, 析构函数会解锁
      // 创建一个MutexLocker的对象x, 同时加锁
      // 当x脱离作用域时, MutexLocker的析构函数会自动解锁
      MutexLocker x(Heap_lock);

      // 在本线程等待锁时, 其他线程可能已经扩容了region或者进行了GC,
      // 所以拿到锁后, 首先尝试分配对象
      result = _allocator->attempt_allocation_locked(word_size);
      if (result != nullptr) {
        return result;
      }

      // 如果JNI代码在访问临界区时发生了GC, JVM会阻止这次GC, 等到JNI代码退出临界区后再补上这次GC,
      // GCLocker用于管理这些操作, 如果is_active_and_needs_gc()返回true,
      // 则表示有JNI代码在访问临界区, 并且阻止了一次GC, 在退出临界区后, GCLocker会执行一次GC
      //
      // can_expand_young_list()返回当前已经持有的新生代region个数是否小于最大新生代region个数
      // 如果还没有达到最大region个数, 则尝试扩容新生代
      //
      // bool G1Policy::can_expand_young_list() const {
      //   uint young_list_length = _g1h->young_regions_count();
      //   return young_list_length < young_list_max_length();
      // }
      if (GCLocker::is_active_and_needs_gc() && policy()->can_expand_young_list()) {
        // 扩容新生代并分配对象
        result = _allocator->attempt_allocation_force(word_size);
        if (result != nullptr) {
          return result;
        }
      }

      // 加锁分配失败, 且GCLocker稍后不会补上GC时, 需要执行一次GC
      should_try_gc = !GCLocker::needs_gc();
      // 获取之前已经执行的GC次数
      gc_count_before = total_collections();

      // x脱离作用域, MutexLocker的析构函数会自动释放锁
    }

    // 是否需要执行GC
    if (should_try_gc) {
      bool succeeded;
      // 执行GC并分配对象的内存
      result = do_collection_pause(word_size, gc_count_before, &succeeded, GCCause::_g1_inc_collection_pause);
      if (result != nullptr) {
        // 对象分配成功
        assert(succeeded, "only way to get back a non-null result");
        log_trace(gc, alloc)("%s: Successfully scheduled collection returning " PTR_FORMAT,
                             Thread::current()->name(), p2i(result));
        return result;
      }

      if (succeeded) {
        // GC执行成功, 还是不够分配对象, 内存空间不足
        log_trace(gc, alloc)("%s: Successfully scheduled collection failing to allocate "
                             SIZE_FORMAT " words", Thread::current()->name(), word_size);
        return nullptr;
      }
      log_trace(gc, alloc)("%s: Unsuccessfully scheduled collection allocating " SIZE_FORMAT " words",
                           Thread::current()->name(), word_size);
    } else {
      // 本来要执行的GC被GCLocker阻止了
      if (gclocker_retry_count > GCLockerRetryAllocationCount) {
        // GC被GCLocker阻止了太多次, 直接返回null
        log_warning(gc, alloc)("%s: Retried waiting for GCLocker too often allocating "
                               SIZE_FORMAT " words", Thread::current()->name(), word_size);
        return nullptr;
      }
      log_trace(gc, alloc)("%s: Stall until clear", Thread::current()->name());
      // JNI线程还在临界区, 或者GCLocker启动的GC还没有结束,
      // 当前线程需要等待GCLocker处理完成, 然后重新尝试分配对象的内存
      GCLocker::stall_until_clear();
      // 被GCLocker阻止的GC次数
      gclocker_retry_count += 1;
    }

    // 有两种可能会导致代码执行到这里:
    // 1. GC被其他线程打断
    // 2. GC被GCLocker阻止
    // 此时, 其他线程或GCLocker可能已经执行完了GC, 回收了内存空间,
    // 所以再次尝试分配对象内存,
    // 先使用CAS分配, 如果CAS失败, 就会由下一轮循环进行加锁分配
    size_t dummy = 0;
    // 使用CAS分配对象的内存空间
    result = _allocator->attempt_allocation(word_size, word_size, &dummy);
    if (result != nullptr) {
      return result;
    }

    // Give a warning if we seem to be looping forever.
    if ((QueuedAllocationWarningCount > 0) &&
        (try_count % QueuedAllocationWarningCount == 0)) {
      log_warning(gc, alloc)("%s:  Retried allocation %u times for " SIZE_FORMAT " words",
                             Thread::current()->name(), try_count, word_size);
    }
  }

  ShouldNotReachHere();
  return nullptr;
}
```

## 拿到锁后, 尝试分配对象

```cpp
// --- src/hotspot/share/gc/g1/g1Allocator.inline.hpp --- //

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

// --- src/hotspot/share/gc/g1/g1AllocRegion.inline.hpp --- //

inline HeapWord* G1AllocRegion::attempt_allocation_locked(size_t word_size) {
  size_t temp;
  return attempt_allocation_locked(word_size, word_size, &temp);
}

inline HeapWord* G1AllocRegion::attempt_allocation_locked(size_t min_word_size,
                                                          size_t desired_word_size,
                                                          size_t* actual_word_size) {
  // 在当前region分配对象
  HeapWord* result = attempt_allocation(min_word_size, desired_word_size, actual_word_size);
  if (result != nullptr) {
    return result;
  }

  // 申请一个新的region, 并在其中分配对象
  return attempt_allocation_using_new_region(min_word_size, desired_word_size, actual_word_size);
}
```
