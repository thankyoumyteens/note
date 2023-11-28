# DCQS 分区

DCQS 分为 4 个区: 白、绿、黄、红, 由 Green、Yellow 和 Red 三个变量控制边界: 

1. 白区: `[0, Green)`, 对于该区, Refine 线程并不处理, 交由 GC 线程来处理 DCQ
2. 绿区: `[Green, Yellow)`, 在该区中, Refine 线程开始启动, 并且根据 DCQS 的大小启动不同数量的 Refine 线程来处理 DCQ
3. 黄区: `[Yellow, Red)`, 在该区, 所有的 Refine 线程(除了抽样线程)都参与 DCQ 处理
4. 红区: `[Red, +∞)`, 在该区, 不仅仅所有的 Refine 线程参与处理 RSet, Java 线程也会参与处理 DCQ

Green、Yellow 和 Red 三个值通过三个参数设置: -XX:G1ConcRefinementGreenZone、-XX:G1ConcRefinementYellowZone、-XX:G1ConcRefinementRedZone, 默认值都是 0。如果没有设置这三个值, G1 则自动推断这三个区的阈值大小。

- -XX:G1ConcRefinementGreenZone: 是-XX:ParallelGCThreads 的值
- -XX:G1ConcRefinementYellowZone: 是-XX:G1ConcRefinementGreenZone 的 3 倍
- -XX:G1ConcRefinementRedZone: 是-XX:G1ConcRefinementGreenZone 的 6 倍

Refine 线程的个数可以通过参数-XX:G1ConcRefinementThreads 设置, 默认值为 0, 当没有设置该值时 G1 会把它设置为-XX:ParallelGCThreads。

-XX:ParallelGCThreads 也可以通过参数设置, 默认值为 0, 如果没有设置, G1 也可以自己推断出来: 

- 当 cpu 内核的个数小于等于 8 时, ParallelGCThreads 的值是: 
- 当 cpu 内核的个数大于 8 时, ParallelGCThreads 的值是: 8+(cpu 内核的个数-8)\*5/8

在绿区的时候, Refine 线程会根据 DCQS 数值的大小启动不同数量的 Refine 线程, 参数-XX:G1ConcRefinementThresholdStep 用于控制每个 Refine 线程消费队列的步长, 如果不设置, 可以自动推断。
