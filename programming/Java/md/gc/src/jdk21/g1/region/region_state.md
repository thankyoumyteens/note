# region的3种状态

G1可使用的堆大小取决于JVM参数MaxHeapSize, 但是G1不会一开始就把所有堆都分配成region, 而是根据需要才分配, 没有分配成region的内存处于Uncommitted状态, Uncommitted状态的region可以用于分配对象。已经分配成region的内存处于Commited状态, Commited状态又分为Active状态和Inactive状态。

G1 使用HeapRegionManager类的对象管理堆空间, 它有一个字段 _committed_map 记录了堆中属于Committed状态的region。如果不需要那么多的region, G1也会重新把一些region变回Uncommitted状态。

region有3种状态:

1. Uncommitted: 属于未分配的内存
2. Active: 表示这是个准备使用的region, 处于Active状态的region才可以用于分配对象
3. Inactive : 准备转换成Uncommit状态

3种状态之间的转换:

- Uncommitted -> Active
- Active      -> Inactive
- Inactive    -> Active
- Inactive    -> Uncommitted

```cpp
///////////////////////////////////////////////////
// src/hotspot/share/gc/g1/heapRegionManager.hpp //
///////////////////////////////////////////////////

class HeapRegionManager: public CHeapObj<mtGC> {
  // 记录当前处于committed状态的region
  G1CommittedRegionMap _committed_map;
}

//////////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1CommittedRegionMap.hpp //
//////////////////////////////////////////////////////

class G1CommittedRegionMap : public CHeapObj<mtGC> {
  // 使用位图标记region的状态, true表示Active, false表示Inactive

  // 位图, 每一位指向一个Active状态的region
  CHeapBitMap _active;
  // 位图, 每一位指向一个Inactive状态的region
  CHeapBitMap _inactive;

  // Active状态的region个数
  uint _num_active;

  // Inactive状态的region个数
  uint _num_inactive;
}
```
