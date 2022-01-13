# try中有return时finally还会执行吗

try中有return, 会先将值暂存，无论finally语句中对该值做什么处理，最终返回的都是try语句中的暂存值。当try与finally语句中均有return语句，会忽略try中return。

# RabbitMQ六种消息模型

# 消息可靠性投递

# RabbitMQ集群架构模式

# RabbitMQ幂等性

# Redis缓存穿透缓存击穿缓存雪崩

# Redis持久化 AOF RDB

# # Redis哨兵

# Redis数据类型

# Redis缓存过期处理与内存淘汰机制

# Spring中的事务传播行为

# 接口幂等性

#  == 和 equals 的区别是什么

== 对基本类型是值比较，对引用类型是引用比较。equals 默认情况下是引用比较，只是 String、Integer 等类重写了 equals 方法，把它变成了值比较，所以一般情况下 equals 比较的是值是否相等。

# Math.round(-1.5) 等于多少

等于-1，因为在数轴上取值时是向右取整

# StringBuffer 和 StringBuilder 区别

StringBuffer 是线程安全的，而 StringBuilder 是非线程安全的，但 StringBuilder 的性能却高于 StringBuffer（因为stringbuffer加锁了），所以在单线程环境下推荐使用 StringBuilder，多线程环境下推荐使用 StringBuffer。

# String str="i"与 String str=new String("i")一样吗

不一样，因为内存的分配方式不一样。String str="i"的方式，Java 虚拟机会将其分配到常量池中（常量池保存在方法区中）；而 String str=new String("i") 则会被分到堆内存中。

# 如何将字符串反转？

使用 StringBuilder 或者 stringBuffer 的 reverse() 方法。

或者对撞指针
```java
void reverseString(char[] s) {
    int l = 0;
    int r = s.length - 1;
    while (l < r) {
        swap(s, l++, r--);
    }
}
void swap(char[] arr, int i, int j){
    char t = arr[i];
    arr[i] = arr[j];
    arr[j] = t;
}
```

# BIO、NIO、AIO 有什么区别

- BIO：Block IO 同步阻塞式 IO，就是我们平常使用的传统 IO，它的特点是模式简单使用方便，并发处理能力低。
- NIO：Non IO 同步非阻塞 IO，是传统 IO 的升级，客户端和服务器端通过 Channel（通道）通讯，实现了多路复用。
- AIO：Asynchronous IO 是 NIO 的升级，也叫 NIO2，实现了异步非堵塞 IO ，异步 IO 的操作基于事件和回调机制。

# HashMap 和 Hashtable 有什么区别？

- 存储：HashMap 运行 key 和 value 为 null，而 Hashtable 不允许。
- 线程安全：Hashtable 是线程安全的，而 HashMap 是非线程安全的。
- Hashtable 是保留类不建议使用，推荐在单线程环境下使用 HashMap 替代，多线程使用 ConcurrentHashMap 替代。

# 说一下 HashMap 的实现原理

HashMap 基于 Hash 算法实现的，我们通过 put(key,value)存储，get(key)来获取。当传入 key 时，HashMap 会根据 key. hashCode() 计算出 hash 值，根据 hash 值将 value 保存在 bucket 里。当计算出的 hash 值相同时，我们称之为 hash 冲突，HashMap 的做法是用链表和红黑树存储相同 hash 值的 value。当 hash 冲突的个数比较少时，使用链表否则使用红黑树。

# 说一下 HashSet 的实现原理

HashSet 是基于 HashMap 实现的，HashSet 底层使用 HashMap 来保存所有元素

# ArrayList 和 Vector 的区别是什么？

- 线程安全：Vector 使用了 Synchronized 来实现线程同步，是线程安全的，而 ArrayList 是非线程安全的。
- 性能：ArrayList 在性能方面要优于 Vector。（因为Synchronized）
- 扩容：ArrayList 和 Vector 都会根据实际的需要动态的调整容量，只不过在 Vector 扩容每次会增加 1 倍，而 ArrayList 只会增加 50%。

# 怎么确保一个集合不能被修改

可以使用 Collections. unmodifiableCollection(Collection c) 方法来创建一个只读集合，这样改变集合的任何操作都会抛出 Java. lang. UnsupportedOperationException 异常。

# 并行和并发有什么区别

- 并行：多个处理器或多核处理器同时处理多个任务。
- 并发：多个任务在同一个 CPU 核上，按细分的时间片轮流(交替)执行，从逻辑上来看那些任务是同时执行。

# 创建线程有哪几种方式？

- 继承 Thread 重写 run 方法；
- 实现 Runnable 接口；
- 实现 Callable 接口。

# runnable 和 callable 有什么区别？

runnable 没有返回值，callable 可以拿到返回值和捕获异常

# 线程的5种状态

- 新建(NEW)：新创建了一个线程对象。
- 可运行(RUNNABLE)：线程对象创建后，其他线程调用了该对象的start()方法。该状态的线程位于可运行线程池中，等待被线程调度选中，获取cpu 的使用权 。
- 运行(RUNNING)：可运行状态(runnable)的线程获得了cpu 时间片（timeslice） ，执行程序代码。
- 阻塞(BLOCKED)：阻塞状态是指线程因为某种原因放弃了cpu 使用权，也即让出了cpu timeslice，暂时停止运行。直到线程进入可运行(runnable)状态，才有机会再次获得cpu timeslice 转到运行(running)状态。
- 死亡(DEAD)：线程run()、main() 方法执行结束，或者因异常退出了run()方法，则该线程结束生命周期。死亡的线程不可再次复生。

