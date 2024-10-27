# 执行 GC

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::collect() {
  // Do timing/tracing/statistics/pre- and post-logging/verification work not
  // directly related to the collection. They should not be accounted for in
  // collection work timing.

  // The G1YoungGCTraceTime message depends on collector state, so must come after
  // determining collector state.
  G1YoungGCTraceTime tm(this, _gc_cause);

  // JFR
  G1YoungGCJFRTracerMark jtm(gc_timer_stw(), gc_tracer_stw(), _gc_cause);
  // JStat/MXBeans
  G1YoungGCMonitoringScope ms(monitoring_support(),
                              !collection_set()->candidates()->is_empty() /* all_memory_pools_affected */);
  // Create the heap printer before internal pause timing to have
  // heap information printed as last part of detailed GC log.
  G1HeapPrinterMark hpm(_g1h);
  // Young GC internal pause timing
  G1YoungGCNotifyPauseMark npm(this);

  // 设置worker线程数, 并启动worker线程
  // worker是实际执行GC的工作线程
  set_young_collection_default_active_worker_threads();

  // 在进行其它操作之前, 先等待根分区扫描完成
  wait_for_root_region_scanning();

  G1YoungGCVerifierMark vm(this);
  {
    // 这里是实际开始回收的地方

    // 记录 Young GC 实际开始的时间
    policy()->record_young_collection_start();
    // 选择回收集
    pre_evacuate_collection_set(jtm.evacuation_info());
    // 记录每个worker线程执行GC的结果
    G1ParScanThreadStateSet per_thread_states(_g1h, // G1堆的指针
                                              // worker线程数
                                              workers()->active_workers(),
                                              // 回收集
                                              collection_set(),
                                              //用来记录每个分区是否疏散(evacuation)失败
                                              // 并记录疏散失败的原因
                                              // 用来加快 post evacuation 阶段的处理速度
                                              &_evac_failure_regions);

    // 进行 Mixed GC 时, 会有部分老年代分区加入到回收集, 这些老年代分区称为 optional region
    bool may_do_optional_evacuation = collection_set()->optional_region_length() != 0;
    // 实际执行疏散回收集的工作
    // The may_do_optional_evacuation flag for the initial collection set
    // evacuation indicates whether one or more optional evacuation steps may
    // follow.
    // If not set, G1 can avoid clearing the card tables of regions that we scan
    // for roots from the heap: when scanning the card table for dirty cards after
    // all remembered sets have been dumped onto it, for optional evacuation we
    // mark these cards as "Scanned" to know that we do not need to re-scan them
    // in the additional optional evacuation passes. This means that in the "Clear
    // Card Table" phase we need to clear those marks. However, if there is no
    // optional evacuation, g1 can immediately clean the dirty cards it encounters
    // as nobody else will be looking at them again, saving the clear card table
    // work later.
    // This case is very common (young only collections and most mixed gcs), so
    // depending on the ratio between scanned and evacuated regions (which g1 always
    // needs to clear), this is a big win.
    evacuate_initial_collection_set(&per_thread_states, may_do_optional_evacuation);

    if (may_do_optional_evacuation) {
      evacuate_optional_collection_set(&per_thread_states);
    }
    post_evacuate_collection_set(jtm.evacuation_info(), &per_thread_states);

    // Refine the type of a concurrent mark operation now that we did the
    // evacuation, eventually aborting it.
    _concurrent_operation_is_full_mark = policy()->concurrent_operation_is_full_mark("Revise IHOP");

    // Need to report the collection pause now since record_collection_pause_end()
    // modifies it to the next state.
    jtm.report_pause_type(collector_state()->young_gc_pause_type(_concurrent_operation_is_full_mark));

    policy()->record_young_collection_end(_concurrent_operation_is_full_mark, evacuation_failed());
  }
  TASKQUEUE_STATS_ONLY(_g1h->task_queues()->print_and_reset_taskqueue_stats("Oop Queue");)
}

```

## 设置 worker 线程数

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::set_young_collection_default_active_worker_threads(){
  uint active_workers = WorkerPolicy::calc_active_workers(workers()->max_workers(),
                                                          workers()->active_workers(),
                                                          Threads::number_of_non_daemon_threads());
  active_workers = workers()->set_active_workers(active_workers);
  log_info(gc,task)("Using %u workers of %u for evacuation", active_workers, workers()->max_workers());
}
```

## 等待根分区扫描完成

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::wait_for_root_region_scanning() {
  Ticks start = Ticks::now();
  // We have to wait until the CM threads finish scanning the
  // root regions as it's the only way to ensure that all the
  // objects on them have been correctly scanned before we start
  // moving them during the GC.
  bool waited = concurrent_mark()->wait_until_root_region_scan_finished();
  Tickspan wait_time;
  if (waited) {
    wait_time = (Ticks::now() - start);
  }
  phase_times()->record_root_region_scan_wait_time(wait_time.seconds() * MILLIUNITS);
}
```

## 选择回收集

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::pre_evacuate_collection_set(G1EvacInfo* evacuation_info) {
  {
    Ticks start = Ticks::now();
    G1PreEvacuateCollectionSetBatchTask cl;
    G1CollectedHeap::heap()->run_batch_task(&cl);
    phase_times()->record_pre_evacuate_prepare_time_ms((Ticks::now() - start).seconds() * 1000.0);
  }

  // 选择回收集
  calculate_collection_set(evacuation_info, policy()->max_pause_time_ms());

  // Please see comment in g1CollectedHeap.hpp and
  // G1CollectedHeap::ref_processing_init() to see how
  // reference processing currently works in G1.
  ref_processor_stw()->start_discovery(false /* always_clear */);

  _evac_failure_regions.pre_collection(_g1h->max_reserved_regions());

  _g1h->gc_prologue(false);

  // Initialize the GC alloc regions.
  allocator()->init_gc_alloc_regions(evacuation_info);

  {
    Ticks start = Ticks::now();
    rem_set()->prepare_for_scan_heap_roots();
    phase_times()->record_prepare_heap_roots_time_ms((Ticks::now() - start).seconds() * 1000.0);
  }

  {
    G1PrepareEvacuationTask g1_prep_task(_g1h);
    Tickspan task_time = run_task_timed(&g1_prep_task);

    _g1h->set_young_gen_card_set_stats(g1_prep_task.all_card_set_stats());
    _g1h->set_humongous_stats(g1_prep_task.humongous_total(), g1_prep_task.humongous_candidates());

    phase_times()->record_register_regions(task_time.seconds() * 1000.0);
  }

  assert(_g1h->verifier()->check_region_attr_table(), "Inconsistency in the region attributes table.");

#if COMPILER2_OR_JVMCI
  DerivedPointerTable::clear();
#endif

  if (collector_state()->in_concurrent_start_gc()) {
    concurrent_mark()->pre_concurrent_start(_gc_cause);
  }

  evac_failure_injector()->arm_if_needed();
}

void G1YoungCollector::calculate_collection_set(G1EvacInfo* evacuation_info, double target_pause_time_ms) {
  // 确定回收集之前需要先让当前正在用于分配对象的分区退休(不能再继续用于分配对象)
  // 因为这个分区也可能被选中加入到回收集中
  allocator()->release_mutator_alloc_regions();

  // G1SurvivorRegions* G1YoungCollector::survivor_regions() const {
  //  return _g1h->survivor();
  // }
  collection_set()->finalize_initial_collection_set(target_pause_time_ms, survivor_regions());
  evacuation_info->set_collection_set_regions(collection_set()->region_length() +
                                              collection_set()->optional_region_length());

  concurrent_mark()->verify_no_collection_set_oops();

  if (hr_printer()->is_active()) {
    G1PrintCollectionSetClosure cl(hr_printer());
    collection_set()->iterate(&cl);
    collection_set()->iterate_optional(&cl);
  }
}

// --- src/hotspot/share/gc/g1/g1CollectionSet.cpp --- //

void G1CollectionSet::finalize_initial_collection_set(double target_pause_time_ms, G1SurvivorRegions* survivor) {
  // 确定新生代分区
  double time_remaining_ms = finalize_young_part(target_pause_time_ms, survivor);
  // 内部有判断, 如果是 Young GC 则跳过, 因为Young GC 阶段不会选择老年代分区
  finalize_old_part(time_remaining_ms);
}

double G1CollectionSet::finalize_young_part(double target_pause_time_ms, G1SurvivorRegions* survivors) {
  Ticks start_time = Ticks::now();

  // void G1CollectionSet::finalize_incremental_building() {
  //   assert(_inc_build_state == Active, "Precondition");
  //   assert(SafepointSynchronize::is_at_safepoint(), "should be at a safepoint");
  // }
  finalize_incremental_building();

  guarantee(target_pause_time_ms > 0.0,
            "target_pause_time_ms = %1.6lf should be positive", target_pause_time_ms);

  // 此时卡表中的脏卡片的数量
  size_t pending_cards = _policy->pending_cards_at_gc_start();

  log_trace(gc, ergo, cset)("Start choosing CSet. Pending cards: " SIZE_FORMAT " target pause time: %1.2fms",
                            pending_cards, target_pause_time_ms);

  // The young list is laid with the survivor regions from the previous
  // pause are appended to the RHS of the young list, i.e.
  //   [Newly Young Regions ++ Survivors from last pause].

  uint eden_region_length = _g1h->eden_regions_count();
  uint survivor_region_length = survivors->length();
  init_region_lengths(eden_region_length, survivor_region_length);

  verify_young_cset_indices();

  double predicted_base_time_ms = _policy->predict_base_time_ms(pending_cards);
  // Base time already includes the whole remembered set related time, so do not add that here
  // again.
  double predicted_eden_time = _policy->predict_young_region_other_time_ms(eden_region_length) +
                               _policy->predict_eden_copy_time_ms(eden_region_length);
  double remaining_time_ms = MAX2(target_pause_time_ms - (predicted_base_time_ms + predicted_eden_time), 0.0);

  log_trace(gc, ergo, cset)("Added young regions to CSet. Eden: %u regions, Survivors: %u regions, "
                            "predicted eden time: %1.2fms, predicted base time: %1.2fms, target pause time: %1.2fms, remaining time: %1.2fms",
                            eden_region_length, survivor_region_length,
                            predicted_eden_time, predicted_base_time_ms, target_pause_time_ms, remaining_time_ms);

  // Clear the fields that point to the survivor list - they are all young now.
  survivors->convert_to_eden();

  phase_times()->record_young_cset_choice_time_ms((Ticks::now() - start_time).seconds() * 1000.0);

  return remaining_time_ms;
}
```
