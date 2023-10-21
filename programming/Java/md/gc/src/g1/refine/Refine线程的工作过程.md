# Refine线程的工作过程

如果没有足够多的引用关系变更，大部分的Refine线程都是空转，所以需要一个机制能动态激活和冻结线程，JVM通过wait和notify机制来实现。假设有n个Refine线程，从0到n-1号线程都是由前一个线程发现自己太忙，激活后一个，后一个线程发现自己太闲的时候则主动冻结自己。第0个线程是由正在运行的Java线程来激活的，当Java线程尝试把修改的引用放入到DCQ时，如果0号线程还没激活，则发送notify信号激活它。0号线程可能会由任意一个用户线程来通知，而1号到n-1号线程只能由前一个Refine线程通知。因为0号线程可以由任意用户线程通知，所以0号线程由一个全局的Monitor通知，而1号到n-1号线程中的Monitor则是局部变量。

Refine线程的工作就是根据DCQ中的引用者找到被引用者，然后在被引用者所在region的RSet中记录引用关系。因为在Refine线程执行的过程中并不会发生GC，也不会发生对象的移动，即对象地址都是固定的，所以不用考虑在执行过程中被引用者的地址发生变化的情况。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\concurrentG1RefineThread.cpp

```cpp
void ConcurrentG1RefineThread::run() {
  // 初始化线程私有信息
  initialize_in_thread();
  wait_for_universe_init();
  // Refine的最后一个线程是抽样线程，用于预测停顿时间并调整新生代region个数
  // _worker_id就是refine线程的编号， 0~n-1，第n个是抽样线程
  if (_worker_id >= cg1r()->worker_thread_num()) {
    // 运行抽样线程
    run_young_rs_sampling();
    // 终止当前线程
    terminate();
    return;
  }
  // Refine线程，处理RSet
  while (!_should_terminate) {
    // DCQS
    DirtyCardQueueSet& dcqs = JavaThread::dirty_card_queue_set();

    // 调用wait()，开始等待有需要处理的DCQ
    wait_for_completed_buffers();
    // 被唤醒，继续执行
    // 先检查是自己否空闲需要冻结
    if (_should_terminate) {
      break;
    }

    {
      SuspendibleThreadSetJoiner sts;

      do {
        // DCQS中的DCQ个数
        int curr_buffer_num = (int)dcqs.completed_buffers_num();
        // If the number of the buffers falls down into the yellow zone,
        // that means that the transition period after the evacuation pause has ended.
        if (dcqs.completed_queue_padding() > 0 && curr_buffer_num <= cg1r()->yellow_zone()) {
          dcqs.set_completed_queue_padding(0);
        }
        // 根据负载判断是否需要停止当前的Refine线程，如果需要则停止
        if (_worker_id > 0 && curr_buffer_num <= _deactivation_threshold) {
          deactivate();
          break;
        }
        // 根据负载判断是否需要通知/启动新的Refine线程，如果需要则发一个通知
        if (_next != NULL && !_next->is_active() && curr_buffer_num > _next->_threshold) {
          _next->activate();
        }
        // 在apply_closure_to_completed_buffer()中处理DCQS
        // green_zone：DCQS分为4个区：白、绿、黄、红，
        // Refine线程只处理绿区及以上的，
        // 而白区到绿区的部分只会在gc的时候处理
      } while (dcqs.apply_closure_to_completed_buffer(_refine_closure, _worker_id + _worker_id_offset, cg1r()->green_zone()));

      // 当有yield请求时退出循环，目的是为了进入安全点
      if (is_active()) {
        deactivate();
      }
    }

  }
  // 终止当前线程
  terminate();
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\dirtyCardQueue.cpp

```cpp
/**
 * 处理DCQS
 */
bool DirtyCardQueueSet::apply_closure_to_completed_buffer(CardTableEntryClosure* cl,
                                                          uint worker_i,
                                                          int stop_at,
                                                          bool during_pause) {
  // 从DCQS中取出一个DCQ来处理
  // stop_at是之前传入的green_zone
  BufferNode* nd = get_completed_buffer(stop_at);
  // 处理DCQ
  bool res = apply_closure_to_completed_buffer_helper(cl, worker_i, nd);
  // _processed_buffers_rs_thread：已处理的DCQ个数
  if (res) Atomic::inc(&_processed_buffers_rs_thread);
  return res;
}

bool DirtyCardQueueSet::apply_closure_to_completed_buffer_helper(CardTableEntryClosure* cl,
                                         uint worker_i,
                                         BufferNode* nd) {
  if (nd != NULL) {
    // BufferNode的数据是在buf中存储的
    void **buf = BufferNode::make_buffer_from_node(nd);
    size_t index = nd->index();
    // 处理DCQ
    bool b =
      DirtyCardQueue::apply_closure_to_buffer(cl, buf,
                                              index, _sz,
                                              true, worker_i);
    if (b) {
      // 处理完成，回收空间
      deallocate_buffer(buf);
      return true;
    } else {
      // 处理失败，重新加入DCQS
      enqueue_complete_buffer(buf, index);
      return false;
    }
  } else {
    return false;
  }
}

bool DirtyCardQueue::apply_closure_to_buffer(CardTableEntryClosure* cl,
                                             void** buf,
                                             size_t index, size_t sz,
                                             bool consume,
                                             uint worker_i) {
  if (cl == NULL) {
    return true;
  }
  for (size_t i = index; i < sz; i += oopSize) {
    int ind = byte_index_to_index((int)i);
    // 取出DCQ中保存的card，card_ptr指向全局卡表中引用者所在的卡片
    jbyte* card_ptr = (jbyte*)buf[ind];
    if (card_ptr != NULL) {
      // 设置buf为NULL，再对buf遍历时就可以快速跳过NULL
      if (consume) {
        buf[ind] = NULL;
      }
      // 处理card
      if (!cl->do_card_ptr(card_ptr, worker_i)) {
        return false;
      }
    }
  }
  return true;
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
class RefineCardTableEntryClosure: public CardTableEntryClosure {
public:
  bool do_card_ptr(jbyte* card_ptr, uint worker_i) {
    // 处理card
    bool oops_into_cset = G1CollectedHeap::heap()->g1_rem_set()->refine_card(card_ptr, worker_i, false);

    if (_concurrent && SuspendibleThreadSet::should_yield()) {
      return false;
    }
    return true;
  }
};
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1RemSet.cpp

```cpp
bool G1RemSet::refine_card(jbyte* card_ptr, uint worker_i,
                           bool check_for_refs_into_cset) {
  // dirty_card_val()返回一个表示dirty的枚举值，
  // 如果card_ptr指向的值不是dirty，
  // 就表示全局卡表中这个card已经不是dirty了，
  // 说明该card_ptr已经处理过了，所以不再需要处理，直接返回
  if (*card_ptr != CardTableModRefBS::dirty_card_val()) {
    return false;
  }
  // 获取card所映射的内存的开始地址
  HeapWord* start = _ct_bs->addr_for(card_ptr);
  // 找到card对应的region
  HeapRegion* r = _g1->heap_region_containing(start);

  // 引用者是新生代或者在CSet中都不需要更新，因为他们都会在GC中被收集
  // 在引用关系通过写屏障进入到DCQ的时候就会被过滤
  // 这里再次过滤，是为了避免并发的问题
  if (r->is_young()) {
    return false;
  }
  // 引用者在CSet中
  if (r->in_collection_set()) {
    return false;
  }

  // G1会把一些热点card，放入hot card cache
  G1HotCardCache* hot_card_cache = _cg1r->hot_card_cache();
  // 判断是否使用了hot card cache
  if (hot_card_cache->use_cache()) {
    // 把当前card加入hot card cache
    // 如果hot card cache中存的太多了，会把最先加入的card移出
    card_ptr = hot_card_cache->insert(card_ptr);
    if (card_ptr == NULL) {
      // hot card会留到后续批量处理
      return false;
    }
    // 此时的card_ptr已经不是传入的card_ptr了，
    // 现在它是从hot card cache中移出的card
    // 需要重新获取card对应的region
    start = _ct_bs->addr_for(card_ptr);
    r = _g1->heap_region_containing(start);
  }

  // 计算card所映射的内存的结束地址
  // 默认一个card对应512字节内存
  HeapWord* end   = start + CardTableModRefBS::card_size_in_words;
  // 声明要处理的内存块，即card映射的内存区
  MemRegion dirtyRegion(start, end);
  // TODO 这段代码不知道干啥的
  G1ParPushHeapRSClosure* oops_in_heap_closure = NULL;
  if (check_for_refs_into_cset) {
    oops_in_heap_closure = _cset_rs_update_cl[worker_i];
  }
  G1UpdateRSOrPushRefOopClosure update_rs_oop_cl(_g1,
                                                 _g1->g1_rem_set(),
                                                 oops_in_heap_closure,
                                                 check_for_refs_into_cset,
                                                 worker_i);
  update_rs_oop_cl.set_from(r);

  G1TriggerClosure trigger_cl;
  FilterIntoCSClosure into_cs_cl(NULL, _g1, &trigger_cl);
  G1InvokeIfNotTriggeredClosure invoke_cl(&trigger_cl, &into_cs_cl);
  G1Mux2Closure mux(&invoke_cl, &update_rs_oop_cl);

  FilterOutOfRegionClosure filter_then_update_rs_oop_cl(r,
                        (check_for_refs_into_cset ?
                                (OopClosure*)&mux :
                                (OopClosure*)&update_rs_oop_cl));
  // 不处理新生代的card
  bool filter_young = true;
  // 处理card
  HeapWord* stop_point =
    r->oops_on_card_seq_iterate_careful(dirtyRegion,
                                        &filter_then_update_rs_oop_cl,
                                        filter_young,
                                        card_ptr);

  // 如果处理中出现问题，比如内存不连续等，
  // 则把该card重新标记为dirty，放入到全局的DCQ，等待后续处理
  if (stop_point != NULL) {
    if (*card_ptr != CardTableModRefBS::dirty_card_val()) {
      *card_ptr = CardTableModRefBS::dirty_card_val();
      MutexLockerEx x(Shared_DirtyCardQ_lock,
                      Mutex::_no_safepoint_check_flag);
      // 全局的DCQ
      DirtyCardQueue* sdcq =
        JavaThread::dirty_card_queue_set().shared_dirty_card_queue();
      sdcq->enqueue(card_ptr);
    }
  } else {
    _conc_refine_cards++;
  }

  // card中如果有引用CSet中的对象时，把has_refs_into_cset设置为true
  bool has_refs_into_cset = trigger_cl.triggered();

  return has_refs_into_cset;
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegion.cpp

```cpp
HeapWord* HeapRegion::oops_on_card_seq_iterate_careful(MemRegion mr,
                                 FilterOutOfRegionClosure* cl,
                                 bool filter_young,
                                 jbyte* card_ptr) {
  if (filter_young) {
    assert(card_ptr != NULL, "pre-condition");
  } else {
    assert(card_ptr == NULL, "pre-condition");
  }
  // 获取Java堆
  G1CollectedHeap* g1h = G1CollectedHeap::heap();

  // 判断你是否处于stop the world的GC
  // TODO 没懂
  if (g1h->is_gc_active()) {
    mr = mr.intersection(MemRegion(bottom(), scan_top()));
  } else {
    mr = mr.intersection(used_region());
  }
  if (mr.is_empty()) {
    return NULL;
  }

  if (is_young() && filter_young) {
    // 当前区域属于新生代region，并且需要过滤掉新生代空间
    return NULL;
  }

  if (card_ptr != NULL) {
    // 把card的dirty标记去掉
    *card_ptr = CardTableModRefBS::clean_card_val();
    // 插入一个StoreLoad内存屏障，保证card的修改对所有线程立即可见
    OrderAccess::storeload();
  }

  // 计算待处理的内存区域的边界
  HeapWord* const start = mr.start();
  HeapWord* const end = mr.end();

  // start指针可能指向某个对象的中间
  // block_start()返回指向对象起始地址的指针
  // ------------------------------------------------
  // |      |某个对象占用的内存空间|                    |
  // ------------------------------------------------
  //        ⬆       ⬆                        ⬆
  //       cur    start                     end
  HeapWord* cur = block_start(start);

  // 处理跨越start的对象
  oop obj;
  HeapWord* next = cur;
  do {
    cur = next;
    obj = oop(cur);
    // 对象在region上是连续排列的，如果为null则后面没有对象了
    if (obj->klass_or_null() == NULL) {
      // 这块内存区域已经不是对象了
      return cur;
    }
    // 继续向后扫描，步长时一个对象的大小
    next = cur + block_size(cur);
  } while (next <= start);

  // while循环执行完：
  // ------------------------------------------------
  // |      |某个对象占用的内存空间|                    |
  // ------------------------------------------------
  //        ⬆       ⬆           ⬆           ⬆
  //       cur    start       next         end

  // 遍历这块内存区域中的对象
  do {
    // 取出cur指向的对象
    obj = oop(cur);
    if (obj->klass_or_null() == NULL) {
      // 这块内存区域已经不是对象了
      return cur;
    }

    // cur移动到下一个对象
    // ------------------------------------------------
    // |      |某个对象占用的内存空间|                    |
    // ------------------------------------------------
    //                ⬆           ⬆           ⬆
    //              start        cur         end
    cur = cur + block_size(cur);
    // 判断对象是否存活
    if (!g1h->is_obj_dead(obj)) {
      // 对象不是数组，或者在start和end之间
      if (!obj->is_objArray() || (((HeapWord*)obj) >= start && cur <= end)) {
        // 在这里更新RSet
        obj->oop_iterate(cl);
      } else {
        // 在这里更新RSet
        obj->oop_iterate(cl, mr);
      }
    }
  } while (cur < end);

  return NULL;
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1OopClosures.inline.hpp

```cpp
template <class T>
inline void G1UpdateRSOrPushRefOopClosure::do_oop_nv(T* p) {
  // 被引用方的对象
  oop obj = oopDesc::load_decode_heap_oop(p);
  if (obj == NULL) {
    return;
  }
  // 获取被引用方对象所在的region，to指向这个region的起始地址
  HeapRegion* to = _g1->heap_region_containing(obj);
  // _from指向引用方对象所在的region的起始地址
  if (_from == to) {
    // 引用方和被引用方在同一个region里
    return;
  }
  // The _record_refs_into_cset flag is true during the RSet
  // updating part of an evacuation pause. It is false at all
  // other times:
  //  * rebuilding the remembered sets after a full GC
  //  * during concurrent refinement.
  //  * updating the remembered sets of regions in the collection
  //    set in the event of an evacuation failure (when deferred
  //    updates are enabled).

  if (_record_refs_into_cset && to->in_collection_set()) {
    // We are recording references that point into the collection
    // set and this particular reference does exactly that...
    // If the referenced object has already been forwarded
    // to itself, we are handling an evacuation failure and
    // we have already visited/tried to copy this object
    // there is no need to retry.
    if (!self_forwarded(obj)) {
      assert(_push_ref_cl != NULL, "should not be null");
      // Push the reference in the refs queue of the G1ParScanThreadState
      // instance for this worker thread.
      _push_ref_cl->do_oop(p);
     }

    // Deferred updates to the CSet are either discarded (in the normal case),
    // or processed (if an evacuation failure occurs) at the end
    // of the collection.
    // See G1RemSet::cleanup_after_oops_into_collection_set_do().
  } else {
    // We either don't care about pushing references that point into the
    // collection set (i.e. we're not during an evacuation pause) _or_
    // the reference doesn't point into the collection set. Either way
    // we add the reference directly to the RSet of the region containing
    // the referenced object.
    assert(to->rem_set() != NULL, "Need per-region 'into' remsets.");
    // 更新被引用方的RSet
    to->rem_set()->add_reference(p, _worker_i);
  }
}
```
