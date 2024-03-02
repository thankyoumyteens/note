# 设置新生代 region 数量

G1 首先会预测出下一次 GC 会用到的卡表和 rset 的大小, 然后根据这两个值以及前面计算的预期范围预测出新生代的大小。再根据这个预测的新生代大小确定新生代的实际大小, 最后根据实际大小计算出新生代的最大值。

```cpp
//////////////////////////////////////////
// src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////

void G1Policy::update_young_length_bounds() {
  assert(!Universe::is_fully_initialized() || SafepointSynchronize::is_at_safepoint(), "must be");
  bool for_young_only_phase = collector_state()->in_young_only_phase();
  // pending_cards: DCQ Set中用到的card数量
  // rs_length: rset大小
  update_young_length_bounds(_analytics->predict_pending_cards(for_young_only_phase),
                             _analytics->predict_rs_length(for_young_only_phase));
}

void G1Policy::update_young_length_bounds(size_t pending_cards, size_t rs_length) {
  // 当前新生代region数量
  // return Atomic::load(&_young_list_target_length);
  uint old_young_list_target_length = young_list_target_length();

  // 预测新生代预期region数量
  uint new_young_list_desired_length = calculate_young_desired_length(pending_cards, rs_length);
  // 计算新生代实际region数量
  uint new_young_list_target_length = calculate_young_target_length(new_young_list_desired_length);
  // 计算新生代最大region数量
  uint new_young_list_max_length = calculate_young_max_length(new_young_list_target_length);

  log_trace(gc, ergo, heap)("Young list length update: pending cards %zu rs_length %zu old target %u desired: %u target: %u max: %u",
                            pending_cards,
                            rs_length,
                            old_young_list_target_length,
                            new_young_list_desired_length,
                            new_young_list_target_length,
                            new_young_list_max_length);

  // 设置新生代预期region数量
  Atomic::store(&_young_list_desired_length, new_young_list_desired_length);
  // 设置新生代实际region数量
  Atomic::store(&_young_list_target_length, new_young_list_target_length);
  // 设置新生代最大region数量
  Atomic::store(&_young_list_max_length, new_young_list_max_length);
}
```

## 预测新生代 region 的数量

<!-- TODO MMU 基准时间 -->

预测新生代 region 数量的方法:

1. 首先确定新生代的最小值, 方法是找出下面 3 个数量的最大值:
   - G1YoungGenSizer 计算出的新生代期望最小值
   - survivor region 数 + 1, 因为至少要有一个 eden region 用来分配对象
   - 当前新生代 region 数(垃圾回收之后的)
2. 确定新生代的最大值, 方法是找出下面 2 个数量的最大值:
   - G1YoungGenSizer 计算出的新生代期望最大值
   - 第 1 步算出的新生代的最小值
3. 根据 mmu 计算期望的 eden region 数, 根据基准时间计算期望的 eden region 数, 取两者的最大值, 作为 eden region 数量。加上 survivor region 数量, 作为新生代 region 数量
4. 确保新生代 region 数量在第 1 步和第 2 步算出的范围内

```cpp
//////////////////////////////////////////
// src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////

uint G1Policy::calculate_young_desired_length(size_t pending_cards, size_t rs_length) const {
  // 取出新生代的预期范围
  // return _min_desired_young_length;
  uint min_young_length_by_sizer = _young_gen_sizer.min_desired_young_length();
  // return _max_desired_young_length;
  uint max_young_length_by_sizer = _young_gen_sizer.max_desired_young_length();

  assert(min_young_length_by_sizer >= 1, "invariant");
  assert(max_young_length_by_sizer >= min_young_length_by_sizer, "invariant");

  // 堆中当前的survivor region个数
  // return _survivor.length();
  const uint survivor_length = _g1h->survivor_regions_count();
  // 堆中当前的新生代region个数
  // return _eden.length() + _survivor.length();
  const uint allocated_young_length = _g1h->young_regions_count();

  // 新生代region数的下边界
  // survivor_length + 1 表示至少需要有一个 eden region
  uint absolute_min_young_length = MAX3(min_young_length_by_sizer,
                                        survivor_length + 1,
                                        allocated_young_length);
  // 新生代region数的上边界
  uint absolute_max_young_length = MAX2(max_young_length_by_sizer, absolute_min_young_length);

  // 根据mmu预测eden的大小
  //
  // MMU, 全称为Minimum Mutator Utilization,
  // 是描述在一段时间内应用程序能够运行的最小百分比
  // 例如, 设定MMU为95%, 表示在一个指定的时间段内,
  // mutator最多只能被停顿5%的时间
  uint desired_eden_length_by_mmu = 0;
  uint desired_eden_length_by_pause = 0;

  uint desired_young_length = 0;
  // 是否使用自适应的新生代大小
  if (use_adaptive_young_list_length()) {
    // 根据mmu计算期望的eden region数
    desired_eden_length_by_mmu = calculate_desired_eden_length_by_mmu();
    // 预测基准时间
    // 包括: 处理rset的时间, 处理整个新生代的的固定花费的时间,
    //      处理refinement缓存的时间, 把对象复制到survovor的时间
    //      基本上包含除了复制eden region之外的所有时间
    double base_time_ms = predict_base_time_ms(pending_cards, rs_length);

    // 根据基准时间计算期望的eden region数
    desired_eden_length_by_pause =
      calculate_desired_eden_length_by_pause(base_time_ms,
                                             absolute_min_young_length - survivor_length,
                                             absolute_max_young_length - survivor_length);
    // 取两者的最大值
    uint desired_eden_length = MAX2(desired_eden_length_by_pause,
                                    desired_eden_length_by_mmu);

    desired_young_length = desired_eden_length + survivor_length;
  } else {
    // 新生代大小固定
    desired_young_length = min_young_length_by_sizer;
  }
  // 确保desired_young_length在[absolute_min_young_length, absolute_max_young_length]范围内
  desired_young_length = clamp(desired_young_length, absolute_min_young_length, absolute_max_young_length);

  log_trace(gc, ergo, heap)("Young desired length %u "
                            "survivor length %u "
                            "allocated young length %u "
                            "absolute min young length %u "
                            "absolute max young length %u "
                            "desired eden length by mmu %u "
                            "desired eden length by pause %u ",
                            desired_young_length, survivor_length,
                            allocated_young_length, absolute_min_young_length,
                            absolute_max_young_length, desired_eden_length_by_mmu,
                            desired_eden_length_by_pause);

  assert(desired_young_length >= allocated_young_length, "must be");
  return desired_young_length;
}
```

## 确定新生代实际 region 数量

G1 默认会保留 10% 的空闲 region, 确定新生代的实际 region 数量分为 3 种情况:

1. 当前空闲的 region 数量已经不足 10%, G1 会把本来要保留的一部分 region 分配给新生代, 这样一来, 保留的 region 数量会低于 10%, 可能会导致 to-space exhausted
2. 当前空闲的 region 数量超过 10%, 但保留 10% 的 region 后, 剩余的 region 无法达到新生代的预期大小。所以也需要使用一部分本来要保留的 region, 保留 region 也会低于 10%
3. 当前空闲的 region 数量充足, 足够满足预期的新生代 region 数量分配, G1 也可以保留 10% 的空闲 region

```cpp
//////////////////////////////////////////
// src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////

uint G1Policy::calculate_young_target_length(uint desired_young_length) const {
  // 堆中已经有的新生代region个数
  // return _eden.length() + _survivor.length();
  uint allocated_young_length = _g1h->young_regions_count();

  // 要新增的eden region个数
  uint receiving_additional_eden;

  if (allocated_young_length >= desired_young_length) {
    // 当前的新生代region数已经超过了预期, 不再增加region
    receiving_additional_eden = 0;
    log_trace(gc, ergo, heap)("Young target length: Already used up desired young %u allocated %u",
                              desired_young_length,
                              allocated_young_length);
  } else {
    // 先计算调整后的新生代region数量receiving_young,
    // 然后用receiving_young减去堆中已经有的新生代region个数allocated_young_length,
    // 就得到了要新增的eden region个数receiving_additional_eden
    //
    // receiving_young要在尽量满足desired_young_length的同时, 尽可能少的使用保留region

    // max_to_eat_into_reserve: 最多能使用多少个要保留的region
    //
    // _reserve_regions: 要保留的region个数, 堆空间初始化时设置,
    //                   取值是堆中region个数的10%
    uint max_to_eat_into_reserve = MIN2(_young_gen_sizer.min_desired_young_length(),
                                        (_reserve_regions + 1) / 2);

    log_trace(gc, ergo, heap)("Young target length: Common "
                              "free regions at end of collection %u "
                              "desired young length %u "
                              "reserve region %u "
                              "max to eat into reserve %u",
                              _free_regions_at_end_of_collection,
                              desired_young_length,
                              _reserve_regions,
                              max_to_eat_into_reserve);

    if (_free_regions_at_end_of_collection <= _reserve_regions) {
      // 当前空闲的 region 数量已经不足 10%,
      // 全部使用保留的region

      // 调整后的新生代region数量, 尽量满足desired_young_length
      uint receiving_young = MIN3(_free_regions_at_end_of_collection,
                                  desired_young_length,
                                  max_to_eat_into_reserve);

      // 如果当前的新生代region数已经超过了计算出来的数量, 则不再增加region
      receiving_additional_eden = allocated_young_length < receiving_young ?
                                  receiving_young - allocated_young_length : 0;

      log_trace(gc, ergo, heap)("Young target length: Fully eat into reserve "
                                "receiving young %u receiving additional eden %u",
                                receiving_young,
                                receiving_additional_eden);
    } else if (_free_regions_at_end_of_collection < (desired_young_length + _reserve_regions)) {
      // 当前空闲的 region 数量超过 10%, 但还是小于预测的新生代 region 数量 + 10%的空闲 region,
      // 使用一部分保留的region

      // 去掉要保留的10%后, 剩余可用的空闲region个数
      uint free_outside_reserve = _free_regions_at_end_of_collection - _reserve_regions;
      assert(free_outside_reserve < desired_young_length,
             "must be %u %u",
             free_outside_reserve, desired_young_length);
      // 要使用的保留region个数
      uint receiving_within_reserve = MIN2(desired_young_length - free_outside_reserve,
                                           max_to_eat_into_reserve);
      // 调整后的新生代region数量, 尽量满足desired_young_length
      uint receiving_young = free_outside_reserve + receiving_within_reserve;
      // 如果当前的新生代region数已经超过了计算出来的调整后的数量, 则不再增加region
      receiving_additional_eden = allocated_young_length < receiving_young ?
                                  receiving_young - allocated_young_length : 0;

      log_trace(gc, ergo, heap)("Young target length: Partially eat into reserve "
                                "free outside reserve %u "
                                "receiving within reserve %u "
                                "receiving young %u "
                                "receiving additional eden %u",
                                free_outside_reserve, receiving_within_reserve,
                                receiving_young, receiving_additional_eden);
    } else {
      // 当前空闲的 region 数量充足,
      // 不使用保留的region
      receiving_additional_eden = desired_young_length - allocated_young_length;
      log_trace(gc, ergo, heap)("Young target length: No need to use reserve "
                                "receiving additional eden %u",
                                receiving_additional_eden);
    }
  }

  uint target_young_length = allocated_young_length + receiving_additional_eden;

  assert(target_young_length >= allocated_young_length, "must be");

  log_trace(gc, ergo, heap)("Young target length: "
                            "young target length %u "
                            "allocated young length %u "
                            "received additional eden %u",
                            target_young_length, allocated_young_length,
                            receiving_additional_eden);
  return target_young_length;
}
```

## 计算新生代最大 region 数量

```cpp
//////////////////////////////////////////
// src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////

uint G1Policy::calculate_young_max_length(uint target_young_length) const {
  uint expansion_region_num = 0;
  // GCLockerEdenExpansionPercent: 默认5
  if (GCLockerEdenExpansionPercent > 0) {
    double perc = GCLockerEdenExpansionPercent / 100.0;
    // 当前新生代region数量的5%
    double expansion_region_num_d = perc * young_list_target_length();

    expansion_region_num = (uint) ceil(expansion_region_num_d);
  }
  uint max_length = target_young_length + expansion_region_num;
  assert(target_young_length <= max_length, "overflow");
  return max_length;
}
```
