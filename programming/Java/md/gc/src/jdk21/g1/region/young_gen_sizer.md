# 新生代的预期范围

在设置新生代大小前, G1 会先预测新生代的预期范围, 然后参考这个范围找到一个合适的值, 作为新生代 region 的数量。使用哪种方法计算新生代 region 数量的预期范围, 与启动 JVM 时设置的参数有关:

1. 不设置任何相关的参数: 最小值是: (堆空间的 region 数量 × G1NewSizePercent) ÷ 100, G1NewSizePercent 是新生代的初始大小占整个堆大小的百分比, 默认为 5。最大值是: (堆空间的 region 数量 × G1MaxNewSizePercent) ÷ 100, G1MaxNewSizePercent 是新生代的最大大小占整个堆大小的百分比, 默认为 60
2. NewRatio: 如果设置了 NewRatio, 那么最小值和最大值相同, 都是: 堆空间 region 个数 ÷ (NewRatio + 1)。如果设置了 NewSize 或者 MaxNewSize, NewRatio 参数就会失效
3. NewSize: 如果设置了 NewSize, 那么最小值固定为: NewSize ÷ 一个 region 的大小, 最大值是: (堆空间的 region 数量 × G1MaxNewSizePercent) ÷ 100
4. MaxNewSize: 如果设置了 MaxNewSize, 那么最大值固定为: MaxNewSize ÷ 一个 region 的大小, 最小值是: (堆空间的 region 数量 × G1NewSizePercent) ÷ 100
5. 同时设置了 NewSize 和 MaxNewSize: 最小值和最大值都会固定, 不会动态变化, 在后续对新生代进行回收的时候可能满足不了用户期望的暂停时间

```cpp
/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1YoungGenSizer.cpp //
/////////////////////////////////////////////////////////////////

/**
 * 初始化G1YoungGenSizer
 * G1Policy的构造函数中调用
 *
 * _sizer_kind: 预期范围的计算方法,
 *              默认使用SizerDefaults
 * _min_desired_young_length: 预期最小新生代region数量
 * _max_desired_young_length: 预期最大新生代region数量
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
      // 关闭自适应新生代大小
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
      // 如果NewSize==MaxNewSize, 则关闭自适应新生代大小
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
 * 计算新生代region的预期范围

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
