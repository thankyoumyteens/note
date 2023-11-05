# RSet 处理

RSet 处理的入口在 scan_remembered_sets()方法中。

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

更新 RSet 就是把引用关系存储到 RSet 对应的 PRT 中。Refine 线程会处理 DCQS 中绿区和黄区的 DCQ，而白区的 DCQ 会留给 GC 线程处理。在 YGC 中会处理白区，其处理方式和 Refine 线程完全一样，区别就是处理的 DCQ 对象不同。YGC 通过 updateRS()方法来更新 RSet。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1RemSet.cpp

```cpp
void G1RemSet::updateRS(DirtyCardQueue* into_cset_dcq, uint worker_i) {
  // 使用closure处理尚未处理的DCQ
  RefineRecordRefsIntoCSCardTableEntryClosure into_cset_update_rs_cl(_g1, into_cset_dcq);
  _g1->iterate_dirty_card_closure(&into_cset_update_rs_cl, into_cset_dcq, false, worker_i);
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
void G1CollectedHeap::iterate_dirty_card_closure(CardTableEntryClosure* cl,
                                                 DirtyCardQueue* into_cset_dcq,
                                                 bool concurrent,
                                                 uint worker_i) {
  // 先处理hot card
  G1HotCardCache* hot_card_cache = _cg1r->hot_card_cache();
  hot_card_cache->drain(worker_i, g1_rem_set(), into_cset_dcq);

  // 处理DCQS中剩下的DCQ
  DirtyCardQueueSet& dcqs = JavaThread::dirty_card_queue_set();
  size_t n_completed_buffers = 0;
  // apply_closure_to_completed_buffer()的第三个参数为0，表示处理所有的DCQ
  while (dcqs.apply_closure_to_completed_buffer(cl, worker_i, 0, true)) {
    n_completed_buffers++;
  }
  dcqs.clear_n_completed_buffers();
}
```

## 扫描 RSet

扫描 RSet 是根据 RSet 的存储信息扫描找到对应的引用者，即根。因为 RSet 内部使用了 3 种不同粒度的存储类型，所以根的大小也会不同，简单地说这个根指的是引用者对应的内存块，这里可能是 512 字节也可能是一整个 region，然后根据内存块找到引用者对象。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1RemSet.cpp

```cpp
void G1RemSet::scanRS(G1ParPushHeapRSClosure* oc,
                      CodeBlobClosure* code_root_cl,
                      uint worker_i) {
  // 每个GC线程会根据自己的编号处理不同范围的region
  // 不同的GC线程不会处理相同的region，所以他们可以并行执行
  HeapRegion *startRegion = _g1->start_cset_region_for_worker(worker_i);
  // 创建处理RSet的closure
  ScanRSClosure scanRScl(oc, code_root_cl, worker_i);
  // 第一次扫描，处理一般对象
  _g1->collection_set_iterate_from(startRegion, &scanRScl);
  // 第二次扫描，处理JIT编译后的代码
  scanRScl.set_try_claimed();
  _g1->collection_set_iterate_from(startRegion, &scanRScl);

  _cards_scanned[worker_i] = scanRScl.cards_done();
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
void G1CollectedHeap::collection_set_iterate_from(HeapRegion* r,
                                                  HeapRegionClosure *cl) {
  if (r == NULL) {
    return;
  }
  // 从cur开始遍历region
  HeapRegion* cur = r;
  while (cur != NULL) {
    HeapRegion* next = cur->next_in_collection_set();
    // 处理region
    if (cl->doHeapRegion(cur) && false) {
      // 标记处理失败
      cl->incomplete();
      return;
    }
    cur = next;
  }
  // 如果本线程已经处理完自己要处理的region，
  // 帮助处理其他线程待处理的region
  cur = g1_policy()->collection_set();
  while (cur != r) {
    HeapRegion* next = cur->next_in_collection_set();
    if (cl->doHeapRegion(cur) && false) {
      cl->incomplete();
      return;
    }
    cur = next;
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1RemSet.cpp

```cpp
class ScanRSClosure : public HeapRegionClosure {
public:
  bool doHeapRegion(HeapRegion* r) {
    // 获取当前region的rset
    HeapRegionRemSet* hrrs = r->rem_set();
    if (hrrs->iter_is_complete()) {
      return false;
    }
    if (!_try_claimed && !hrrs->claim_iter()) {
      return false;
    }
    // 把当前的region加入_dirty_cards_region_list
    // _dirty_cards_region_list用于GC之后清理Rset
    // 因为这个region被回收，所以其Rset也需要清理
    _g1h->push_dirty_cards_region(r);

    HeapRegionRemSetIterator iter(hrrs);
    size_t card_index;
    // _block_size表示一次扫描多少个卡页，这个值是为了提高效率
    // _block_size由参数G1RSetScanBlockSize控制，默认值为64
    size_t jump_to_card = hrrs->iter_claimed_next(_block_size);
    for (size_t current_card = 0; iter.has_next(card_index); current_card++) {
      if (current_card >= jump_to_card + _block_size) {
        jump_to_card = hrrs->iter_claimed_next(_block_size);
      }
      if (current_card < jump_to_card) continue;
      HeapWord* card_start = _g1h->bot_shared()->address_for_index(card_index);
      // 获取card所在的region
      HeapRegion* card_region = _g1h->heap_region_containing(card_start);
      _cards++;
      // 把引用方的region也加入_dirty_cards_region_list
      if (!card_region->is_on_dirty_cards_region_list()) {
        _g1h->push_dirty_cards_region(card_region);
      }

      // 只有引用方的region不在CSet中才需要扫描，
      // 因为在CSet中的region肯定会被回收
      // 如果引用方还没有被处理，则处理这个region
      if (!card_region->in_collection_set() &&
          !_ct_bs->is_card_dirty(card_index)) {
        scanCard(card_index, card_region);
      }
    }
    if (!_try_claimed) {
      // 处理JIT编译的代码
      scan_strong_code_roots(r);
      hrrs->set_iter_complete();
    }
    return false;
  }

  void scanCard(size_t index, HeapRegion *r) {
    // HeapRegionDCTOC是DirtyCardToOopClosure的子类
    HeapRegionDCTOC cl(_g1h, r, _oc,
                       CardTableModRefBS::Precise);

    _oc->set_region(r);
    // card对应的512字节的卡页
    MemRegion card_region(_bot_shared->address_for_index(index), G1BlockOffsetSharedArray::N_words);
    MemRegion pre_gc_allocated(r->bottom(), r->scan_top());
    MemRegion mr = pre_gc_allocated.intersection(card_region);
    if (!mr.is_empty() && !_ct_bs->is_card_claimed(index)) {
      _ct_bs->set_card_claimed(index);
      _cards_done++;
      // 扫描卡页
      cl.do_MemRegion(mr);
    }
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\memory\space.cpp

```cpp
void DirtyCardToOopClosure::do_MemRegion(MemRegion mr) {

  MemRegionClosure* pCl = _sp->preconsumptionDirtyCardClosure();
  if (pCl != NULL) {
    pCl->do_MemRegion(mr);
  }

  HeapWord* bottom = mr.start();
  HeapWord* last = mr.last();
  HeapWord* top = mr.end();
  HeapWord* bottom_obj;
  HeapWord* top_obj;

  bottom_obj = _sp->block_start(bottom);
  top_obj    = _sp->block_start(last);

  top = get_actual_top(top, top_obj);

  if (_precision == CardTableModRefBS::ObjHeadPreciseArray &&
      _min_done != NULL &&
      _min_done < top) {
    top = _min_done;
  }

  bottom = MIN2(bottom, top);
  MemRegion extended_mr = MemRegion(bottom, top);

  if (!extended_mr.is_empty()) {
    // 扫面卡页
    walk_mem_region(extended_mr, bottom_obj, top);
  }

  if (!_cl->idempotent()) {
    _min_done = bottom;
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegion.cpp

```cpp
void HeapRegionDCTOC::walk_mem_region(MemRegion mr,
                                      HeapWord* bottom,
                                      HeapWord* top) {
  G1CollectedHeap* g1h = _g1;
  size_t oop_size;
  HeapWord* cur = bottom;

  // bottom指向mr中第一个对象的地址，
  // top是最后一个对象的地址
  if (!g1h->is_obj_dead(oop(cur), _hr)) {
    oop_size = oop(cur)->oop_iterate(_rs_scan, mr);
  } else {
    oop_size = _hr->block_size(cur);
  }

  cur += oop_size;

  if (cur < top) {
    oop cur_oop = oop(cur);
    oop_size = _hr->block_size(cur);
    HeapWord* next_obj = cur + oop_size;
    // 遍历卡页里面所有的对象
    // 此时卡页中的所有对象都会被作为根，
    // 即使这个老年代对象已经不再存活，
    // 所以这里会产生浮动垃圾
    while (next_obj < top) {
      if (!g1h->is_obj_dead(cur_oop, _hr)) {
        // 遍历引用方对象所有的字段
        // 如果这个字段指向的对象在cset中，即存活
        // 就把这个存活的被引用对象放入队列中等待复制
        cur_oop->oop_iterate(_rs_scan);
      }
      cur = next_obj;
      cur_oop = oop(cur);
      oop_size = _hr->block_size(cur);
      // 因为已经对TLAB、PLAB不用的空间填充了dummy对象，
      // 所以这里通过oop_size可以直接跳过这个dummy对象
      next_obj = cur + oop_size;
    }

    // 处理最后一个对象，
    // 这个对象的起始地址在这个卡页中，
    // 但是结束地址有可能跨卡页，
    // 所以要专门殊处理
    if (!g1h->is_obj_dead(oop(cur), _hr)) {
      oop(cur)->oop_iterate(_rs_scan, mr);
    }
  }
}
```
