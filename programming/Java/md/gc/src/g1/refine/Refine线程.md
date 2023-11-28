# Refine 线程

Refine 线程是 G1 新引入的并发线程池, 线程默认数目为 G1ConcRefinementThreads+1, 它分为两大功能: 

1. 用于处理新生代 region 的抽样, 并且在满足响应时间的这个指标下, 控制新生代 region 的数量。通常有一个线程来处理
2. 管理 RSet, 这是 Refine 最主要的功能。RSet 的更新并不是同步完成的, G1 会把所有的引用关系的变化都先放入到一个队列中, 称为 dirty card queue（DCQ）, 然后使用线程来消费这个队列以完成更新。正常来说有 G1ConcRefinementThreads 个线程处理。实际上除了 Refine 线程更新 RSet 之外, GC 线程或者 Java 线程也可能会更新 RSet, DCQ 通过 Dirty Card Queue Set（DCQS）来管理, 为了能够并发地处理, 每个 Refine 线程只负责 DCQS 中的某几个 DCQ
