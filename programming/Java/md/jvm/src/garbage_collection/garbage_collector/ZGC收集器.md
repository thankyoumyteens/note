# ZGC收集器

ZGC(Z Garbage Collector)是一款在JDK 11中新加入的由Oracle公司研发的具有实验性质的低延迟垃圾收集器。ZGC的设计目标是在尽可能对吞吐量影响不太大的前提下，实现在任意堆内存大小下都可以把垃圾收集的停顿时间限制在十毫秒以内的低延迟。

ZGC也采用基于Region的堆内存布局，但不同的是，ZGC的Region可以动态创建和销毁，以及动态的区域容量大小。在x64硬件平台下，ZGC的Region可以具有大、中、小三类容量：

- 小型Region(Small Region)：容量固定为2MB，用于放置小于256KB的小对象
- 中型Region(Medium Region)：容量固定为32MB，用于放置大于等于256KB但小于4MB的对象
- 大型Region(Large Region)：容量不固定，可以动态变化，但必须为2MB的整数倍，用于放置4MB或以上的大对象。每个大型Region中只会存放一个大对象，虽然名字叫作大型Region，但它的实际容量完全有可能小于中型Region，最小容量可低至4MB。大型Region在ZGC的实现中是不会被重分配的，因为复制一个大对象的代价非常高昂

![](../../img/zgc_region.jpeg)

