# ParallelOld收集器

Parallel Old是Parallel Scavenge收集器的老年代版本，支持多线程并发收集，基于标记-整理算法实现。

这个收集器是直到JDK 6时才开始提供的，在此之前，新生代的Parallel Scavenge收集器一直没有合适的老年代收集器搭配。

直到Parallel Old收集器出现后，吞吐量优先收集器终于有了比较名副其实的搭配组合，在注重吞吐量或者处理器资源较为稀缺的场合，都可以优先考虑Parallel Scavenge加Parallel Old收集器这个组合。
