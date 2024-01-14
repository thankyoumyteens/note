# 初始化 region 的大小

在 G1 中, 每个 region 的大小都是相同的。region 的大小会影响 G1 的运行效率, 如果 region 过大, 一个 region 虽然可以分配更多的对象, 但回收就会花费更长的时间。如果 region 过小, 则会导致对象的分配效率过于低下。

可以通过参数 -XX:G1HeapRegionSize 来设置 Region 的大小, 它的默认值为 0。如果不指定 region 的大小, G1 就会自己推断出 region 的合适大小。

```cpp
////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegion.cpp //
////////////////////////////////////////////////////////////

/**
 * 调用处: HeapRegion::setup_heap_region_size(MaxHeapSize);
 * MaxHeapSize: JVM参数, 默认96M
 */
void HeapRegion::setup_heap_region_size(size_t max_heap_size) {
    // G1HeapRegionSize: JVM参数, 默认0
  size_t region_size = G1HeapRegionSize;
  // G1HeapRegionSize为0表示由JVM自己计算region的大小
  if (region_size == 0) {
    // 把堆空间分为2048个region, 计算每个region的大小
    // region大小限制在[1M, 32M]之间
    //
    // target_number(): 返回2048
    // min_size(): region最小的大小, 返回1M
    // max_ergonomics_size(): region最大的合理大小, 超过这个大小可能会降低性能, 返回32M
    region_size = clamp(max_heap_size / HeapRegionBounds::target_number(),
                        HeapRegionBounds::min_size(),
                        HeapRegionBounds::max_ergonomics_size());
  }

  // 确保region大小是2的幂
  // 返回值满足:
  //   1. 大于或等于region_size
  //   2. 是2的n次方
  region_size = round_up_power_of_2(region_size);

  // 确保region_size在[1M, 512M]之内
  region_size = clamp(region_size, HeapRegionBounds::min_size(), HeapRegionBounds::max_size());

  // 计算log region_size的值
  int region_size_log = log2i_exact(region_size);

  // 设置HeapRegion类的一些静态变量
  guarantee(LogOfHRGrainBytes == 0, "we should only set it once");
  LogOfHRGrainBytes = region_size_log;

  guarantee(GrainBytes == 0, "we should only set it once");
  // 记录region的大小, 用于后面扩容堆空间
  GrainBytes = region_size;

  guarantee(GrainWords == 0, "we should only set it once");
  GrainWords = GrainBytes >> LogHeapWordSize;

  guarantee(CardsPerRegion == 0, "we should only set it once");
  CardsPerRegion = GrainBytes >> G1CardTable::card_shift();

  LogCardsPerRegion = log2i(CardsPerRegion);

  if (G1HeapRegionSize != GrainBytes) {
    FLAG_SET_ERGO(G1HeapRegionSize, GrainBytes);
  }
}

///////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/utilities/globalDefinitions.hpp //
///////////////////////////////////////////////////////////////////////

/**
 * 返回在[min, max]之内的值
 *   1. value < min, 返回min
 *   2. value > max, 返回max
 *   3. 否则返回value
 */
template<typename T>
inline T clamp(T value, T min, T max) {
  assert(min <= max, "must be");
  return MIN2(MAX2(value, min), max);
}
```
