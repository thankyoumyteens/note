# Mixed GC

Mixed GC 可以分为两个阶段：

1. 并发标记：目的是识别老年代 region 中的活跃对象，并计算 region 中垃圾对象所占空间的多少，用于垃圾回收过程中判断是否回收这个 region
2. 垃圾回收：这个过程和 Young GC 的步骤完全一致，重用了 Young GC 的代码，最大的不同是在回收时不仅仅回收新生代 region，同时回收并发标记中识别到的垃圾多的老年代 region
