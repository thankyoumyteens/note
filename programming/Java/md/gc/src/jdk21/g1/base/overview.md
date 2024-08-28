# 总览

## 对象分配

G1 的分配策略: 开启 TLAB 时, JVM 会优先在 TLAB 中分配内存, 当对象在 TLAB 空间分配内存失败时, JVM 会通过 CAS 或加锁直接在堆中分配内存。

## 记忆集

G1 使用记忆集(RSet)记录对象在不同分区之间的引用关系，目的是为了加速垃圾回收的速度。比如一条赋值语句: `objA.field = objB;` G1 会在 objB 的 RSet 中记录 objA 的地址。

在 G1 中提供了 3 种回收算法: Yong GC, Mixed GC 和 Full GC。这三种算法都会回收新生代分区, 所以需要记录 RSet 的情况只有两种:

1. 老年代 Region 到新生代 Region 之间有引用关系
2. 老年代 Region 到老年代 Region 之间有引用关系

在线程运行过程中, 如果对象的引用发生了变化(通常就是赋值操作), 就必须要通知 RSet, 更改其中的记录, 但对于一个 Region 来说, 里面的对象有可能被很多 Region 所引用, 这就要求这个 Region 记录所有引用者的信息, 占用大量的空间。

G1 提供了 3 种 RSet 的粒度:

1. 稀疏 PRT(Per Region Table): 通过哈希表方式来存储每个 region 的引用关系, key 是 region index，value 是 card 数组
2. 细粒度 PRT: 当稀疏 PRT 指定 region 的 card 数量超过阈值时，则在细粒度 PRT 中创建一个对应的 PerRegionTable 对象。每个 PRT 包含一个 Region 的起始地址和一个位图, 位图的每一位对应 Region 的 512 字节
3. 粗粒度位图: 当细粒度 PRT size 超过阈值时，所有 region 形成一个位图。位图中的每一位对应一个 Region

## Refine 线程

Refine 线程是的功能:

1. 处理新生代 region 的抽样, 并且在满足响应时间的这个指标下, 控制新生代 region 的数量。通常有一个线程来处理
2. 管理 RSet, 这是 Refine 最主要的功能。RSet 的更新并不是同步完成的, G1 会把所有的引用关系的变化都先放入到一个队列中, 称为 Dirty Card Queue (DCQ), 然后使用线程来消费这个队列以完成 RSet 的更新。DCQ 通过 Dirty Card Queue Set(DCQS) 来管理, 为了能够并发地处理, 每个 Refine 线程只负责 DCQS 中的某几个 DCQ

JVM 在每次给引用类型的字段赋值时, 会插入一个写后屏障(post-write barrier), 在写后屏障中会做下面的处理:

1. 在全局卡表中找到该字段所在的 card, 并设置为 dirty_card(G1 有一个全局卡表, 它的每个 card 都对应某个 Region 中的 512 字节内存, 如果一个 card 变脏, 就说明对应的 region 存在跨分区的引用)
2. 如果当前线程是 Java 线程(每个 Java 线程都有一个自己的 DCQ), 把该 card 插入线程内部的 DCQ。否则把该 card 插入所有线程共享的全局 DCQ

## Young GC

在创建对象的时候, 如果内存空间不足, 会优先触发新生代回收(Young GC, YGC)。

Young GC 的回收过程:

1. 暂停其他线程(STW)
2. 选择回收集(CSet): 对于 YGC 来说是所有的新生代分区
3. 根处理: 把 GC Roots 直接引用的对象复制到新的分区, 然后把这些对象的所有字段加入队列等待后续的处理
4. RSet 处理: 把 RSet 当成根, 把直接引用的对象复制到新的分区, 然后把这些对象的所有字段加入队列等待后续的处理
5. 复制: 把队列中的字段引用的对象递归复制到新的分区
6. Redirty: 重构 RSet, 因为对象已经移动到新的分区, 需要更新老年代分区到新分区的指针
7. 释放空间: 把新的分区设置为 Survivor, 清空原来的分区
8. 调整新生代分区的数量以匹配目标停顿时间
9. 恢复其他线程(STW 结束)

## Mixed GC

混合回收(Mixed GC)分为两个阶段: 并发标记和垃圾回收。
