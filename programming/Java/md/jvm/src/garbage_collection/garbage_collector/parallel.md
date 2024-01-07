# ParallelGC(ParallelScavenge 和 ParallelOld)

Parallel Scavenge 是一款新生代回收器, 它是基于标记-复制算法实现的, 能够并行回收的多线程回收器。Parallel Scavenge 的特点是它的关注点与其他回收器不同, 其他回收器的关注点是尽可能地缩短垃圾回收时用户线程的停顿时间, 而 Parallel Scavenge 的目标是提高吞吐量, 它不会关心 GC 时用户线程的停顿时间。

吞吐量是处理器运行用户代码的时间与处理器总消耗时间的比值。如果 JVM 完成某个任务, 用户代码加上垃圾回收总共耗费了 100 分钟, 其中垃圾回收花掉 1 分钟, 那吞吐量就是 99%。停顿时间越短的垃圾回收器就越适合需要与用户交互的程序, 良好的响应速度能提升用户体验。而高吞吐量则可以最高效率地利用处理器资源, 尽快完成程序的运算任务, 主要适合在后台运算而不需要太多交互的分析任务。

Parallel Old 是 Parallel Scavenge 的老年代版本, 支持多线程并行回收, 基于标记-整理算法实现。在注重吞吐量或者处理器资源较为稀缺的场合, 都可以优先考虑 Parallel Scavenge 加 Parallel Old 这个组合。JDK 8 默认的垃圾回收器就是 Parallel Scavenge + Parallel Old。
