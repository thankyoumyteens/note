# 初始化新生代的大小

新生代的大小就是新生代 reion 的个数。在初始化阶段, G1 会确定新生代预期 region 个数的可选范围\[min_young_length, max_young_length\]的计算方法。在后续调整新生代 region 的时候, G1 会先使用初始化时确定的计算方法计算出新生代 region 个数的可选范围, 然后从这个范围中找到一个满足 MaxGCPauseMillis 的最大值。

## 计算新生代 region 数的预期范围

使用哪种方法计算新生代 region 个数的可选范围, 与启动 JVM 时设置的参数有关:

1. 不设置任何相关的参数: 由 G1 自己决定, min_young_length 的值是: (堆空间的 region 数量 \* G1NewSizePercent) / 100, G1NewSizePercent 是新生代的初始大小占整个堆大小的百分比, 默认为 5。max_young_length 的值是: (堆空间的 region 数量 \* G1MaxNewSizePercent) / 100, G1MaxNewSizePercent 是新生代的最大大小占整个堆大小的百分比, 默认为 60
2. NewRatio: 如果设置了 NewRatio, 那么 min_young_length 和 max_young_length 相同, 都是: 堆空间 region 个数 / (NewRatio + 1)。如果设置了 NewSize 或者 MaxNewSize, NewRatio 参数就会失效
3. NewSize: 如果设置了 NewSize, 那么 min_young_length 固定为: NewSize / 一个 region 的大小, max_young_length 会动态变化
4. MaxNewSize: 如果设置了 MaxNewSize, 那么 max_young_length 固定为: MaxNewSize / 一个 region 的大小, min_young_length 会动态变化
5. 同时设置了 NewSize 和 MaxNewSize: min_young_length 和 max_young_length 都会固定, 不会动态变化, 在后续对新生代进行回收的时候可能满足不了用户期望的暂停时间

```cpp
/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1YoungGenSizer.cpp //
/////////////////////////////////////////////////////////////////

/**
 * 初始化G1YoungGenSizer
 * G1Policy的构造函数中调用
 *
 * _sizer_kind: min_young_length 和 max_young_length 的计算方法,
 *              默认使用SizerDefaults
 * _min_desired_young_length: 最小新生代region数量
 * _max_desired_young_length: 最大新生代region数量
 */
G1YoungGenSizer::G1YoungGenSizer() : _sizer_kind(SizerDefaults),
  _use_adaptive_sizing(true), _min_desired_young_length(0), _max_desired_young_length(0) {
  // 是否手动设置了NewRatio
  if (FLAG_IS_CMDLINE(NewRatio)) {
    if (FLAG_IS_CMDLINE(NewSize) || FLAG_IS_CMDLINE(MaxNewSize)) {
      // 如果设置了NewSize或MaxNewSize会导致NewRatio无效
      log_warning(gc, ergo)("-XX:NewSize and -XX:MaxNewSize override -XX:NewRatio");
    } else {
      // 设置了NewRatio, 则新生代的大小为: 堆大小 / (NewRatio + 1)
      _sizer_kind = SizerNewRatio;
      _use_adaptive_sizing = false;
      return;
    }
  }

  if (NewSize > MaxNewSize) {
    // 参数错误: NewSize不能大于MaxNewSize
    if (FLAG_IS_CMDLINE(MaxNewSize)) {
      log_warning(gc, ergo)("NewSize (" SIZE_FORMAT "k) is greater than the MaxNewSize (" SIZE_FORMAT "k). "
                            "A new max generation size of " SIZE_FORMAT "k will be used.",
                            NewSize/K, MaxNewSize/K, NewSize/K);
    }
    FLAG_SET_ERGO(MaxNewSize, NewSize);
  }

  if (FLAG_IS_CMDLINE(NewSize)) {
    // 设置最小新生代region数量
    _min_desired_young_length = MAX2((uint) (NewSize / HeapRegion::GrainBytes), 1U);
    if (FLAG_IS_CMDLINE(MaxNewSize)) {
      // 设置最大新生代region数量
      _max_desired_young_length = MAX2((uint) (MaxNewSize / HeapRegion::GrainBytes), 1U);
      // 新生代的region数量不会动态变化
      _sizer_kind = SizerMaxAndNewSize;
      _use_adaptive_sizing = _min_desired_young_length != _max_desired_young_length;
    } else {
      // 动态调整最大新生代region数量
      _sizer_kind = SizerNewSizeOnly;
    }
  } else if (FLAG_IS_CMDLINE(MaxNewSize)) {
    // 设置最大新生代region数量
    _max_desired_young_length = MAX2((uint) (MaxNewSize / HeapRegion::GrainBytes), 1U);
    // 动态调整最小新生代region数量
    _sizer_kind = SizerMaxNewSizeOnly;
  }
}

/**
 * 计算新生代region的范围, 调用时机:
 *   1. 堆空间初始化时
 *   2. 堆空间改变时(堆中的region数量改变, 比如GC后需要调整堆空间大小)
 *
 * number_of_heap_regions: 堆中region的总数
 * min_young_length: 新生代region个数的最小值
 * max_young_length: 新生代region个数的最大值
 */
void G1YoungGenSizer::recalculate_min_max_young_length(uint number_of_heap_regions, uint* min_young_length, uint* max_young_length) {
  assert(number_of_heap_regions > 0, "Heap must be initialized");

  switch (_sizer_kind) {
    case SizerDefaults:
      // min_young_length和max_young_length都会动态调整
      *min_young_length = calculate_default_min_length(number_of_heap_regions);
      *max_young_length = calculate_default_max_length(number_of_heap_regions);
      break;
    case SizerNewSizeOnly:
      // min_young_length固定, 只调整max_young_length
      *max_young_length = calculate_default_max_length(number_of_heap_regions);
      *max_young_length = MAX2(*min_young_length, *max_young_length);
      break;
    case SizerMaxNewSizeOnly:
      // max_young_length固定, 只调整min_young_length
      *min_young_length = calculate_default_min_length(number_of_heap_regions);
      *min_young_length = MIN2(*min_young_length, *max_young_length);
      break;
    case SizerMaxAndNewSize:
      // 新生代region个数固定, 不会调整
      break;
    case SizerNewRatio:
      // 新生代region个数调整为当前堆空间的百分比,
      // min_young_length和max_young_length相等
      *min_young_length = MAX2((uint)(number_of_heap_regions / (NewRatio + 1)), 1u);
      *max_young_length = *min_young_length;
      break;
    default:
      ShouldNotReachHere();
  }

  assert(*min_young_length <= *max_young_length, "Invalid min/max young gen size values");
}

uint G1YoungGenSizer::calculate_default_min_length(uint new_number_of_heap_regions) {
  // G1NewSizePercent: 设置新生代的初始大小占整个堆大小的百分比, 默认为 5
  uint default_value = (new_number_of_heap_regions * G1NewSizePercent) / 100;
  // 新生代最少也要有1个region
  return MAX2(1U, default_value);
}

uint G1YoungGenSizer::calculate_default_max_length(uint new_number_of_heap_regions) {
  // G1MaxNewSizePercent: 设置新生代的最大大小占整个堆大小的百分比, 默认为 60
  uint default_value = (new_number_of_heap_regions * G1MaxNewSizePercent) / 100;
  // 新生代最少也要有1个region
  return MAX2(1U, default_value);
}
```

## 初始化新生代 region 的时机

<!-- TODO 存疑 看看_max_desired_young_length的值，它什么时候改变 -->

在堆空间初始化时(G1CollectedHeap 初始化), 会调用上面的 recalculate_min_max_young_length() 函数计算新生代 region 的范围, 并根据这个范围设置新生代 region 的数量。

```cpp
//////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////////////////////

/**
 * G1CollectedHeap初始化时调用
 */
void G1Policy::init(G1CollectedHeap* g1h, G1CollectionSet* collection_set) {
  _g1h = g1h;
  _collection_set = collection_set;

  assert(Heap_lock->owned_by_self(), "Locking discipline.");
  // 传入整个堆空间的region数量
  _young_gen_sizer.adjust_max_new_size(_g1h->max_regions());
  // 记录当前空闲region数量
  _free_regions_at_end_of_collection = _g1h->num_free_regions();
  // 设置新生代region数量
  update_young_length_bounds();

  // 初始化cset
  _collection_set->start_incremental_building();
}

/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1YoungGenSizer.cpp //
/////////////////////////////////////////////////////////////////

void G1YoungGenSizer::adjust_max_new_size(uint number_of_heap_regions) {

  uint temp = _min_desired_young_length;
  uint result = _max_desired_young_length;
  // 计算新生代region的范围
  recalculate_min_max_young_length(number_of_heap_regions, &temp, &result);
  // 计算新生代region最大字节数
  size_t max_young_size = result * HeapRegion::GrainBytes;
  if (max_young_size != MaxNewSize) {
    FLAG_SET_ERGO(MaxNewSize, max_young_size);
  }
}
```

## 设置新生代 region 数量

```cpp
//////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////////////////////

void G1Policy::update_young_length_bounds() {
  assert(!Universe::is_fully_initialized() || SafepointSynchronize::is_at_safepoint(), "must be");
  bool for_young_only_phase = collector_state()->in_young_only_phase();
  update_young_length_bounds(_analytics->predict_pending_cards(for_young_only_phase),
                             _analytics->predict_rs_length(for_young_only_phase));
}

void G1Policy::update_young_length_bounds(size_t pending_cards, size_t rs_length) {
  // 当前新生代region数量
  // return Atomic::load(&_young_list_target_length);
  uint old_young_list_target_length = young_list_target_length();

  // 计算新生代预期region数量
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

## 计算新生代预期 region 数量

```cpp
//////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////////////////////

// Calculates desired young gen length. It is calculated from:
//
// - sizer min/max bounds on young gen
// - pause time goal for whole young gen evacuation
// - MMU goal influencing eden to make GCs spaced apart
// - if after a GC, request at least one eden region to avoid immediate full gcs
//
// We may enter with already allocated eden and survivor regions because there
// are survivor regions (after gc). Young gen revising can call this method at any
// time too.
//
// For this method it does not matter if the above goals may result in a desired
// value smaller than what is already allocated or what can actually be allocated.
// This return value is only an expectation.
//
uint G1Policy::calculate_young_desired_length(size_t pending_cards, size_t rs_length) const {
  uint min_young_length_by_sizer = _young_gen_sizer.min_desired_young_length();
  uint max_young_length_by_sizer = _young_gen_sizer.max_desired_young_length();

  assert(min_young_length_by_sizer >= 1, "invariant");
  assert(max_young_length_by_sizer >= min_young_length_by_sizer, "invariant");

  // Calculate the absolute and desired min bounds first.

  // 堆中当前的survivor region个数
  const uint survivor_length = _g1h->survivor_regions_count();
  // 堆中已经有的新生代region个数
  const uint allocated_young_length = _g1h->young_regions_count();

  // 新生代region数的下边界
  // survivor_length + 1: 至少需要有一个 eden region
  uint absolute_min_young_length = MAX3(min_young_length_by_sizer,
                                        survivor_length + 1,
                                        allocated_young_length);
  // 新生代region数的上边界
  uint absolute_max_young_length = MAX2(max_young_length_by_sizer, absolute_min_young_length);
  // MMU，全称为Minimum Mutator Utilization，
  // 是描述在一段时间内应用程序能够运行的最小百分比
  // 例如，设定MMU为95%, 表示在一个指定的时间段内，mutator最多只能被停顿5%的时间
  uint desired_eden_length_by_mmu = 0;
  uint desired_eden_length_by_pause = 0;

  uint desired_young_length = 0;
  if (use_adaptive_young_list_length()) {
    desired_eden_length_by_mmu = calculate_desired_eden_length_by_mmu();

    double base_time_ms = predict_base_time_ms(pending_cards, rs_length);

    desired_eden_length_by_pause =
      calculate_desired_eden_length_by_pause(base_time_ms,
                                             absolute_min_young_length - survivor_length,
                                             absolute_max_young_length - survivor_length);

    // Incorporate MMU concerns; assume that it overrides the pause time
    // goal, as the default value has been chosen to effectively disable it.
    uint desired_eden_length = MAX2(desired_eden_length_by_pause,
                                    desired_eden_length_by_mmu);

    desired_young_length = desired_eden_length + survivor_length;
  } else {
    // The user asked for a fixed young gen so we'll fix the young gen
    // whether the next GC is young or mixed.
    desired_young_length = min_young_length_by_sizer;
  }
  // Clamp to absolute min/max after we determined desired lengths.
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

# 计算新生代实际 region 数量

```cpp
//////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////////////////////

// Limit the desired (wished) young length by current free regions. If the request
// can be satisfied without using up reserve regions, do so, otherwise eat into
// the reserve, giving away at most what the heap sizer allows.
uint G1Policy::calculate_young_target_length(uint desired_young_length) const {
  uint allocated_young_length = _g1h->young_regions_count();

  uint receiving_additional_eden;
  if (allocated_young_length >= desired_young_length) {
    // Already used up all we actually want (may happen as G1 revises the
    // young list length concurrently, or caused by gclocker). Do not allow more,
    // potentially resulting in GC.
    receiving_additional_eden = 0;
    log_trace(gc, ergo, heap)("Young target length: Already used up desired young %u allocated %u",
                              desired_young_length,
                              allocated_young_length);
  } else {
    // Now look at how many free regions are there currently, and the heap reserve.
    // We will try our best not to "eat" into the reserve as long as we can. If we
    // do, we at most eat the sizer's minimum regions into the reserve or half the
    // reserve rounded up (if possible; this is an arbitrary value).

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
      // Fully eat (or already eating) into the reserve, hand back at most absolute_min_length regions.
      uint receiving_young = MIN3(_free_regions_at_end_of_collection,
                                  desired_young_length,
                                  max_to_eat_into_reserve);
      // We could already have allocated more regions than what we could get
      // above.
      receiving_additional_eden = allocated_young_length < receiving_young ?
                                  receiving_young - allocated_young_length : 0;

      log_trace(gc, ergo, heap)("Young target length: Fully eat into reserve "
                                "receiving young %u receiving additional eden %u",
                                receiving_young,
                                receiving_additional_eden);
    } else if (_free_regions_at_end_of_collection < (desired_young_length + _reserve_regions)) {
      // Partially eat into the reserve, at most max_to_eat_into_reserve regions.
      uint free_outside_reserve = _free_regions_at_end_of_collection - _reserve_regions;
      assert(free_outside_reserve < desired_young_length,
             "must be %u %u",
             free_outside_reserve, desired_young_length);

      uint receiving_within_reserve = MIN2(desired_young_length - free_outside_reserve,
                                           max_to_eat_into_reserve);
      uint receiving_young = free_outside_reserve + receiving_within_reserve;
      // Again, we could have already allocated more than we could get.
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
      // No need to use the reserve.
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
//////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////////////////////

uint G1Policy::calculate_young_max_length(uint target_young_length) const {
  uint expansion_region_num = 0;
  // GCLockerEdenExpansionPercent: 默认5
  if (GCLockerEdenExpansionPercent > 0) {
    double perc = GCLockerEdenExpansionPercent / 100.0;
    double expansion_region_num_d = perc * young_list_target_length();
    // We use ceiling so that if expansion_region_num_d is > 0.0 (but
    // less than 1.0) we'll get 1.
    expansion_region_num = (uint) ceil(expansion_region_num_d);
  }
  uint max_length = target_young_length + expansion_region_num;
  assert(target_young_length <= max_length, "overflow");
  return max_length;
}
```
