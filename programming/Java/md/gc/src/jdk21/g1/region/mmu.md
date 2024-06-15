# MMU

<!-- TODO GC时的MMU -->

MMU(Minimum Mutator Utilization): 在一段时间(\_time_slice)内 mutator 运行时间的最小百分比。例如, 设定 MMU 为 95%, 表示在一个指定的时间段内, mutator 最多只能被停顿 5% 的时间。

```cpp
// --- src/hotspot/share/gc/g1/g1Policy.cpp --- //

/**
 * 根据mmu计算期望的eden region数
 */
uint G1Policy::calculate_desired_eden_length_by_mmu() const {
  assert(use_adaptive_young_list_length(), "precondition");
  double now_sec = os::elapsedTime();
  double when_ms = _mmu_tracker->when_max_gc_sec(now_sec) * 1000.0;
  double alloc_rate_ms = _analytics->predict_alloc_rate_ms();
  return (uint) ceil(alloc_rate_ms * when_ms);
}

// --- src/hotspot/share/gc/g1/g1MMUTracker.hpp --- //

class G1MMUTracker: public CHeapObj<mtGC> {
  double when_max_gc_sec(double current_time) {
    return when_sec(current_time, max_gc_time());
  }
};

// --- src/hotspot/share/gc/g1/g1MMUTracker.cpp --- //

/**
 * 在堆空间初始化阶段, 由于没有历史GC暂停时间, 这个函数会直接返回0
 *
 * current_timestamp: 传入当前时间的时间戳
 * pause_time: 堆空间初始化时, 会传入max_gc_time()
 *             在并发标记阶段, 会传入其它值
 */
double G1MMUTracker::when_sec(double current_timestamp, double pause_time) {
  assert(pause_time > 0.0, "precondition");

  // max_gc_time(): -XX:MaxGCPauseMillis, 最大GC暂停时间
  // If the pause is over the maximum, just assume that it's the maximum.
  pause_time = MIN2(pause_time, max_gc_time());

  double gc_budget = max_gc_time() - pause_time;

  double limit = current_timestamp + pause_time - _time_slice;
  // 从最新一条记录开始向老记录遍历
  // _array: 记录历史的GC暂停时间
  // _no_entries: _array中的元素个数
  for (int i = 0; i < _no_entries; ++i) {
    int index = trim_index(_head_index - i);
    G1MMUTrackerElem *elem = &_array[index];
    // 比_time_slice的时间段还要早, 不再继续遍历
    if (elem->end_time() <= limit) {
      break;
    }

    // GC暂停时间(不超过_time_slice时间段)
    double duration = (elem->end_time() - MAX2(elem->start_time(), limit));
    // This duration would exceed (strictly greater than) the budget.
    if (duration > gc_budget) {
      // This timestamp captures the instant the budget is balanced (or used up).
      double balance_timestamp = elem->end_time() - gc_budget;
      assert(balance_timestamp >= limit, "inv");
      return balance_timestamp - limit;
    }

    gc_budget -= duration;
  }

  // Not enough gc time spent inside the window, we have a budget surplus.
  return 0;
}
```
