# Region

Region 是 G1 堆和操作系统交互的最小管理单位。G1 的 Region 分为 4 类：

1. 空闲 Region(Free Heap Region)
2. 新生代 Region(Young Heap Region)，新生代 Region 又可以分为 Eden 和 Survivor
3. 老年代 Region(Old Heap Region)
4. 大对象 Region(Humongous Heap Region)，大对象可能 1 个 Region 放不下，所以分为 Starts Region 和 Continues Region 两种，Starts 存放大对象的开始，Continues 继续存放 Starts 没存下的部分

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegionType.hpp

```cpp
// 0000 0 [ 0] Free
//
// 0001 0      Young Mask
// 0001 0 [ 2] Eden
// 0001 1 [ 3] Survivor
//
// 0010 0      Humongous Mask
// 0010 0 [ 4] Humongous Starts
// 0010 1 [ 5] Humongous Continues
//
// 01000 [ 8] Old
```

## Region 的大小

在 G1 中每个 Region 的大小都是相同的。Region 的大小会影响 G1 的运行效率，如果 Region 过大，一个 Region 可以分配更多的对象，但回收就会花费更长的时间。如果 Region 过小，就会导致对象的分配效率过于低下。

可以通过参数 -XX:G1HeapRegionSize 来设置 Region 的大小，它的默认值为 0。如果不指定 Region 的大小，G1 就会自己推断出 Region 的合适大小。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegion.cpp

```cpp
/**
 * 推断Region的大小
 * initial_heap_size：初始内存，对应-XX:InitialHeapSize参数的值，等价于-Xms，默认为0
 * max_heap_size：最大分配内存，对应-XX:MaxHeapSize参数的值，等价于-Xmx，默认为96MB
 */
void HeapRegion::setup_heap_region_size(size_t initial_heap_size, size_t max_heap_size) {
  uintx region_size = G1HeapRegionSize;
  // 是否设置了-XX:G1HeapRegionSize
  if (FLAG_IS_DEFAULT(G1HeapRegionSize)) {
    // 如果用户没有指定Region的大小
    // 就根据初始内存和最大分配内存计算平均值
    size_t average_heap_size = (initial_heap_size + max_heap_size) / 2;
    // 把平均值除以Region的数量(默认2048个)得到每个Region的大小
    // 在G1中，Region最小为1MB
    // MAX2函数在计算出的Region大小和1MB中取最大值
    region_size = MAX2(average_heap_size / HeapRegionBounds::target_number(),
                       (uintx) HeapRegionBounds::min_size());
  }
  // 计算出Region的大小后，需要对它进行对齐处理
  // int log2_long(jlong x)函数返回大于或等于给定整数x的最小2的幂次方数
  int region_size_log = log2_long((jlong) region_size);
  region_size = ((uintx)1 << region_size_log);

  // 在G1中，Region最小为1MB，最大为32MB
  // 确保region_size在[1MB,32MB]之间
  if (region_size < HeapRegionBounds::min_size()) {
    region_size = HeapRegionBounds::min_size();
  } else if (region_size > HeapRegionBounds::max_size()) {
    region_size = HeapRegionBounds::max_size();
  }

  // 根据region_size计算其他的空间的大小，比如卡表的大小
  // ...
}
```

## 新生代的 Region 个数

G1 会先计算出整个新生代的所占用内存空间，然后除以每个 Region 的大小，得到新生代需要多少个 Region。

在 G1 中，新生代的内存空间大小一般是动态变化的，可以通过以下参数来设置新生代的大小：

- -XX:NewSize：用于设置新生代的初始大小
- -XX:MaxNewSize：用于设置新生代的最大大小
- -Xmn：用于设置新生代的大小，等价于设置了 NewSize 和 MaxNewSize，且 NewSize=MaxNewSize

例如，以下命令将新生代的初始大小设置为 256MB，最大大小设置为 1024MB：

```sh
java -XX:+UseG1GC -XX:NewSize=256m -XX:MaxNewSize=1024m -jar myapp.jar
```

如果设置了 NewSize 和 MaxNewSize，G1 会根据它们来计算新生代 Region 的个数。

- -XX:NewRatio：用于设置新生代占整个堆内存的比例

这个参数通常与 -XX:MaxNewSize 一起使用，以控制新生代占用的内存空间范围。例如，以下命令将新生代的初始大小设置为堆内存的 30%，最大大小为 64GB：

```sh
java -XX:+UseG1GC -XX:NewRatio=3 -XX:MaxNewSize=64g -jar myapp.jar
```

如果设置了 NewSize 和 MaxNewSize，G1 会忽略 NewRatio。如果只设置了 NewRatio，则 NewSize=MaxNewSize=堆内存/(NewRatio+1)。

- -XX:G1NewSizePercent：用于设置年新生代的初始大小占整个堆内存大小的百分比，默认为 5
- -XX:G1MaxNewSizePercent：用于设置年新生代的最大大小占整个堆内存大小的百分比，默认为 60

如果没有设置 NewSize 和 MaxNewSize，或只设置了其中的一个，G1 会根据 G1NewSizePercent 和 G1MaxNewSizePercent 来计算新生代内存的最大值和最小值。

如果新生代内存的最大值和最小值相等，则说明新生代的大小不会动态变化，这意味着 G1 在后续对新生代进行 GC 的时候可能满足不了用户期望的暂停时间。

## 新生代分区列表

G1 会维护一个新生代分区列表，当新生代需要扩大时，G1 会把空闲的 Region 加入到新生代分区列表中，如果没有空闲的 Region，G1 会分配新的 Region 然后把它加入到新生代分区列表中。

参数-XX:GCTimeRatio 用于设置程序运行时间与 GC 执行时间之间的比率，计算方式为：100\*(1/(1+GCTimeRatio))。GCTimeRatio 的默认值为 9，即 GC 时间占比超过 10%的时候才需要扩展内存空间。
