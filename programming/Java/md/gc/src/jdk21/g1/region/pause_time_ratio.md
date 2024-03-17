# 计算 pause_time_ratio

判断新生代是否需要扩容时, 需要用到 short_term_pause_time_ratio 和 long_term_pause_time_ratio, 这两个值是在每次 GC 结束后计算的。G1Analytics 中维护了两个长度为 10 的队列, 分别记录每一次 GC 暂停的时间和每一次 GC 结束的时间。

1. 计算 short_term_pause_time_ratio: pause_time_ms ÷ short_interval_ms
2. 计算 long_term_pause_time_ratio: (\_recent_gc_times_ms.sum() - \_recent_gc_times_ms.oldest() + pause_time_ms) ÷ long_interval_ms

![](../../../img/compute_pause_time_ratios.png)

```cpp
//////////////////////////////////////////
// src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////

/**
 * GC结束后会记录相关的时间
 */
void G1Policy::record_pause(G1GCPauseType gc_type,
                            double start,
                            double end,
                            bool evacuation_failure) {
  // 记录到MMU的历史数据中
  if (gc_type != G1GCPauseType::FullGC) {
    _mmu_tracker->add_pause(start, end);
  }

  if (!evacuation_failure) {
    // 计算 pause_time_ratio
    update_gc_pause_time_ratios(gc_type, start, end);
  }

  update_time_to_mixed_tracking(gc_type, start, end);
}

void G1Policy::update_gc_pause_time_ratios(G1GCPauseType gc_type, double start_time_sec, double end_time_sec) {
  // GC暂停的时间
  double pause_time_sec = end_time_sec - start_time_sec;
  double pause_time_ms = pause_time_sec * 1000.0;
  // 记录GC暂停时间占程序执行总时间的比例
  _analytics->compute_pause_time_ratios(end_time_sec, pause_time_ms);
  // 把本次GC暂停的时间和GC结束的时间存入队列
  _analytics->update_recent_gc_times(end_time_sec, pause_time_ms);

  if (gc_type == G1GCPauseType::Cleanup || gc_type == G1GCPauseType::Remark) {
    _analytics->append_prev_collection_pause_end_ms(pause_time_ms);
  } else {
    _analytics->set_prev_collection_pause_end_ms(end_time_sec * 1000.0);
  }
}

/////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1Analytics.cpp //
/////////////////////////////////////////////

/**
 * 记录GC暂停时间占程序执行总时间的比例
 */
void G1Analytics::compute_pause_time_ratios(double end_time_sec, double pause_time_ms) {
  // 最近n次GC中, 程序总的运行时间
  double long_interval_ms = (end_time_sec - oldest_known_gc_end_time_sec()) * 1000.0;
  // 最近n次GC中, GC的暂停时间
  double gc_pause_time_ms = _recent_gc_times_ms.sum() - _recent_gc_times_ms.oldest() + pause_time_ms;
  // 最近n次GC暂停时间的比例
  _long_term_pause_time_ratio = gc_pause_time_ms / long_interval_ms;
  _long_term_pause_time_ratio = clamp(_long_term_pause_time_ratio, 0.0, 1.0);

  // 本次GC, 程序总的运行时间
  double short_interval_ms = (end_time_sec - most_recent_gc_end_time_sec()) * 1000.0;
  // 本次GC暂停时间的比例
  _short_term_pause_time_ratio = pause_time_ms / short_interval_ms;
  _short_term_pause_time_ratio = clamp(_short_term_pause_time_ratio, 0.0, 1.0);
}

/**
 * 取出最早的一次GC结束的时间
 */
double G1Analytics::oldest_known_gc_end_time_sec() const {
  return _recent_prev_end_times_for_all_gcs_sec.oldest();
}

/**
 * 取出最近一次GC结束的时间
 */
double G1Analytics::most_recent_gc_end_time_sec() const {
  return _recent_prev_end_times_for_all_gcs_sec.last();
}

/**
 * 把本次GC暂停的时间和GC结束的时间存入队列
 */
void G1Analytics::update_recent_gc_times(double end_time_sec,
                                         double pause_time_ms) {
  // 队列, 默认长度10, 用于记录每一次GC暂停的时间
  _recent_gc_times_ms.add(pause_time_ms);
  // 队列, 默认长度10, 用于记录每一次GC结束的时间
  _recent_prev_end_times_for_all_gcs_sec.add(end_time_sec);
}
```

## 队列添加元素

TruncatedSeq 在队列满了的时候, 如果还有新元素入队, 会把最早的元素移出队列。TruncatedSeq 的实现方式:

1. TruncatedSeq 使用数组实现, 假设队列长度为 5, 在队列为空的时候 next 指向索引 0
   ```
   [0, 0, 0, 0, 0]
    ^
    |
   _next
   ```
2. 队列中添加一个元素后, next 会后移一位, next 会始终指向新元素添加的位置(最老的元素)
   ```
   [100, 0, 0, 0, 0]
         ^
         |
       _next
   ```
3. 当入队第 5 个元素, 导致队列满后, next 会重新指向索引 0, 此时索引 0 的元素是最早入队的
   ```
   [100, 101, 102, 103, 104]
     ^
     |
   _next
   ```
4. 继续向队列添加元素时, 索引为 0 的元素会被新元素替换掉
   ```
   [105, 101, 102, 103, 104]
          ^
          |
        _next
   ```

```cpp
///////////////////////////////////////////////
// src/hotspot/share/utilities/numberSeq.cpp //
///////////////////////////////////////////////

/**
 * 队列中的元素全部初始化为0
 */
TruncatedSeq::TruncatedSeq(int length, double alpha):
  AbsSeq(alpha), _length(length), _next(0) {
  _sequence = NEW_C_HEAP_ARRAY(double, _length, mtInternal);
  for (int i = 0; i < _length; ++i)
    _sequence[i] = 0.0;
}

/**
 * 添加元素
 */
void TruncatedSeq::add(double val) {
  AbsSeq::add(val);

  // 取出最老的元素, 删除这个元素
  double old_val = _sequence[_next];

  _sum -= old_val;
  _sum_of_squares -= old_val * old_val;

  _sum += val;
  _sum_of_squares += val * val;

  // 用新元素替换旧元素
  _sequence[_next] = val;

  // _next是新元素要插入数组位置的索引, 达到数组的长度后会从0重新开始
  // 旧_next为0时, 新_next = (0 + 1) % 10 = 1
  // 旧_next为1时, 新_next = (1 + 1) % 10 = 2
  // ...
  // 旧_next为9时, 新_next = (9 + 1) % 10 = 0
  // ...
  _next = (_next + 1) % _length;

  // _num记录数组中实际有多少元素
  if (_num < _length)
    ++_num;

  guarantee( variance() > -1.0, "variance should be >= 0" );
}
```
