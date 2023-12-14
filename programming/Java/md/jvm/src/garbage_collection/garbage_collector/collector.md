# 垃圾回收器

垃圾回收器(Garbage Collector)主要的作用是自动回收程序不再使用的内存空间, 以减少程序员管理内存的负担, 提高程序设计的效率。

衡量垃圾回收器的三项最重要的指标:

1. 内存占用(Footprint)
2. 吞吐量(Throughput)
3. 延迟(Latency)

三者总体的表现会随技术进步而越来越好, 但是要在这三个方面同时兼顾是不可能的, 一款回收器通常最多可以同时达成其中的两项。

低延迟垃圾回收器(Low-Latency Garbage Collector 或者 Low-Pause-Time Garbage Collector)是一种以降低垃圾回收的延迟为主要目标的垃圾回收器。
