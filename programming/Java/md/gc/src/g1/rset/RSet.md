# RSet

G1 使用记忆集(RSet)记录从非收集部分指向收集部分的指针的集合。

有两种方法记录引用关系: Point out 和 Point in。Point out 在引用方的 RSet 中记录被引用方的地址。而 Point in 在被引用方的 Rset 中记录引用方。比如赋值语句: objA.field = objB; Point out 会在 objA 的 RSet 中记录 objB 的地址, Point in 会在 objB 的 RSet 中记录 objA 的地址。

G1 使用了 Point in 的方法。

在 G1 中提供了 3 种收集算法: Yong GC、Mixed GC 和 Full GC。Yong GC 总是收集所有新生代 Region, Mixed GC 会收集所有的新生代 Region 以及部分老年代 Region, 而 Full GC 则收集所有的 Region。

Region 之间有 5 种引用关系: 

1. Region 内部有引用关系, 无论是新生代 Region 还是老年代 Region 内部的引用, 都无需记录引用关系, 因为回收的时候是针对一个 Region 而言, 即这个 Region 要么被回收要么不回收, 回收的时候会遍历整个 Region, 所以无需记录这种额外的引用关系
2. 新生代 Region 到新生代 Region 之间有引用关系, 这个无需记录, 原因在于 G1 的 3 中回收算法都会全量处理新生代 Region, 所以它们都会被遍历, 所以无需记录新生代到新生代之间的引用
3. 新生代 Region 到老年代 Region 之间有引用关系, 这个无需记录, Yong GC 针对的是所有新生代 Region, 无需这个引用关系, Mixed GC 也会回收所有新生代 Region, 那么遍历新生代 Region 的时候自然能找到引用的老年代 Region, 所以也无需这个引用, 对于 Full GC 来说更无需这个引用关系, 所有的 Region 都会被处理
4. 老年代 Region 到新生代 Region 之间有引用关系, 这个需要记录, 在 Yong GC 的时候有两种 GC Root, 一个就是栈和方法区中变量的引用, 另外一个就是老年代 Region 到新生代 Region 的引用
5. 老年代 Region 到老年代 Region 之间有引用关系, 这个需要记录, 在 Mixed GC 的时候可能只有部分老年代 Region 被回收, 所以必须记录引用关系, 快速找到哪些对象是活跃的

在线程运行过程中, 如果对象的引用发生了变化(通常就是赋值操作), 就必须要通知 RSet, 更改其中的记录, 但对于一个 Region 来说, 里面的对象有可能被很多 Region 所引用, 这就要求这个 Region 记录所有引用者的信息。为此 G1 使用了卡表 PRT(Per region Table)来记录这种变化。

每个 Region 都包含了一个 PRT, 它通过 HeapRegion 里面的 HeapRegionRemSet 获得, 而 HeapRegionRemSet 包含了一个 OtherRegionsTable, 也就是 PRT。

一个对象可能被引用的次数不固定, 它可能被很多对象引用, 也可能只被一个对象引用, 所以 OtherRegionsTable 使用了三种不同的粒度来描述引用, 主要有以下三种粒度: 

1. 稀疏 PRT: 通过哈希表方式来存储, 默认长度为 4。key 是 region_index, value 是 card 数组
2. 细粒度 PRT: PRT 指针的数组。每个 PRT 元素包含了一个 HeapRegion 的起始地址和一个位图, 这个位图描述这个 HeapRegion 的引用情况, 每一位对应 Region 的 512 字节, 所以它的大小为 HeapRegionSize%512, 这样可以使用更少的内存存储更多的引用关系
3. 粗粒度位图: 通过位图来表示, 位图中的每一位代表一个 Region

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegion.hpp

```cpp
/**
 * Region
 */
class HeapRegion: public G1OffsetTableContigSpace {
  friend class VMStructs;
 private:

  HeapRegionRemSet* _rem_set;
  // ...
};
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegionRemSet.hpp

```cpp
/**
 * RSet
 */
class HeapRegionRemSet : public CHeapObj<mtGC> {
// ...
private:
  // ...
  OtherRegionsTable _other_regions;
  // ...
}

/**
 * OtherRegionsTable
 */
class OtherRegionsTable VALUE_OBJ_CLASS_SPEC {
  // ...
  // 粗粒度位图
  BitMap      _coarse_map;
  // ...
  // 细粒度PRT, PerRegionTable*的数组
  PerRegionTable** _fine_grain_regions;
  // ...
  // 稀疏PRT
  SparsePRT   _sparse_table;
  // ...
};
```
