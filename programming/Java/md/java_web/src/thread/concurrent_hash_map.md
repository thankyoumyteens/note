# ConcurrentHashMap

## JDK1.7 及以前

ConcurrentHashMap 由 Segment 数组组成, 每个 Segment 又包含一个 HashEntry 数组, 数组中的每一个 HashEntry 既是一个键值对, 也是一个链表的头节点。

ConcurrentHashMap 定位一个元素的过程需要进行两次 Hash 操作。第一次 Hash 定位到 Segment, 第二次 Hash 定位到元素所在的链表的头部。

ConcurrentHashMap 使用分段锁技术, 将数据分成一段一段的存储(Segment 数组), 然后给每一段数据配一把锁(ReentrantLock), 当一个线程占用锁访问其中一个段的时候, 其他段的数据也能被其他线程访问, 在保证线程安全的同时降低了锁的粒度, 让并发操作效率更高。

## JDK1.8

去除 Segment+HashEntry 的实现, 改为 HashMap 搭配 Synchronized+CAS 的实现。用 Synchronized+CAS 代替 Segment, 这样锁的粒度更小了(只会锁住链表/红黑树的头节点), 并且不是每次都要加锁, 只有 CAS 尝试失败了再加锁。
