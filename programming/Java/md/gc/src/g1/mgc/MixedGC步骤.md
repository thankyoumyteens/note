# Mixed GC 步骤

Mixed GC 分为两个阶段：并发标记和垃圾回收。其中垃圾回收阶段一定发生在并发标记阶段之后。

## 并发标记

并发标记阶段可以分为：初始标记阶段，并发标记阶段，再标记阶段和清理阶段。

### 初始标记子阶段

标记由根集合直接可达的所有对象（栈对象、全局对象、JNI 对象等），根是对象图的起点，因此初始标记需要将 Java 线程暂停。实际上，初始标记借用了 Young GC 的结果，将 Young GC 后的新生代 Survivor region 作为根，所以 Mixed GC 一定发生在 Young GC 之后，且不需要再进行一次初始标记。

虽然并发标记是以 Survivor region 为根对整个老年代进行标记，但是，存在被根直接引用、但不被 Survivor 中的对象引用的老年代对象，这些对象会在 Young GC 的根处理阶段中加入到标记栈中。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
/**
 * Young GC 的根处理阶段
 * p 是根集合直接引用的对象
 */
void G1ParCopyClosure<barrier, do_mark_object>::do_oop_work(T* p) {
  T heap_oop = oopDesc::load_heap_oop(p);

  if (oopDesc::is_null(heap_oop)) {
    return;
  }

  oop obj = oopDesc::decode_heap_oop_not_null(heap_oop);

  const InCSetState state = _g1->in_cset_state(obj);
  if (state.is_in_cset()) {
    // 在CSet中的对象
    // YGC的根处理阶段中会复制这些对象
  } else {
    // 对于不在CSet中的对象，先把对象标记为存活，在并发标记的时候作为根对象
    if (state.is_humongous()) {
      // 如果是大对象，直接把大对象标记为存活对象
      _g1->set_humongous_is_live(obj);
    }
    // 当进行一般的YGC时，参数设置为G1MarkNone，
    // 当发现开启了并发标记则设置为G1MarkFromRoot
    if (do_mark_object == G1MarkFromRoot) {
      // 把根对象放入到标记栈
      mark_object(obj);
    }
  }

  if (barrier == G1BarrierEvac) {
    // ...
  }
}

void G1ParCopyHelper::mark_object(oop obj) {
  // 把这个对象标记为灰色，在并发标记的时候作为根
  _cm->grayRoot(obj, (size_t) obj->size(), _worker_id);
}
```

### 并发标记子阶段

当 Young GC 执行结束之后，如果发现满足并发标记的条件，并发线程就开始进行并发标记。根据新生代的 Survivor region 以及老年代 region 的 RSet 开始并发标记。并发标记的时机是在 Young GC 之后，只有达到 InitiatingHeapOccupancyPercent 阈值后，才会触发并发标记。InitiatingHeapOccupancyPercent 默认值是 45，表示的是当已经分配的内存加上即将分配的内存超过内存总容量的 45% 就可以开始并发标记。并发标记线程在并发标记阶段启动，由参数 -XX:ConcGCThreads（默认为 GC 线程数的 1/4，即-XX:ParallelGCThreads/4）控制启动数量，每个线程每次只扫描一个 region，从而标记出存活对象。在标记的时候还会计算存活的数量（Live Data Accounting），只要一个对象被标记，同时会计算字节数，并计入 region 空间，这和并发算法相关。并发标记会对所有的 region 进行标记。这个阶段并不需要 STW，标记线程和 Java 线程并发运行。

### 再标记子阶段

再标记（Remark）是最后一个标记阶段。在该阶段中，G1 需要一个暂停的时间，找出所有未被访问的存活对象，同时完成存活内存数据计算。引入该阶段的目的，是为了能够达到结束标记的目标。要结束标记的过程，要满足三个条件：

1. 从根出发，并发标记阶段已经追踪了所有的存活对象
2. 标记栈是空的
3. 所有的引用变更都被处理了。这里的引用变更包括新增空间分配和引用变更，新增的空间所有对象都认为是存活的，引用变更是处理 SATB

前两个条件是很容易达到的，但是最后一个是很困难的。如果不引入一个 STW 的再标记过程，那么应用会不断地更新引用，也就是说，会不断产生新的引用变更，因而永远也无法达成完成标记的条件。

这个阶段也是并行执行的，通过参数 -XX:ParallelGCThreads 可设置 STW 时可用的 GC 线程数。同时，引用处理也是再标记阶段的一部分，所有重度使用引用对象（弱引用、软引用、虚引用、最终引用）的应用都需要不少的开销来处理引用。

### 清理子阶段

再标记阶段之后进入清理阶段，也是需要 STW 的。清理阶段主要执行以下操作：

1. 统计存活对象，这是利用 RSet 和 BitMap 来完成的，统计的结果将会用来排序 region，以用于下一次的 CSet 的选择。根据 SATB 算法，需要把新分配的对象，即不在本次并发标记范围内的新分配对象，都视为存活对象
2. 交换标记位图，为下次并发标记准备
3. 重置 RSet，此时老年代 region 已经标记完成，如果标记后的 region 没有引用对象，这说明引用已经改变，这个时候可以删除原来的 RSet 里面的引用关系
4. 把空闲 region 放到空闲 region 列表中。这里的空闲指的是全都是垃圾对象的 region，如果 region 中还有任何存活对象都不会释放，真正释放是在垃圾回收阶段。实际上，清理操作并不会删除垃圾对象，也不会执行存活对象的拷贝。在极端情况下，该阶段结束之后，空闲 region 列表将毫无变化，JVM 的内存使用情况也毫无变化。

## 垃圾回收

Mixed GC 的垃圾回收实际上与 Young GC 是一样的：

1. 第一个步骤是从所有 region 中选出若干个 region 进行回收，这些被选中的 region 称为 Collect Set（简称 CSet）
2. 第二个步骤是把这些 region 中存活的对象复制到空闲的 region 中去，同时把这些已经被回收的 region 放到空闲 region 列表中

垃圾回收总是要在一次新的 Young GC 开始后才会发生。
