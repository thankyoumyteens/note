# 扩大新生代

在Young GC的收尾阶段, 会判断是否需要扩大新生代。

参数GCTimeRatio用于判断是否需要扩大新生代, 默认9。 

```cpp
/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

void G1CollectedHeap::expand_heap_after_young_collection(){
  size_t expand_bytes = _heap_sizing_policy->young_collection_expansion_amount();
  // expand_bytes大于0表示需要扩容
  if (expand_bytes > 0) {
    double expand_ms = 0.0;
    // 扩容
    if (!expand(expand_bytes, _workers, &expand_ms)) {
      // 扩容失败
    }
    // 记录扩容花费的时间
    phase_times()->record_expand_heap_time(expand_ms);
  }
}

////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1HeapSizingPolicy.cpp //
////////////////////////////////////////////////////////////////////

/**
 * 计算新生代可以扩容的大小
 */
size_t G1HeapSizingPolicy::young_collection_expansion_amount() {
  assert(GCTimeRatio > 0, "must be");
  // TODO
  double long_term_pause_time_ratio = _analytics->long_term_pause_time_ratio();
  double short_term_pause_time_ratio = _analytics->short_term_pause_time_ratio();
  // GCTimeRatio控制GC执行时间和应用程序执行时间的比例, 默认为GCTimeRatio
  // 默认情况下, GC执行时间 : 应用程序执行时间 = 1 : 10
  const double pause_time_threshold = 1.0 / (1.0 + GCTimeRatio);
  // 根据堆的剩余空间调整这个比例
  double threshold = scale_with_heap(pause_time_threshold);

  size_t expand_bytes = 0;

  if (_g1h->capacity() == _g1h->max_capacity()) {
    // 堆空间达到最大容量, 无法扩大
    log_expansion(short_term_pause_time_ratio, long_term_pause_time_ratio,
                  threshold, pause_time_threshold, true, 0);
    clear_ratio_check_data();
    return expand_bytes;
  }

  // If the last GC time ratio is over the threshold, increment the count of
  // times it has been exceeded, and add this ratio to the sum of exceeded
  // ratios.
  if (short_term_pause_time_ratio > threshold) {
    _ratio_over_threshold_count++;
    _ratio_over_threshold_sum += short_term_pause_time_ratio;
  }

  log_trace(gc, ergo, heap)("Heap expansion triggers: pauses since start: %u "
                            "num prev pauses for heuristics: %u "
                            "ratio over threshold count: %u",
                            _pauses_since_start,
                            _num_prev_pauses_for_heuristics,
                            _ratio_over_threshold_count);

  // Check if we've had enough GC time ratio checks that were over the
  // threshold to trigger an expansion. We'll also expand if we've
  // reached the end of the history buffer and the average of all entries
  // is still over the threshold. This indicates a smaller number of GCs were
  // long enough to make the average exceed the threshold.
  bool filled_history_buffer = _pauses_since_start == _num_prev_pauses_for_heuristics;
  if ((_ratio_over_threshold_count == MinOverThresholdForGrowth) ||
      (filled_history_buffer && (long_term_pause_time_ratio > threshold))) {
    size_t min_expand_bytes = HeapRegion::GrainBytes;
    size_t reserved_bytes = _g1h->max_capacity();
    size_t committed_bytes = _g1h->capacity();
    size_t uncommitted_bytes = reserved_bytes - committed_bytes;
    size_t expand_bytes_via_pct =
      uncommitted_bytes * G1ExpandByPercentOfAvailable / 100;
    double scale_factor = 1.0;

    // If the current size is less than 1/4 of the Initial heap size, expand
    // by half of the delta between the current and Initial sizes. IE, grow
    // back quickly.
    //
    // Otherwise, take the current size, or G1ExpandByPercentOfAvailable % of
    // the available expansion space, whichever is smaller, as the base
    // expansion size. Then possibly scale this size according to how much the
    // threshold has (on average) been exceeded by. If the delta is small
    // (less than the StartScaleDownAt value), scale the size down linearly, but
    // not by less than MinScaleDownFactor. If the delta is large (greater than
    // the StartScaleUpAt value), scale up, but adding no more than MaxScaleUpFactor
    // times the base size. The scaling will be linear in the range from
    // StartScaleUpAt to (StartScaleUpAt + ScaleUpRange). In other words,
    // ScaleUpRange sets the rate of scaling up.
    if (committed_bytes < InitialHeapSize / 4) {
      expand_bytes = (InitialHeapSize - committed_bytes) / 2;
    } else {
      double const MinScaleDownFactor = 0.2;
      double const MaxScaleUpFactor = 2;
      double const StartScaleDownAt = pause_time_threshold;
      double const StartScaleUpAt = pause_time_threshold * 1.5;
      double const ScaleUpRange = pause_time_threshold * 2.0;

      double ratio_delta;
      if (filled_history_buffer) {
        ratio_delta = long_term_pause_time_ratio - threshold;
      } else {
        ratio_delta = (_ratio_over_threshold_sum / _ratio_over_threshold_count) - threshold;
      }

      expand_bytes = MIN2(expand_bytes_via_pct, committed_bytes);
      if (ratio_delta < StartScaleDownAt) {
        scale_factor = ratio_delta / StartScaleDownAt;
        scale_factor = MAX2(scale_factor, MinScaleDownFactor);
      } else if (ratio_delta > StartScaleUpAt) {
        scale_factor = 1 + ((ratio_delta - StartScaleUpAt) / ScaleUpRange);
        scale_factor = MIN2(scale_factor, MaxScaleUpFactor);
      }
    }

    expand_bytes = static_cast<size_t>(expand_bytes * scale_factor);

    // Ensure the expansion size is at least the minimum growth amount
    // and at most the remaining uncommitted byte size.
    expand_bytes = clamp(expand_bytes, min_expand_bytes, uncommitted_bytes);

    clear_ratio_check_data();
  } else {
    // An expansion was not triggered. If we've started counting, increment
    // the number of checks we've made in the current window.  If we've
    // reached the end of the window without resizing, clear the counters to
    // start again the next time we see a ratio above the threshold.
    if (_ratio_over_threshold_count > 0) {
      _pauses_since_start++;
      if (_pauses_since_start > _num_prev_pauses_for_heuristics) {
        clear_ratio_check_data();
      }
    }
  }

  log_expansion(short_term_pause_time_ratio, long_term_pause_time_ratio,
                threshold, pause_time_threshold, false, expand_bytes);

  return expand_bytes;
}

double G1HeapSizingPolicy::scale_with_heap(double pause_time_threshold) {
  double threshold = pause_time_threshold;
  // If the heap is at less than half its maximum size, scale the threshold down,
  // to a limit of 1%. Thus the smaller the heap is, the more likely it is to expand,
  // though the scaling code will likely keep the increase small.
  if (_g1h->capacity() <= _g1h->max_capacity() / 2) {
    threshold *= (double)_g1h->capacity() / (double)(_g1h->max_capacity() / 2);
    threshold = MAX2(threshold, 0.01);
  }

  return threshold;
}
```
