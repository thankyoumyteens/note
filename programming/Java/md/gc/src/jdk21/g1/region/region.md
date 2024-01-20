# region

Region 是 G1 堆和操作系统交互的最小管理单位。G1 的 Region 分为 4 类:

1. 空闲 Region(Free Heap Region)
2. 新生代 Region(Young Heap Region), 新生代 Region 又可以分为 Eden 和 Survivor
3. 老年代 Region(Old Heap Region)
4. 大对象 Region(Humongous Heap Region), 大对象可能 1 个 Region 放不下, 需要多个 Region 共同存放, Starts 存放大对象的开始, Continues 继续存放 Starts 没存下的部分

```cpp
////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegionType.hpp //
////////////////////////////////////////////////////////////////

/**
 * Region的类型
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

  Tag get() const {
    hrt_assert_is_valid(_tag);
    return _tag;
  }

  void set(Tag tag) {
    hrt_assert_is_valid(tag);
    hrt_assert_is_valid(_tag);
    _tag = tag;
  }

  // Sets the type to 'tag', expecting the type to be 'before'. This
  // is available for when we want to add sanity checking to the type
  // transition.
  void set_from(Tag tag, Tag before) {
    hrt_assert_is_valid(tag);
    hrt_assert_is_valid(before);
    hrt_assert_is_valid(_tag);
    assert(_tag == before, "HR tag: %u, expected: %u new tag; %u", _tag, before, tag);
    _tag = tag;
  }

  // Private constructor used for static constants
  HeapRegionType(Tag t) : _tag(t) { hrt_assert_is_valid(_tag); }

public:

  bool is_free() const { return get() == FreeTag; }

  bool is_young()    const { return (get() & YoungMask) != 0; }
  bool is_eden()     const { return get() == EdenTag;  }
  bool is_survivor() const { return get() == SurvTag;  }

  bool is_humongous()           const { return (get() & HumongousMask) != 0;   }
  bool is_starts_humongous()    const { return get() == StartsHumongousTag;    }
  bool is_continues_humongous() const { return get() == ContinuesHumongousTag; }

  bool is_old() const { return (get() & OldMask) != 0; }

  bool is_old_or_humongous() const { return (get() & (OldMask | HumongousMask)) != 0; }

  void set_free() { set(FreeTag); }

  void set_eden()        { set_from(EdenTag, FreeTag); }
  void set_eden_pre_gc() { set_from(EdenTag, SurvTag); }
  void set_survivor()    { set_from(SurvTag, FreeTag); }

  void set_starts_humongous()    { set_from(StartsHumongousTag,    FreeTag); }
  void set_continues_humongous() { set_from(ContinuesHumongousTag, FreeTag); }

  void set_old() { set(OldTag); }


  HeapRegionType() : _tag(FreeTag) { hrt_assert_is_valid(_tag); }

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
