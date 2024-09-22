# doit 函数

VM_Operation 实际要执行的逻辑会写在 doit 函数中。

1. 如果发起 GC 的线程要求的是执行 GC 并分配对象内存(word_size 大于 0), 那么 JVM 会先尝试分配对象, 如果分配成功就可以省去一次 GC
2. 如果分配对象内存失败, 或者发起 GC 的线程要求的只是执行 GC, 那么 JVM 会开始执行增量的垃圾回收(Young GC 或 Mixed GC)
3. GC 执行成功后, 如果需要分配对象(word_size 大于 0), JVM 会再次尝试分配。否则会根据需要执行 Full GC

```cpp
// --- src/hotspot/share/gc/g1/g1VMOperations.cpp --- //

void VM_G1CollectForAllocation::doit() {
  G1CollectedHeap* g1h = G1CollectedHeap::heap();

  if (_word_size > 0) {
    // _word_size大于0表示发起GC的线程同时请求了分配对象, 先尝试分配对象
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
      // 分配对象
      _result = g1h->satisfy_failed_allocation(_word_size, &_gc_succeeded);
    } else if (g1h->should_upgrade_to_full_gc()) {
      // 执行Full GC
      _gc_succeeded = g1h->upgrade_to_full_collection();
    }
  }
}
```

## 判断是否需要执行 Full GC

没有空闲的 region 且堆无法再扩展时, 则需要执行 Full GC。

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.hpp --- //

// 如果增量的垃圾回收需要升级到Full GC, 则返回true
// 没有空闲的region且堆无法再扩展时, 返回true
bool should_upgrade_to_full_gc() const {
  return is_maximal_no_gc() && num_free_regions() == 0;
}

bool is_maximal_no_gc() const override {
  // 没有空闲的region
  // _hrm.available(): 未提交的region个数
  // _regions.length() - _committed_map.num_active()
  return _hrm.available() == 0;
}

// 获取空闲region列表
uint num_free_regions() const {
  // _free_list为空, 表示堆无法再扩展
  // _free_list.length()
  return _hrm.num_free_regions();
}
```

## GC 前的分配尝试

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

HeapWord* G1CollectedHeap::attempt_allocation_at_safepoint(size_t word_size,
                                                           bool expect_null_mutator_alloc_region) {
  assert_at_safepoint_on_vm_thread();
  assert(!_allocator->has_mutator_alloc_region() || !expect_null_mutator_alloc_region,
         "the current alloc region was unexpectedly found to be non-null");

  if (!is_humongous(word_size)) {
    // 复用加锁分后配的代码(此时在安全点中, 没有线程安全问题, 无需获取锁)
    return _allocator->attempt_allocation_locked(word_size);
  } else {
    // 分配大对象
    HeapWord* result = humongous_obj_allocate(word_size);
    if (result != nullptr && policy()->need_to_start_conc_mark("STW humongous allocation")) {
      // 开始并发标记
      collector_state()->set_initiate_conc_mark_if_possible(true);
    }
    return result;
  }

  ShouldNotReachHere();
}
```
