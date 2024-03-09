# 初始化 region 的大小

在 G1 中, 每个 region 的大小都是相同的, region 的大小会影响 G1 的运行效率。如果 region 太大, 一个 region 虽然可以分配更多的对象, 但回收就会花费更长的时间。如果 region 太小, 在分配对象时会不断申请新的 region, 导致对象的分配效率过于低下。

可以通过参数 -XX:G1HeapRegionSize 来手动设置 region 的大小, 手动设置的 region 大小需要在 1M 到 512M 之间。如果没有手动指定 region 的大小, G1 会在 1M 到 32M 的范围内计算出一个合适的 region 大小。

```cpp
////////////////////////////////////////////
// src/hotspot/share/gc/g1/heapRegion.cpp //
////////////////////////////////////////////

// 调用栈:
// HeapRegion::setup_heap_region_size(unsigned long) heapRegion.cpp:65
// G1Arguments::initialize_alignments() g1Arguments.cpp:56
// GCArguments::initialize_heap_sizes() gcArguments.cpp:64
// universe_init() universe.cpp:783
// init_globals() init.cpp:124
// Threads::create_vm(JavaVMInitArgs *, bool *) threads.cpp:550
// JNI_CreateJavaVM_inner(JavaVM_ **, void **, void *) jni.cpp:3577
// JNI_CreateJavaVM(JavaVM **, void **, void *) jni.cpp:3668
// InitializeJVM java.c:1506
// JavaMain java.c:415
// ThreadJavaMain java_md_macosx.m:720
// _pthread_start 0x0000000188f8a034
/**
 * max_heap_size: 会传入JVM参数: MaxHeapSize
 */
void HeapRegion::setup_heap_region_size(size_t max_heap_size) {
  // G1HeapRegionSize: JVM参数, 默认0
  size_t region_size = G1HeapRegionSize;
  // G1HeapRegionSize为0表示由JVM自己计算region的大小
  if (region_size == 0) {
    // 把堆空间分为2048个region, 计算每个region的大小,
    // 每个region的大小限制在[1M, 32M]之间
    //
    // target_number(): 返回2048
    // min_size(): region最小的大小, 返回1M
    // max_ergonomics_size(): region最大的合理大小,
    //                        超过这个大小可能会降低性能,
    //                        返回32M
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

  // 设置HeapRegion类的一些静态变量

  int region_size_log = log2i_exact(region_size);

  guarantee(LogOfHRGrainBytes == 0, "we should only set it once");
  LogOfHRGrainBytes = region_size_log;

  // 记录region的大小
  guarantee(GrainBytes == 0, "we should only set it once");
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

///////////////////////////////////////////////////////
// src/hotspot/share/utilities/globalDefinitions.hpp //
///////////////////////////////////////////////////////

/**
 * 返回在[min, max]之内的值:
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
