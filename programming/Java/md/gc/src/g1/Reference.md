# Reference

引用类型都直接或间接继承了 Reference 类。

```java
public abstract class Reference<T> {
    // 引用类型包裹的对象
    private T referent;

    // 引用队列(单向链表)
    // queue中使用head字段存储链表的头节点
    volatile ReferenceQueue<? super T> queue;

    // 当前reference处于不同个状态时, 取值不同:
    // Active: null
    // Pending: this
    // Enqueued: 指向ReferenceQueue的下一个节点
    // Inactive: this
    volatile Reference next;

    // Pending队列(单向链表), 全局唯一
    // pending为链表的头节点
    private static Reference<Object> pending = null;

    // 当前reference处于不同个状态时, 取值不同:
    // Active: 指向discovered list中的下一个节点, discovered list由JVM内部使用
    // Pending: 指向Pending队列的下一个节点
    // 其他状态: null
    transient private Reference<T> discovered;

    // lock是Pending队列的全局锁
    static private class Lock { }
    private static Lock lock = new Lock();

    Reference(T referent) {
        this(referent, null);
    }

    Reference(T referent, ReferenceQueue<? super T> queue) {
        this.referent = referent;
        this.queue = (queue == null) ? ReferenceQueue.NULL : queue;
    }
}
```

引用中用到了两个队列: Pending 队列和 ReferenceQueue 队列。

Pending 队列是由 JVM 构建的，当一个对象除了被 Reference 引用之外没有其它的强引用时，JVM 就会将这个对象回收, 并把指向需要回收的对象的 Reference 放入到这个队列里面。

Pending 队列会由 ReferenceHandler 线程来处理, ReferenceHandler 线程是 JVM 的一个内部线程，它也是 Reference 的一个内部类，它会将 Pending 队列中要被回收的 Reference 对象移出队列，如果 Reference 对象在初始化的时候传入了 ReferenceQueue 队列，那么就把这个移出的 Reference 对象放到它自己的 ReferenceQueue 队列里，如果没有传入 ReferenceQueue 队列，那么其关联的对象就不会进入到 Pending 队列中，会直接被回收掉。

```java
public class Test {
    public static void main(String[] args) throws InterruptedException {
        Object o = new Object();
        ReferenceQueue<Object> q = new ReferenceQueue<>();
        WeakReference<Object> ref = new WeakReference<>(o, q);
        o = null;
        System.out.println("GC前: ");
        System.out.println(ref);
        System.out.println(ref.get());
        System.gc();
        // 等待ReferenceHandler线程处理完成
        Thread.sleep(100);
        Reference<?> reference = q.poll();
        if (reference != null) {
            System.out.println("对象o被回收");
            System.out.println(reference);
            System.out.println(ref.get());
        }
    }
}
// 输出:
/*
GC前:
java.lang.ref.WeakReference@75b84c92
java.lang.Object@6bc7c054
对象o被回收
java.lang.ref.WeakReference@75b84c92
null
*/
```

ReferenceQueue 用于决定 Reference 引用的对象被回收时，Reference 对象能否进入到 Pending 队列。最终由 ReferenceHandler 线程处理后，Reference 就被放到了这个队列里面，用户可以从 ReferenceQueue 里拿到 reference,执行自定义操作，所以这个队列起到一个对象被回收时通知的作用。

如果不带 ReferenceQueue 的话,要想知道 Reference 持有的对象是否被回收，就只有不断地轮询 Reference 对象, 判断 get() 方法返回的对象是否为 null(虚引用不能这样做,其 get 始终返回 null,因此它只有带 queue 的构造函数)。

如果传入的 ReferenceQueue 队列为 null，那么就会给 queue 字段赋值为 ReferenceQueue.NULL,这个 NULL 是 ReferenceQueue 对象的一个内部类，它重写了入队方法 enqueue()，这个方法只有一个操作，直接返回 false，也就是这个对列不会存取任何数据, 它起到状态标记的作用。

```java
public class ReferenceQueue<T> {

    private static class Null<S> extends ReferenceQueue<S> {
        boolean enqueue(Reference<? extends S> r) {
            return false;
        }
    }

    static ReferenceQueue<Object> NULL = new Null<>();
}
```

## Reference 状态及转换

- Active: 活动状态, referent 对象存在强引用状态, 还没有被回收
- Pending: 垃圾回收器将 Reference 对象放入到 Pending 队列中，等待 ReferenceHandler 线程处理。如果没有指定 ReferenceQueue, 则直接变为 Inactive 状态
- Enqueued: ReferenceHandler 线程将 Pending 队列中的对象取出来放到 ReferenceQueue 队列中
- Inactive: 处于此状态的 Reference 对象可以被回收, 并且其内部的 referent 对象也可以被回收

Reference 对象的状态要通过字段 next 和 queue 来判断:

- Active: next == null
- Pending: next == this && queue == 构造方法中传入的 ReferenceQueue
- Enqueued: queue == ReferenceQueue.ENQUEUED
- Inactive: next == this && queue == ReferenceQueue.NULL
