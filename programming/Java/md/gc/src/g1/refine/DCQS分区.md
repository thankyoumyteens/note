# DCQS分区

DCQS分为4个区：白、绿、黄、红，由Green、Yellow和Red三个变量控制边界：

1. 白区：`[0，Green)`，对于该区，Refine线程并不处理，交由GC线程来处理DCQ
2. 绿区：`[Green，Yellow)`，在该区中，Refine线程开始启动，并且根据DCQS的大小启动不同数量的Refine线程来处理DCQ
3. 黄区：`[Yellow，Red)`，在该区，所有的Refine线程(除了抽样线程)都参与DCQ处理
4. 红区：`[Red，+∞)`，在该区，不仅仅所有的Refine线程参与处理RSet，用户线程也会参与处理DCQ

Green、Yellow和Red三个值通过三个参数设置：-XX:G1ConcRefinementGreenZone、-XX:G1ConcRefinementYellowZone、-XX:G1ConcRefinementRedZone，默认值都是0。如果没有设置这三个值，G1则自动推断这三个区的阈值大小。

- -XX:G1ConcRefinementGreenZone：是-XX:ParallelGCThreads的值
- -XX:G1ConcRefinementYellowZone：是-XX:G1ConcRefinementGreenZone的3倍
- -XX:G1ConcRefinementRedZone：是-XX:G1ConcRefinementGreenZone的6倍

Refine线程的个数可以通过参数-XX:G1ConcRefinementThreads设置，默认值为0，当没有设置该值时G1会把它设置为-XX:ParallelGCThreads。

-XX:ParallelGCThreads也可以通过参数设置，默认值为0，如果没有设置，G1也可以自己推断出来：

- 当cpu内核的个数小于等于8时，ParallelGCThreads的值是：
- 当cpu内核的个数大于8时，ParallelGCThreads的值是：8+(cpu内核的个数-8)*5/8

在绿区的时候，Refine线程会根据DCQS数值的大小启动不同数量的Refine线程，参数-XX:G1ConcRefinementThresholdStep用于控制每个Refine线程消费队列的步长，如果不设置，可以自动推断。
