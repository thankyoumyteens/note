# YGC 触发的时机

在创建对象时若申请不到内存，则会触发一次 Young GC：

> jdk8u60-master\hotspot\src\share\vm\interpreter\bytecodeInterpreter.cpp

```cpp
// 基于C++的解释器
// Java使用new关键字时会调用到这里
CASE(_new): {
  // 快速分配时不需要GC
  // ...
  // 快速分配失败了，执行慢速分配
  CALL_VM(InterpreterRuntime::_new(THREAD, METHOD->constants(), index),
          handle_exception);
  // ...
}
```

> jdk8u60-master\hotspot\src\share\vm\interpreter\interpreterRuntime.cpp

```cpp
/**
 * 对象的慢速分配
 */
IRT_ENTRY(void, InterpreterRuntime::_new(JavaThread* thread, ConstantPool* pool, int index))
  // ...
  // 创建对象
  oop obj = klass->allocate_instance(CHECK);
  // ...
IRT_END
```

> jdk8u60-master\hotspot\src\share\vm\gc_interface\collectedHeap.inline.hpp

```cpp
/**
 * 申请内存
 */
HeapWord* CollectedHeap::common_mem_allocate_noinit(KlassHandle klass, size_t size, TRAPS) {

  // 从TLAB快速分配时不需要GC
  // ...
  // 从Java堆中分配内存
  bool gc_overhead_limit_was_exceeded = false;
  // Universe::heap ()方法返回的是当前JVM使用的堆类，
  // 因为使用的是G1垃圾回收器，所以返回的是G1CollectedHeap
  result = Universe::heap()->mem_allocate(size,
                                          &gc_overhead_limit_was_exceeded);
  // ...
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
HeapWord* G1CollectedHeap::mem_allocate(size_t word_size,
                                        bool*  gc_overhead_limit_was_exceeded) {
  // 一直循环，直到内存申请成功或者GC后申请失败
  for (uint try_count = 1, gclocker_retry_count = 0; ; try_count += 1) {
    uint gc_count_before;

    HeapWord* result = NULL;
    // 判断是不是大对象
    if (!isHumongous(word_size)) {
      // 不是大对象
      result = attempt_allocation(word_size, &gc_count_before, &gclocker_retry_count);
    } else {
      // 分配大对象
      result = attempt_allocation_humongous(word_size, &gc_count_before, &gclocker_retry_count);
    }
    if (result != NULL) {
      return result;
    }

    // ...
  }
  return NULL;
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.inline.hpp

```cpp
/**
 * 不是大对象的内存分配
 */
inline HeapWord* G1CollectedHeap::attempt_allocation(size_t word_size,
                                                     uint* gc_count_before_ret,
                                                     uint* gclocker_retry_count_ret) {
  AllocationContext_t context = AllocationContext::current();
  // 使用CAS分配
  HeapWord* result = _allocator->mutator_alloc_region(context)->attempt_allocation(word_size,
                                                                                   false);
  if (result == NULL) {
    // 分配失败，进入慢速分配
    result = attempt_allocation_slow(word_size,
                                     context,
                                     gc_count_before_ret,
                                     gclocker_retry_count_ret);
  }
  // ...
  return result;
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
HeapWord* G1CollectedHeap::attempt_allocation_slow(size_t word_size,
                                                   AllocationContext_t context,
                                                   uint* gc_count_before_ret,
                                                   uint* gclocker_retry_count_ret) {
  HeapWord* result = NULL;
  // 循环次数由参数GCLockerRetryAllocationCount控制，默认3次
  for (int try_count = 1; ; try_count += 1) {
    // ...
    if (should_try_gc) {
      // GC后再分配
      bool succeeded;
      result = do_collection_pause(word_size, gc_count_before, &succeeded,
                                   GCCause::_g1_inc_collection_pause);
      if (result != NULL) {
        assert(succeeded, "only way to get back a non-NULL result");
        return result;
      }

      if (succeeded) {
        // 循环次数超出，返回
        MutexLockerEx x(Heap_lock);
        *gc_count_before_ret = total_collections();
        return NULL;
      }
    }
    // ...
  }
}

HeapWord* G1CollectedHeap::do_collection_pause(size_t word_size,
                                               uint gc_count_before,
                                               bool* succeeded,
                                               GCCause::Cause gc_cause) {
  assert_heap_not_locked_and_not_at_safepoint();
  g1_policy()->record_stop_world_start();
  // 要执行的gc任务，false表示不开启并发标记
  VM_G1IncCollectionPause op(gc_count_before,
                             word_size,
                             false, /* should_initiate_conc_mark */
                             g1_policy()->max_pause_time_ms(),
                             gc_cause);

  op.set_allocation_context(AllocationContext::current());
  // GC并分配对象的内存
  VMThread::execute(&op);

  HeapWord* result = op.result();
  bool ret_succeeded = op.prologue_succeeded() && op.pause_succeeded();
  assert(result == NULL || ret_succeeded,
         "the result should be NULL if the VM did not succeed");
  *succeeded = ret_succeeded;

  assert_heap_not_locked();
  return result;
}
```

> jdk8u60-master\hotspot\src\share\vm\runtime\vmThread.cpp

```cpp
void VMThread::execute(VM_Operation* op) {
  // 获取当前线程
  Thread* t = Thread::current();
  // 判断是不是VMThread线程
  if (!t->is_VM_thread()) {
    // 不是VMThread线程，可能是JavaThread或者WatcherThread
    // 会先将任务放到一个队列中，之后再执行
    //...
  } else {
    // 是VMThred线程
    // ...
    _cur_vm_operation = op;
    // 判断任务是否需要在安全点执行且当前不在安全点
    if (op->evaluate_at_safepoint() && !SafepointSynchronize::is_at_safepoint()) {
      // 不在安全点，等待所有线程进入安全点，然后把所有线程暂停
      SafepointSynchronize::begin();
      // 开始gc任务, op是刚刚传入的VM_G1IncCollectionPause的对象
      // evaluate()方法最终会调用VM_G1IncCollectionPause的的doit()方法
      op->evaluate();
      SafepointSynchronize::end();
    } else {
      // 不需要安全点或者在安全点，则直接执行
      op->evaluate();
    }

    // 判断是否需要释放内存空间
    if (op->is_cheap_allocated()) {
      delete op;
    }

    _cur_vm_operation = prev_vm_operation;
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\vm_operations_g1.cpp

```cpp
/**
 * Young GC的准备工作
 */
void VM_G1IncCollectionPause::doit() {
  G1CollectedHeap* g1h = G1CollectedHeap::heap();
  
  if (_word_size > 0) {
    // 再尝试一次分配内存
    _result = g1h->attempt_allocation_at_safepoint(_word_size, allocation_context(),
                                     false);
    if (_result != NULL) {
      _pause_succeeded = true;
      return;
    }
  }

  GCCauseSetter x(g1h, _gc_cause);
  // 这里传入的是false，表示进行Young GC
  if (_should_initiate_conc_mark) {
    _old_marking_cycles_completed_before = g1h->old_marking_cycles_completed();
    bool res = g1h->g1_policy()->force_initial_mark_if_outside_cycle(_gc_cause);
    if (!res) {
      assert(_word_size == 0, "Concurrent Full GC/Humongous Object IM shouldn't be allocating");
      if (_gc_cause != GCCause::_g1_humongous_allocation) {
        _should_retry_gc = true;
      }
      return;
    }
  }
  // Young GC
  _pause_succeeded =
    g1h->do_collection_pause_at_safepoint(_target_pause_time_ms);
  if (_pause_succeeded && _word_size > 0) {
    // Young GC完成，再去申请内存
    _result = g1h->attempt_allocation_at_safepoint(_word_size, allocation_context(),
                                      true);
  } else {
    if (!_pause_succeeded) {
      _should_retry_gc = true;
    }
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
bool G1CollectedHeap::do_collection_pause_at_safepoint(double target_pause_time_ms) {
  assert_at_safepoint(true);
  guarantee(!is_gc_active(), "collection is not reentrant");
  // 判断是否有线程在临界区，如果有则舍弃本次gc，并把need_gc参数设置为true
  if (GC_locker::check_active_before_gc()) {
    return false;
  }

  // 判断此次Young GC是不是一次初次标记
  //（即老年代并发垃圾回收时,会伴随一次youngGC,此时会返回true）
  //纯youngGC阶段这里会返回false
  g1_policy()->decide_on_conc_mark_initiation();

  // 是否处于初始标记停顿阶段(youngGC这里返回的是false)
  bool should_start_conc_mark = g1_policy()->during_initial_mark_pause();

  // Inner scope for scope based logging, timers, and stats collection
  {
    EvacuationInfo evacuation_info;
    if (g1_policy()->during_initial_mark_pause()) {
      increment_old_marking_cycles_started();
      register_concurrent_cycle_start(_gc_timer_stw->gc_start());
    }

    TraceCollectorStats tcs(g1mm()->incremental_collection_counters());
    TraceMemoryManagerStats tms(false /* fullGC */, gc_cause());

    // If the secondary_free_list is not empty, append it to the
    // free_list. No need to wait for the cleanup operation to finish;
    // the region allocation code will check the secondary_free_list
    // and wait if necessary. If the G1StressConcRegionFreeing flag is
    // set, skip this step so that the region allocation code has to
    // get entries from the secondary_free_list.
    if (!G1StressConcRegionFreeing) {
      append_secondary_free_list_if_not_empty_with_lock();
    }

    // Don't dynamically change the number of GC threads this early.  A value of
    // 0 is used to indicate serial work.  When parallel work is done,
    // it will be set.

    { // Call to jvmpi::post_class_unload_events must occur outside of active GC
      IsGCActiveMark x;
      gc_prologue(false);
      increment_total_collections(false /* full gc */);
      increment_gc_time_stamp();

      verify_before_gc();
      check_bitmaps("GC Start");

      COMPILER2_PRESENT(DerivedPointerTable::clear());

      // Please see comment in g1CollectedHeap.hpp and
      // G1CollectedHeap::ref_processing_init() to see how
      // reference processing currently works in G1.

      ref_processor_stw()->enable_discovery(true /*verify_disabled*/,
                                            true /*verify_no_refs*/);

      {
        // We want to temporarily turn off discovery by the
        // CM ref processor, if necessary, and turn it back on
        // on again later if we do. Using a scoped
        // NoRefDiscovery object will do this.
        NoRefDiscovery no_cm_discovery(ref_processor_cm());

        // Forget the current alloc region (we might even choose it to be part
        // of the collection set!).
        _allocator->release_mutator_alloc_region();

        // We should call this after we retire the mutator alloc
        // region(s) so that all the ALLOC / RETIRE events are generated
        // before the start GC event.
        _hr_printer.start_gc(false /* full */, (size_t) total_collections());

        // This timing is only used by the ergonomics to handle our pause target.
        // It is unclear why this should not include the full pause. We will
        // investigate this in CR 7178365.
        //
        // Preserving the old comment here if that helps the investigation:
        //
        // The elapsed time induced by the start time below deliberately elides
        // the possible verification above.
        double sample_start_time_sec = os::elapsedTime();

#if YOUNG_LIST_VERBOSE
        gclog_or_tty->print_cr("\nBefore recording pause start.\nYoung_list:");
        _young_list->print();
        g1_policy()->print_collection_set(g1_policy()->inc_cset_head(), gclog_or_tty);
#endif // YOUNG_LIST_VERBOSE

        g1_policy()->record_collection_pause_start(sample_start_time_sec);

        double scan_wait_start = os::elapsedTime();
        // We have to wait until the CM threads finish scanning the
        // root regions as it's the only way to ensure that all the
        // objects on them have been correctly scanned before we start
        // moving them during the GC.
        bool waited = _cm->root_regions()->wait_until_scan_finished();
        double wait_time_ms = 0.0;
        if (waited) {
          double scan_wait_end = os::elapsedTime();
          wait_time_ms = (scan_wait_end - scan_wait_start) * 1000.0;
        }
        g1_policy()->phase_times()->record_root_region_scan_wait_time(wait_time_ms);

#if YOUNG_LIST_VERBOSE
        gclog_or_tty->print_cr("\nAfter recording pause start.\nYoung_list:");
        _young_list->print();
#endif // YOUNG_LIST_VERBOSE

        if (g1_policy()->during_initial_mark_pause()) {
          concurrent_mark()->checkpointRootsInitialPre();
        }

#if YOUNG_LIST_VERBOSE
        gclog_or_tty->print_cr("\nBefore choosing collection set.\nYoung_list:");
        _young_list->print();
        g1_policy()->print_collection_set(g1_policy()->inc_cset_head(), gclog_or_tty);
#endif // YOUNG_LIST_VERBOSE

        g1_policy()->finalize_cset(target_pause_time_ms, evacuation_info);

        register_humongous_regions_with_in_cset_fast_test();

        assert(check_cset_fast_test(), "Inconsistency in the InCSetState table.");

        _cm->note_start_of_gc();
        // We call this after finalize_cset() to
        // ensure that the CSet has been finalized.
        _cm->verify_no_cset_oops();

        if (_hr_printer.is_active()) {
          HeapRegion* hr = g1_policy()->collection_set();
          while (hr != NULL) {
            _hr_printer.cset(hr);
            hr = hr->next_in_collection_set();
          }
        }

#ifdef ASSERT
        VerifyCSetClosure cl;
        collection_set_iterate(&cl);
#endif // ASSERT

        setup_surviving_young_words();

        // Initialize the GC alloc regions.
        _allocator->init_gc_alloc_regions(evacuation_info);

        // Actually do the work...
        evacuate_collection_set(evacuation_info);

        free_collection_set(g1_policy()->collection_set(), evacuation_info);

        eagerly_reclaim_humongous_regions();

        g1_policy()->clear_collection_set();

        cleanup_surviving_young_words();

        // Start a new incremental collection set for the next pause.
        g1_policy()->start_incremental_cset_building();

        clear_cset_fast_test();

        _young_list->reset_sampled_info();

        // Don't check the whole heap at this point as the
        // GC alloc regions from this pause have been tagged
        // as survivors and moved on to the survivor list.
        // Survivor regions will fail the !is_young() check.
        assert(check_young_list_empty(false /* check_heap */),
          "young list should be empty");

#if YOUNG_LIST_VERBOSE
        gclog_or_tty->print_cr("Before recording survivors.\nYoung List:");
        _young_list->print();
#endif // YOUNG_LIST_VERBOSE

        g1_policy()->record_survivor_regions(_young_list->survivor_length(),
                                             _young_list->first_survivor_region(),
                                             _young_list->last_survivor_region());

        _young_list->reset_auxilary_lists();

        if (evacuation_failed()) {
          _allocator->set_used(recalculate_used());
          uint n_queues = MAX2((int)ParallelGCThreads, 1);
          for (uint i = 0; i < n_queues; i++) {
            if (_evacuation_failed_info_array[i].has_failed()) {
              _gc_tracer_stw->report_evacuation_failed(_evacuation_failed_info_array[i]);
            }
          }
        } else {
          // The "used" of the the collection set have already been subtracted
          // when they were freed.  Add in the bytes evacuated.
          _allocator->increase_used(g1_policy()->bytes_copied_during_gc());
        }

        if (g1_policy()->during_initial_mark_pause()) {
          // We have to do this before we notify the CM threads that
          // they can start working to make sure that all the
          // appropriate initialization is done on the CM object.
          concurrent_mark()->checkpointRootsInitialPost();
          set_marking_started();
          // Note that we don't actually trigger the CM thread at
          // this point. We do that later when we're sure that
          // the current thread has completed its logging output.
        }

        allocate_dummy_regions();

#if YOUNG_LIST_VERBOSE
        gclog_or_tty->print_cr("\nEnd of the pause.\nYoung_list:");
        _young_list->print();
        g1_policy()->print_collection_set(g1_policy()->inc_cset_head(), gclog_or_tty);
#endif // YOUNG_LIST_VERBOSE

        _allocator->init_mutator_alloc_region();

        {
          size_t expand_bytes = g1_policy()->expansion_amount();
          if (expand_bytes > 0) {
            size_t bytes_before = capacity();
            // No need for an ergo verbose message here,
            // expansion_amount() does this when it returns a value > 0.
            if (!expand(expand_bytes)) {
              // We failed to expand the heap. Cannot do anything about it.
            }
          }
        }

        // We redo the verification but now wrt to the new CSet which
        // has just got initialized after the previous CSet was freed.
        _cm->verify_no_cset_oops();
        _cm->note_end_of_gc();

        // This timing is only used by the ergonomics to handle our pause target.
        // It is unclear why this should not include the full pause. We will
        // investigate this in CR 7178365.
        double sample_end_time_sec = os::elapsedTime();
        double pause_time_ms = (sample_end_time_sec - sample_start_time_sec) * MILLIUNITS;
        g1_policy()->record_collection_pause_end(pause_time_ms, evacuation_info);

        MemoryService::track_memory_usage();

        // In prepare_for_verify() below we'll need to scan the deferred
        // update buffers to bring the RSets up-to-date if
        // G1HRRSFlushLogBuffersOnVerify has been set. While scanning
        // the update buffers we'll probably need to scan cards on the
        // regions we just allocated to (i.e., the GC alloc
        // regions). However, during the last GC we called
        // set_saved_mark() on all the GC alloc regions, so card
        // scanning might skip the [saved_mark_word()...top()] area of
        // those regions (i.e., the area we allocated objects into
        // during the last GC). But it shouldn't. Given that
        // saved_mark_word() is conditional on whether the GC time stamp
        // on the region is current or not, by incrementing the GC time
        // stamp here we invalidate all the GC time stamps on all the
        // regions and saved_mark_word() will simply return top() for
        // all the regions. This is a nicer way of ensuring this rather
        // than iterating over the regions and fixing them. In fact, the
        // GC time stamp increment here also ensures that
        // saved_mark_word() will return top() between pauses, i.e.,
        // during concurrent refinement. So we don't need the
        // is_gc_active() check to decided which top to use when
        // scanning cards (see CR 7039627).
        increment_gc_time_stamp();

        verify_after_gc();
        check_bitmaps("GC End");

        assert(!ref_processor_stw()->discovery_enabled(), "Postcondition");
        ref_processor_stw()->verify_no_references_recorded();

        // CM reference discovery will be re-enabled if necessary.
      }

      // We should do this after we potentially expand the heap so
      // that all the COMMIT events are generated before the end GC
      // event, and after we retire the GC alloc regions so that all
      // RETIRE events are generated before the end GC event.
      _hr_printer.end_gc(false /* full */, (size_t) total_collections());

#ifdef TRACESPINNING
      ParallelTaskTerminator::print_termination_counts();
#endif

      gc_epilogue(false);
    }

    // Print the remainder of the GC log output.
    log_gc_footer(os::elapsedTime() - pause_start_sec);

    // It is not yet to safe to tell the concurrent mark to
    // start as we have some optional output below. We don't want the
    // output from the concurrent mark thread interfering with this
    // logging output either.

    _hrm.verify_optional();
    verify_region_sets_optional();

    TASKQUEUE_STATS_ONLY(if (ParallelGCVerbose) print_taskqueue_stats());
    TASKQUEUE_STATS_ONLY(reset_taskqueue_stats());

    print_heap_after_gc();
    trace_heap_after_gc(_gc_tracer_stw);

    // We must call G1MonitoringSupport::update_sizes() in the same scoping level
    // as an active TraceMemoryManagerStats object (i.e. before the destructor for the
    // TraceMemoryManagerStats is called) so that the G1 memory pools are updated
    // before any GC notifications are raised.
    g1mm()->update_sizes();

    _gc_tracer_stw->report_evacuation_info(&evacuation_info);
    _gc_tracer_stw->report_tenuring_threshold(_g1_policy->tenuring_threshold());
    _gc_timer_stw->register_gc_end();
    _gc_tracer_stw->report_gc_end(_gc_timer_stw->gc_end(), _gc_timer_stw->time_partitions());
  }
  // It should now be safe to tell the concurrent mark thread to start
  // without its logging output interfering with the logging output
  // that came from the pause.

  if (should_start_conc_mark) {
    // CAUTION: after the doConcurrentMark() call below,
    // the concurrent marking thread(s) could be running
    // concurrently with us. Make sure that anything after
    // this point does not assume that we are the only GC thread
    // running. Note: of course, the actual marking work will
    // not start until the safepoint itself is released in
    // SuspendibleThreadSet::desynchronize().
    doConcurrentMark();
  }

  return true;
}

void G1CollectedHeap::evacuate_collection_set(EvacuationInfo& evacuation_info) {
  _expand_heap_after_alloc_failure = true;
  _evacuation_failed = false;

  // Should G1EvacuationFailureALot be in effect for this GC?
  NOT_PRODUCT(set_evacuation_failure_alot_for_current_gc();)

  g1_rem_set()->prepare_for_oops_into_collection_set_do();

  // Disable the hot card cache.
  G1HotCardCache* hot_card_cache = _cg1r->hot_card_cache();
  hot_card_cache->reset_hot_cache_claimed_index();
  hot_card_cache->set_use_cache(false);

  uint n_workers;
  if (G1CollectedHeap::use_parallel_gc_threads()) {
    n_workers =
      AdaptiveSizePolicy::calc_active_workers(workers()->total_workers(),
                                     workers()->active_workers(),
                                     Threads::number_of_non_daemon_threads());
    assert(UseDynamicNumberOfGCThreads ||
           n_workers == workers()->total_workers(),
           "If not dynamic should be using all the  workers");
    workers()->set_active_workers(n_workers);
    set_par_threads(n_workers);
  } else {
    assert(n_par_threads() == 0,
           "Should be the original non-parallel value");
    n_workers = 1;
  }


  init_for_evac_failure(NULL);

  rem_set()->prepare_for_younger_refs_iterate(true);

  assert(dirty_card_queue_set().completed_buffers_num() == 0, "Should be empty");
  double start_par_time_sec = os::elapsedTime();
  double end_par_time_sec;

  {
    G1RootProcessor root_processor(this);
    G1ParTask g1_par_task(this, _task_queues, &root_processor);
    // InitialMark needs claim bits to keep track of the marked-through CLDs.
    if (g1_policy()->during_initial_mark_pause()) {
      ClassLoaderDataGraph::clear_claimed_marks();
    }

    if (G1CollectedHeap::use_parallel_gc_threads()) {
      // The individual threads will set their evac-failure closures.
      if (ParallelGCVerbose) G1ParScanThreadState::print_termination_stats_hdr();
      // These tasks use ShareHeap::_process_strong_tasks
      assert(UseDynamicNumberOfGCThreads ||
             workers()->active_workers() == workers()->total_workers(),
             "If not dynamic should be using all the  workers");
      workers()->run_task(&g1_par_task);
    } else {
      g1_par_task.set_for_termination(n_workers);
      g1_par_task.work(0);
    }
    end_par_time_sec = os::elapsedTime();

    // Closing the inner scope will execute the destructor
    // for the G1RootProcessor object. We record the current
    // elapsed time before closing the scope so that time
    // taken for the destructor is NOT included in the
    // reported parallel time.
  }

  G1GCPhaseTimes* phase_times = g1_policy()->phase_times();

  double par_time_ms = (end_par_time_sec - start_par_time_sec) * 1000.0;
  phase_times->record_par_time(par_time_ms);

  double code_root_fixup_time_ms =
        (os::elapsedTime() - end_par_time_sec) * 1000.0;
  phase_times->record_code_root_fixup_time(code_root_fixup_time_ms);

  set_par_threads(0);

  // Process any discovered reference objects - we have
  // to do this _before_ we retire the GC alloc regions
  // as we may have to copy some 'reachable' referent
  // objects (and their reachable sub-graphs) that were
  // not copied during the pause.
  process_discovered_references(n_workers);

  if (G1StringDedup::is_enabled()) {
    double fixup_start = os::elapsedTime();

    G1STWIsAliveClosure is_alive(this);
    G1KeepAliveClosure keep_alive(this);
    G1StringDedup::unlink_or_oops_do(&is_alive, &keep_alive, true, phase_times);

    double fixup_time_ms = (os::elapsedTime() - fixup_start) * 1000.0;
    phase_times->record_string_dedup_fixup_time(fixup_time_ms);
  }

  _allocator->release_gc_alloc_regions(n_workers, evacuation_info);
  g1_rem_set()->cleanup_after_oops_into_collection_set_do();

  // Reset and re-enable the hot card cache.
  // Note the counts for the cards in the regions in the
  // collection set are reset when the collection set is freed.
  hot_card_cache->reset_hot_cache();
  hot_card_cache->set_use_cache(true);

  purge_code_root_memory();

  if (g1_policy()->during_initial_mark_pause()) {
    // Reset the claim values set during marking the strong code roots
    reset_heap_region_claim_values();
  }

  finalize_for_evac_failure();

  if (evacuation_failed()) {
    remove_self_forwarding_pointers();

    // Reset the G1EvacuationFailureALot counters and flags
    // Note: the values are reset only when an actual
    // evacuation failure occurs.
    NOT_PRODUCT(reset_evacuation_should_fail();)
  }

  // Enqueue any remaining references remaining on the STW
  // reference processor's discovered lists. We need to do
  // this after the card table is cleaned (and verified) as
  // the act of enqueueing entries on to the pending list
  // will log these updates (and dirty their associated
  // cards). We need these updates logged to update any
  // RSets.
  enqueue_discovered_references(n_workers);

  redirty_logged_cards();
  COMPILER2_PRESENT(DerivedPointerTable::update_pointers());
}

```
