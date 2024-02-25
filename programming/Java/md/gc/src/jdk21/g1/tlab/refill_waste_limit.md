# refill_waste_limit

JVM 内部会维护一个叫做 refill_waste_limit 的值, 用于判断当前 TLAB 不够分配时, 是否需要申请新的 TLAB:

1. 当 TLAB 剩余空间大于 refill_waste_limit 时, 说明 TLAB 剩余的空间还能满足很多对象的分配, 此时会选择在 TLAB 外面(region 中)分配这个比较大的对象
2. 当 TLAB 剩余空间小于 refill_waste_limit 时, 则会废弃当前 TLAB, 新建一个新的 TLAB 来分配对象

refill_waste_limit 的值可以使用参数 -XX:TLABRefillWasteFraction 来设置, 默认值为 64, 表示 1/64 的 TLAB 空间可以浪费, 成为内存碎片。旧的 TLAB 不用处理, 在垃圾回收的时候, 垃圾回收器不会特殊处理 TLAB, 而是把 Eden 空间当作一个整体来回收里面的对象。

JVM 还提供了一个参数 -XX:TLABWasteIncrement 用于动态增加这个 refill_waste_limit 的值, 默认值为 4 个字。默认情况下, TLAB 的大小和 refill_waste_limit 都会在运行时不断调整, 使系统的运行状态达到最优。可以使用 -XX:-ResizeTLAB 禁止自动调整 TLAB 的大小。-XX:+PrintTLAB 可以跟踪 TLAB 的使用情况。

在动态调整的过程中, 也不能无限制变更, 所以 JVM 提供了参数 -XX:MinTLABSize 用于控制 TLAB 的最小值, 默认值 2K。 对于 G1 来说, 由于大对象都不在新生代, 所以 TLAB 也不能分配大对象, Region 大小的一半就会被认定为大对象, 所以 TLAB 肯定不会超过 Region 大小的一半。

TLAB 的剩余空间不足以分配当前对象时, 会分成以下两种情况:

1. 如果 TLAB 的剩余空间小于或等于 refill_waste_limit, 那么就对这个 TLAB 进行填充一个 dummy 对象, 然后去申请一个新的 TLAB。G1 在扫描时, 当遇到对象时会一整个跳过, 而遇到空白区域时则需要一个字一个字的来扫描, 这势必影响效率, 为此, G1 通过为这些空白区域也分配一个空对象, 即 dummy 对象, 从而让扫描变得更快
2. 如果 TLAB 的剩余空间大于 refill_waste_limit, 虽然不够分配当前这个对象, 但是可以用来分配其他小一点的对象, 那么这次就不使用 TLAB 进行分配, 直接返回 null, 让 JVM 去 region 中分配这个对象, 并且增大 refill_waste_limit 的值。这样, refill_waste_limit 就会随着 JVM 的运行不断增大, 从而避免 TLAB 中的一小块剩余空间被一直保留, JVM 频繁去 region 中分配对象的情况

```cpp
////////////////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/shared/threadLocalAllocBuffer.cpp //
////////////////////////////////////////////////////////////////////////////

/**
 * refill_waste_limit的初始化
 */
size_t ThreadLocalAllocBuffer::initial_refill_waste_limit() {
  return desired_size() / TLABRefillWasteFraction;
}

///////////////////////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/shared/threadLocalAllocBuffer.inline.hpp //
///////////////////////////////////////////////////////////////////////////////////

/**
 * 增大refill_waste_limit的值,
 * 避免频繁在堆中直接分配对象
 */
void ThreadLocalAllocBuffer::record_slow_allocation(size_t obj_size) {

  set_refill_waste_limit(refill_waste_limit() + refill_waste_limit_increment());

  _slow_allocations++;

  log_develop_trace(gc, tlab)("TLAB: %s thread: " PTR_FORMAT " [id: %2d]"
                              " obj: " SIZE_FORMAT
                              " free: " SIZE_FORMAT
                              " waste: " SIZE_FORMAT,
                              "slow", p2i(thread()), thread()->osthread()->thread_id(),
                              obj_size, free(), refill_waste_limit());
}
```
