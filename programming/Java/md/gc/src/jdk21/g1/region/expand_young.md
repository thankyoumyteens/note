# 扩大新生代

在 Young GC 的收尾阶段, 会判断是否需要扩大新生代。

```cpp
/////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

void G1CollectedHeap::expand_heap_after_young_collection(){
  // 计算新生代可以扩容的大小
  size_t expand_bytes = _heap_sizing_policy->young_collection_expansion_amount();
  // expand_bytes大于0表示需要扩容
  if (expand_bytes > 0) {
    // 扩容花费的时间
    double expand_ms = 0.0;
    // 扩容
    if (!expand(expand_bytes, _workers, &expand_ms)) {
      // 扩容失败
    }
    // 记录扩容花费的时间
    phase_times()->record_expand_heap_time(expand_ms);
  }
}
```

## 计算新生代可以扩容的大小

G1 使用 JVM 参数 -XX:GCTimeRatio 来控制 GC 暂停时间和程序执行时间的比例, GCTimeRatio 默认为 9, 二者的比例的计算方法为: `1 : 1 + GCTimeRatio`, 所以 GC 暂停时间和程序执行时间的比例默认为 1 : 10, 即默认情况下 GC 暂停时间不应该超过程序运行时间的 1/10。

G1 在判断是否需要扩容的过程中会用到两个值:

1. short_term_pause_time_ratio: 最新一次 Young GC 暂停时间占程序执行总时间的比例
   - 最新一次 Young GC 暂停时间: 本次 Young GC 开始到结束的时间段
   - 程序执行总时间: 以上一次 Young GC 结束的时间点为起点, 本次 Young GC 结束的时间点为终点的时间段
2. long_term_pause_time_ratio: 历史 Young GC 暂停时间占程序执行总时间的比例
   - 历史 Young GC 暂停时间: 前 n 次 Young GC 暂停时间的总和
   - 程序执行总时间: 以 n 次之前的 Young GC 结束的时间点为起点, 本次 Young GC 结束的时间点为终点的时间段

判断是否需要扩容的过程:

1.

```java
////////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1HeapSizingPolicy.cpp //
////////////////////////////////////////////////////////////////////

/**
 * 计算新生代可以扩容的大小
 */
size_t G1HeapSizingPolicy::young_collection_expansion_amount() {
  assert(GCTimeRatio > 0, "must be");
  // GC暂停时间占程序执行总时间的比例
  double long_term_pause_time_ratio = _analytics->long_term_pause_time_ratio();
  // 上一次GC暂停时间占程序执行总时间的比例
  double short_term_pause_time_ratio = _analytics->short_term_pause_time_ratio();
  // GCTimeRatio用于控制GC暂停时间占程序执行总时间比例的阈值, 默认为9
  // 默认情况下, GC暂停时间 : GC暂停时间+mutator执行时间 = 1 : 10
  const double pause_time_threshold = 1.0 / (1.0 + GCTimeRatio);
  // 根据堆的剩余空间调整这个阈值
  double threshold = scale_with_heap(pause_time_threshold);

  // 要扩容的大小
  size_t expand_bytes = 0;

  if (_g1h->capacity() == _g1h->max_capacity()) {
    // 堆空间达到最大容量, 无法扩大
    log_expansion(short_term_pause_time_ratio, long_term_pause_time_ratio,
                  threshold, pause_time_threshold, true, 0);
    clear_ratio_check_data();
    return expand_bytes;
  }

  // 最新一次GC暂停时间比例超过阈值
  if (short_term_pause_time_ratio > threshold) {
    // 超过阈值的次数
    _ratio_over_threshold_count++;
    // 超过阈值的累计比例
    _ratio_over_threshold_sum += short_term_pause_time_ratio;
  }

  log_trace(gc, ergo, heap)("Heap expansion triggers: pauses since start: %u "
                            "num prev pauses for heuristics: %u "
                            "ratio over threshold count: %u",
                            _pauses_since_start,
                            _num_prev_pauses_for_heuristics,
                            _ratio_over_threshold_count);

  // Check if we've had enough GC time ratio checks that were over the
  // threshold to trigger an expansion.
  // We'll also expand if we've
  // reached the end of the history buffer and the average of all entries
  // is still over the threshold. This indicates a smaller number of GCs were
  // long enough to make the average exceed the threshold.
  bool filled_history_buffer = _pauses_since_start == _num_prev_pauses_for_heuristics;
  // 判断是否需要扩容
  //   MinOverThresholdForGrowth固定为4, GC暂停时间超过阈值的次数达到4时, 需要扩容
  //
  if ((_ratio_over_threshold_count == MinOverThresholdForGrowth) ||
      (filled_history_buffer && (long_term_pause_time_ratio > threshold))) {
    // GrainBytes在初始化region大小的时候被设置
    // GrainBytes = region_size;
    // 最小也要扩容一个region的大小
    size_t min_expand_bytes = HeapRegion::GrainBytes;
    // 堆的总大小
    size_t reserved_bytes = _g1h->max_capacity();
    // 已分配成region的堆大小
    size_t committed_bytes = _g1h->capacity();
    // 未分配的堆大小
    size_t uncommitted_bytes = reserved_bytes - committed_bytes;
    // G1ExpandByPercentOfAvailable控制每次扩容多大, 默认20
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

    // InitialHeapSize: 初始堆内存大小, 等价于-Xms, 默认为0
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

    // 把expand_bytes的值控制在min_expand_bytes和uncommitted_bytes之间
    expand_bytes = clamp(expand_bytes, min_expand_bytes, uncommitted_bytes);
    // 清除本次扩容修改的变量
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
  // 如果当前使用的堆空间已经不足最大可用的堆空间大小的一半，则将阈值调小, 不过最小不低于1%
  if (_g1h->capacity() <= _g1h->max_capacity() / 2) {
    threshold *= (double)_g1h->capacity() / (double)(_g1h->max_capacity() / 2);
    threshold = MAX2(threshold, 0.01);
  }

  return threshold;
}

void G1HeapSizingPolicy::clear_ratio_check_data() {
  _ratio_over_threshold_count = 0;
  _ratio_over_threshold_sum = 0.0;
  _pauses_since_start = 0;
}
```
