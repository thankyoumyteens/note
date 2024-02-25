# region

region 是 G1 堆和操作系统交互的最小管理单位。G1 的 region 分为 4 类:

1. 空闲 region(Free Heap Region)
2. 新生代 region(Young Heap Region): 新生代 region 又可以分为 eden region 和 survivor region
3. 老年代 region(Old Heap Region)
4. 大对象 region(Humongous Heap Region): 如果一个对象的大小超过了一个 region 容量的一半, 就称为大对象, 存放到 humongous region 中。如果某个对象特别大, 1 个 region 放不下的话, 需要多个 region 共同存放, 存放大对象起始内容的 region 称为 starts humongous, 其余的 region 称为 continues humongous

```cpp
////////////////////////////////////////////////
// src/hotspot/share/gc/g1/heapRegionType.hpp //
////////////////////////////////////////////////

/**
 * region的类型
 */
class HeapRegionType {

private:
  // 使用tag来标记不同region的类型
  // tag分为两部分:
  //   主类型 (young, old, humongous)                    : 高 N-1 位
  //   副类型 (eden / survivor, starts / cont hum, etc.) : 最低 1 位
  //
  // 00000 0 [ 0] Free
  //
  // 00001 0 [ 2] Young Mask
  // 00001 0 [ 2] Eden
  // 00001 1 [ 3] Survivor
  //
  // 00010 0 [ 4] Humongous Mask
  // 00010 0 [ 4] Starts Humongous
  // 00010 1 [ 5] Continues Humongous
  //
  // 00100 0 [ 8] Old Mask
  // 00100 0 [ 8] Old
  //
  typedef enum {
    FreeTag               = 0,

    YoungMask             = 2,
    EdenTag               = YoungMask,
    SurvTag               = YoungMask + 1,

    HumongousMask         = 4,
    StartsHumongousTag    = HumongousMask,
    ContinuesHumongousTag = HumongousMask + 1,

    OldMask               = 8,
    OldTag                = OldMask
  } Tag;

  volatile Tag _tag;

public:
  // 定义常用的类型

  // const HeapRegionType HeapRegionType::Eden      = HeapRegionType(EdenTag);
  static const HeapRegionType Eden;
  // const HeapRegionType HeapRegionType::Survivor  = HeapRegionType(SurvTag);
  static const HeapRegionType Survivor;
  // const HeapRegionType HeapRegionType::Old       = HeapRegionType(OldTag);
  static const HeapRegionType Old;
  // const HeapRegionType HeapRegionType::Humongous = HeapRegionType(StartsHumongousTag);
  static const HeapRegionType Humongous;
};
```
