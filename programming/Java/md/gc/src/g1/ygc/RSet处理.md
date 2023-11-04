# RSet 处理

RSet 处理的入口在 scan_remembered_sets()中。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1RootProcessor.cpp

```cpp
void G1RootProcessor::scan_remembered_sets(G1ParPushHeapRSClosure* scan_rs,
                                           OopClosure* scan_non_heap_weak_roots,
                                           uint worker_i) {
  G1GCPhaseTimes* phase_times = _g1h->g1_policy()->phase_times();
  G1GCParPhaseTimesTracker x(phase_times, G1GCPhaseTimes::CodeCacheRoots, worker_i);

  G1CodeBlobClosure scavenge_cs_nmethods(scan_non_heap_weak_roots);

  _g1h->g1_rem_set()->oops_into_collection_set_do(scan_rs, &scavenge_cs_nmethods, worker_i);
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1RemSet.cpp

```cpp
void G1RemSet::oops_into_collection_set_do(G1ParPushHeapRSClosure* oc,
                                           CodeBlobClosure* code_root_cl,
                                           uint worker_i) {

  _cset_rs_update_cl[worker_i] = oc;

  // 这里使用的DCQ不同于Java线程里面的DCQ，
  // Java线程里面的DCQ是为了记录Java线程在运行时的引用关系，
  // 而这个DCQ是为了记录GC过程中发生失败时要保留的引用关系
  DirtyCardQueue into_cset_dcq(&_g1->into_cset_dirty_card_queue_set());
  // 更新RSet
  updateRS(&into_cset_dcq, worker_i);
  // 扫描RSet
  scanRS(oc, code_root_cl, worker_i);

  _cset_rs_update_cl[worker_i] = NULL;
}
```

## 更新 RSet

更新 RSet 就是把引用关系存储到 RSet 对应的 PRT 中。



## 扫描 RSet

扫描 RSet 是根据 RSet 的存储信息扫描找到对应的引用者，即根。因为 RSet 内部使用了 3 种不同粒度的存储类型，所以根的大小也会不同，简单地说这个根指的是引用者对应的内存块，这里可能是 512 字节也可能是一整个 region，然后根据内存块找到引用者对象。
