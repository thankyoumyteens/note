# 启动 Mixed GC

在并发标记结束后，会通过 g1_policy->record_concurrent_mark_cleanup_completed() 设置标记，在下一次增量收集的时候，会判断是否可以开始 Mixed GC。判断的依据主要是根据 CSet 中可回收的 region 信息。

是否可以启动 Mixed GC 的两个前提条件：

1. 并发标记已经结束，更新好 CSet Chooser，用于下一次 CSet 的选择
2. Young GC 结束，判断是否可以进行 Mixed GC

判断的依据在 next_gc_should_be_mixed 中：

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectorPolicy.cpp

```cpp
bool G1CollectorPolicy::next_gc_should_be_mixed(const char* true_action_str,
                                                const char* false_action_str) {
  CollectionSetChooser* cset_chooser = _collectionSetChooser;
  if (cset_chooser->is_empty()) {
    return false;
  }

  // 可回收的空间大小
  size_t reclaimable_bytes = cset_chooser->remaining_reclaimable_bytes();
  // 可回收的空间大小占G1堆总空间大小的比例
  double reclaimable_perc = reclaimable_bytes_perc(reclaimable_bytes);
  // 最小可以浪费的空间G1HeapWastePercent，默认值是5
  double threshold = (double) G1HeapWastePercent;
  if (reclaimable_perc <= threshold) {
    return false;
  }
  // 可回收的空间大小占G1堆总空间大小的比例大于G1HeapWastePercent，
  // 开始Mixed GC
  return true;
}
```

在下一次对象分配失败，需要 GC 的时候会开始 Mixed GC，这部分代码和 Young GC 完全一致，唯一不同的就是 CSet 的处理。在真正的回收时候，会根据预测时间来选择要回收的 region，其主要代码在 G1CollectorPolicy::finalize_cset 中：

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectorPolicy.cpp

```cpp
/**
 * 这个方法会在执行Young GC的
 * G1CollectedHeap::do_collection_pause_at_safepoint()方法中
 * 被调用
 */
void G1CollectorPolicy::finalize_cset(double target_pause_time_ms, EvacuationInfo& evacuation_info) {
  double young_start_time_sec = os::elapsedTime();

  YoungList* young_list = _g1->young_list();
  finalize_incremental_cset_building();

  guarantee(target_pause_time_ms > 0.0,
            err_msg("target_pause_time_ms = %1.6lf should be positive",
                    target_pause_time_ms));
  guarantee(_collection_set == NULL, "Precondition");

  double base_time_ms = predict_base_elapsed_time_ms(_pending_cards);
  double predicted_pause_time_ms = base_time_ms;
  double time_remaining_ms = MAX2(target_pause_time_ms - base_time_ms, 0.0);

  _last_gc_was_young = gcs_are_young() ? true : false;

  if (_last_gc_was_young) {
    _trace_gen0_time_data.increment_young_collection_count();
  } else {
    _trace_gen0_time_data.increment_mixed_collection_count();
  }

  uint survivor_region_length = young_list->survivor_length();
  uint eden_region_length = young_list->length() - survivor_region_length;
  init_cset_region_lengths(eden_region_length, survivor_region_length);

  HeapRegion* hr = young_list->first_survivor_region();
  while (hr != NULL) {
    assert(hr->is_survivor(), "badly formed young list");
    hr->set_eden_pre_gc();
    hr = hr->get_next_young_region();
  }

  young_list->clear_survivors();

  _collection_set = _inc_cset_head;
  _collection_set_bytes_used_before = _inc_cset_bytes_used_before;
  time_remaining_ms = MAX2(time_remaining_ms - _inc_cset_predicted_elapsed_time_ms, 0.0);
  predicted_pause_time_ms += _inc_cset_predicted_elapsed_time_ms;

  set_recorded_rs_lengths(_inc_cset_recorded_rs_lengths);

  double young_end_time_sec = os::elapsedTime();
  phase_times()->record_young_cset_choice_time_ms((young_end_time_sec - young_start_time_sec) * 1000.0);

  double non_young_start_time_sec = young_end_time_sec;
  // 判断是否满足启动 Mixed GC 的两个前提条件：
  // 1. 并发标记已经结束，并更新好了 CSet Chooser
  // 2. Young GC 结束
  if (!gcs_are_young()) {
    // 启动Mixed GC
    CollectionSetChooser* cset_chooser = _collectionSetChooser;
    cset_chooser->verify();
    // 最小收集数，计算CSet中最少要放几个老年代region
    const uint min_old_cset_length = calc_min_old_cset_length();
    // 最大收集数，计算CSet中最多能放几个老年代region
    const uint max_old_cset_length = calc_max_old_cset_length();

    uint expensive_region_num = 0;
    bool check_time_remaining = adaptive_young_list_length();
    // 把老年代region添加到CSet
    HeapRegion* hr = cset_chooser->peek();
    while (hr != NULL) {
      if (old_cset_region_length() >= max_old_cset_length) {
        // 老年代处理数达到最大值，停止添加到CSet
        break;
      }

      size_t reclaimable_bytes = cset_chooser->remaining_reclaimable_bytes();
      double reclaimable_perc = reclaimable_bytes_perc(reclaimable_bytes);
      double threshold = (double) G1HeapWastePercent;
      if (reclaimable_perc <= threshold) {
        // 可回收的空间比例低于G1HeapWastePercent，停止添加到CSet
        break;
      }

      double predicted_time_ms = predict_region_elapsed_time_ms(hr, gcs_are_young());
      if (check_time_remaining) {
        // 新生代region个数可以动态调整
        if (predicted_time_ms > time_remaining_ms) {
          // 预测时间已经超过了目标暂停时间
          if (old_cset_region_length() >= min_old_cset_length) {
            // 已经向CSet中添加了min_old_cset_length个老年代region，
            // 停止添加到CSet
            break;
          }

          // 还没达到最小收集数，但是已经超过了预测时间
          // 记录下来，还差多少个region没有达到最小收集数
          expensive_region_num += 1;
        }
      } else {
        // 新生代region个数不能动态调整
        if (old_cset_region_length() >= min_old_cset_length) {

          break;
        }
      }

      time_remaining_ms = MAX2(time_remaining_ms - predicted_time_ms, 0.0);
      predicted_pause_time_ms += predicted_time_ms;
      cset_chooser->remove_and_move_to_next(hr);
      _g1->old_set_remove(hr);
      // 把老年代region添加到CSet
      add_old_region_to_cset(hr);

      hr = cset_chooser->peek();
    }

    cset_chooser->verify();
  }

  stop_incremental_cset_building();

  double non_young_end_time_sec = os::elapsedTime();
  phase_times()->record_non_young_cset_choice_time_ms((non_young_end_time_sec - non_young_start_time_sec) * 1000.0);
  evacuation_info.set_collectionset_regions(cset_region_length());
}

/**
 * 计算最小收集数
 */
uint G1CollectorPolicy::calc_min_old_cset_length() {
  // 计算最小收集数的时候用到了参数G1MixedGCCountTarget（默认值为8），
  // 这个参数越大，要收集的老年代region越少，反之收集的region越多。
  // 老年代region在CSet中的比例要超过1/G1MixedGCCountTarget，
  // 如果没有超过这个值，即使预测时间超过了目标时间，仍然会添加region，
  // 如果预测时间超过了目标时间，到达最小值之后就不会继续添加
  const size_t region_num = (size_t) _collectionSetChooser->length();
  const size_t gc_num = (size_t) MAX2(G1MixedGCCountTarget, (uintx) 1);
  size_t result = region_num / gc_num;
  // 向上取整，至少要回收一个老年代region
  if (result * gc_num < region_num) {
    result += 1;
  }
  return (uint) result;
}

/**
 * 计算最大收集数
 */
uint G1CollectorPolicy::calc_max_old_cset_length() {
  // G1OldCSetRegionThresholdPercent参数默认值是10，
  // 即一次最多收集10%的region
  G1CollectedHeap* g1h = G1CollectedHeap::heap();
  const size_t region_num = g1h->num_regions();
  const size_t perc = (size_t) G1OldCSetRegionThresholdPercent;
  size_t result = region_num * perc / 100;
  // 向上取整
  if (100 * result < region_num * perc) {
    result += 1;
  }
  return (uint) result;
}
```
