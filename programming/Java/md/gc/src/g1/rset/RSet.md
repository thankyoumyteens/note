# RSet

G1使用记忆集(RSet)记录从非收集部分指向收集部分的指针的集合。

有两种方法记录引用关系：Point out 和 Point in。Point out在引用方的RSet中记录被引用方的地址。而Point in在被引用方的Rset中记录引用方。比如赋值语句：objA.field = objB; Point out会在objA的RSet中记录objB的地址，Point in会在objB的RSet中记录objA的地址。

G1使用了Point in的方法。

在G1中提供了3种收集算法：Yong GC、Mixed GC和Full GC。Yong GC总是收集所有新生代Region，Mixed GC会收集所有的新生代Region以及部分老年代Region，而Full GC则收集所有的Region。

Region之间有5种引用关系：

1. Region内部有引用关系，无论是新生代Region还是老年代Region内部的引用，都无需记录引用关系，因为回收的时候是针对一个Region而言，即这个Region要么被回收要么不回收，回收的时候会遍历整个Region，所以无需记录这种额外的引用关系
2. 新生代Region到新生代Region之间有引用关系，这个无需记录，原因在于G1的3中回收算法都会全量处理新生代Region，所以它们都会被遍历，所以无需记录新生代到新生代之间的引用
3. 新生代Region到老年代Region之间有引用关系，这个无需记录，Yong GC针对的是所有新生代Region，无需这个引用关系，Mixed GC也会回收所有新生代Region，那么遍历新生代Region的时候自然能找到引用的老年代Region，所以也无需这个引用，对于Full GC来说更无需这个引用关系，所有的Region都会被处理
4. 老年代Region到新生代Region之间有引用关系，这个需要记录，在Yong GC的时候有两种GC Root，一个就是栈和方法区中变量的引用，另外一个就是老年代Region到新生代Region的引用
5. 老年代Region到老年代Region之间有引用关系，这个需要记录，在Mixed GC的时候可能只有部分老年代Region被回收，所以必须记录引用关系，快速找到哪些对象是活跃的

在线程运行过程中，如果对象的引用发生了变化（通常就是赋值操作），就必须要通知RSet，更改其中的记录，但对于一个Region来说，里面的对象有可能被很多Region所引用，这就要求这个Region记录所有引用者的信息。为此G1使用了卡表PRT（Per region Table）来记录这种变化。

每个Region都包含了一个PRT，它通过HeapRegion里面的HeapRegionRemSet获得，而HeapRegionRemSet包含了一个OtherRegionsTable，也就是PRT。

一个对象可能被引用的次数不固定，它可能被很多对象引用，也可能只被一个对象引用，所以OtherRegionsTable使用了三种不同的粒度来描述引用，主要有以下三种粒度：

1. 稀疏PRT：通过哈希表方式来存储，默认长度为4。key是region_index，value是card数组
2. 细粒度PRT：PRT指针的数组。每个PRT元素包含了一个HeapRegion的起始地址和一个位图，这个位图描述这个HeapRegion的引用情况，每一位对应Region的512字节，所以它的大小为HeapRegionSize%512，这样可以使用更少的内存存储更多的引用关系
3. 粗粒度位图：通过位图来表示，位图中的每一位代表一个Region

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
  // 细粒度PRT，PerRegionTable*的数组
  PerRegionTable** _fine_grain_regions;
  // ...
  // 稀疏PRT
  SparsePRT   _sparse_table;
  // ...
};
```
