# FinalReference

FinalReference 确保对象在垃圾回收器回收它们之前, 可以有最后的机会来释放它们所持有的资源。它通过将对象包装在一个 Finalizer 对象中来实现。当一个对象被标记为准备回收, 且它是一个 Finalizable 类(即它有一个空的、参数为 void 的、名为 finalize 的方法)的时候, JVM 会创建一个 FinalReference 指向这个对象。然后, JVM 会创建一个 Finalizer 线程来执行这个对象的 finalize 方法。在 finalize 方法中, 对象可以释放它所持有的所有资源。

```java
class FinalReference<T> extends Reference<T> {

    public FinalReference(T referent, ReferenceQueue<? super T> q) {
        super(referent, q);
    }

    @Override
    public boolean enqueue() {
        throw new InternalError("should never reach here");
    }
}
```

## Finalizer

Finalizer 的构造方法是私有的, 是由 JVM 自己来创建。JVM 会主动调用 Finalizer 的 register 方法, 同时将这个 Finalizer 对象加入到 Finalizer 对象链表里, Finalizer 的类变量 unfinalized 指向这个链表的头节点。

JVM 在创建一个对象 a 的过程中会判断这个对象是否重写了 finalize() 方法, 且方法体不为空, 如果符合要求, JVM 就会调用 register 方法, 创建一个引用对象 a 的 Finalizer 对象 f, 并把 f 加入到链表中, 对象 a 此时被 f 引用, f 又被一个静态链表引用, 所以在 f 被移出链表之前, a 不会被垃圾回收。

```java
final class Finalizer extends FinalReference<Object> {
    // 引用队列
    private static ReferenceQueue<Object> queue = new ReferenceQueue<>();
    // 全局唯一的Finalizer对象的链表
    // 这个链表中的Finalizer节点都引用的是
    // 重写了finalize()方法, 且finalize()方法还没被调用的对象
    private static Finalizer unfinalized = null;
    // 用于unfinalized的锁
    private static final Object lock = new Object();

    private Finalizer
        next = null,
        prev = null;
    // next指向自己, 表示已经调用过finalize()方法了
    private boolean hasBeenFinalized() {
        return (next == this);
    }
    // 把Finalizer对象加入链表
    private void add() {
        synchronized (lock) {
            if (unfinalized != null) {
                this.next = unfinalized;
                unfinalized.prev = this;
            }
            unfinalized = this;
        }
    }
    // 把Finalizer对象移出链表
    private void remove() {
        synchronized (lock) {
            if (unfinalized == this) {
                if (this.next != null) {
                    unfinalized = this.next;
                } else {
                    unfinalized = this.prev;
                }
            }
            if (this.next != null) {
                this.next.prev = this.prev;
            }
            if (this.prev != null) {
                this.prev.next = this.next;
            }
            this.next = this;   /* Indicates that this has been finalized */
            this.prev = this;
        }
    }
    // 构造方法
    private Finalizer(Object finalizee) {
        super(finalizee, queue);
        // 把自己加入链表
        add();
    }

    static ReferenceQueue<Object> getQueue() {
        return queue;
    }

    // 给JVM调用
    static void register(Object finalizee) {
        new Finalizer(finalizee);
    }
}
```

## 执行 finalize() 方法

当对象 a 要被回收时, JVM 会把 Finalizer 对象 f 加入 pending_list, 接下来 ReferenceHandler 线程会把 f 从 pending_list 转移到 ReferenceQueue 队列。Finalizer 类在加载的时候会启动一个 FinalizerThread 线程来处理 ReferenceQueue 中的 Finalizer 对象。

```java
final class Finalizer extends FinalReference<Object> {

    static {
        // 类加载时启动FinalizerThread线程
        ThreadGroup tg = Thread.currentThread().getThreadGroup();
        for (ThreadGroup tgn = tg;
             tgn != null;
             tg = tgn, tgn = tg.getParent());
        Thread finalizer = new FinalizerThread(tg);
        finalizer.setPriority(Thread.MAX_PRIORITY - 2);
        finalizer.setDaemon(true);
        finalizer.start();
    }

    // FinalizerThread线程
    private static class FinalizerThread extends Thread {
        private volatile boolean running;
        FinalizerThread(ThreadGroup g) {
            super(g, "Finalizer");
        }
        public void run() {
            // 避免递归调用
            if (running)
                return;

            // 等待JVM初始化完成
            while (!VM.isBooted()) {
                try {
                    VM.awaitBooted();
                } catch (InterruptedException x) {
                    // ignore and continue
                }
            }
            final JavaLangAccess jla = SharedSecrets.getJavaLangAccess();
            running = true;
            // 循环从ReferenceQueue里取Finalizer对象
            for (;;) {
                try {
                    // 从ReferenceQueue中取出
                    Finalizer f = (Finalizer)queue.remove();
                    // 调用finalize()方法
                    f.runFinalizer(jla);
                } catch (InterruptedException x) {
                    // ignore and continue
                }
            }
        }
    }

    // 调用finalize()方法
    private void runFinalizer(JavaLangAccess jla) {
        // 从链表中移出Finalizer对象
        synchronized (this) {
            if (hasBeenFinalized()) return;
            remove();
        }
        try {
            // 获取Finalizer对象引用的对象a
            Object finalizee = this.get();
            if (finalizee != null && !(finalizee instanceof java.lang.Enum)) {
                // 调用对象a的finalize()方法
                jla.invokeFinalize(finalizee);
                // 删除对象a的引用, 此时对象a可以被回收了
                finalizee = null;
            }
        } catch (Throwable x) { }
        super.clear();
    }

    // 可以通过
    // Runtime.getRuntime().runFinalization();
    // 手动调用
    static void runFinalization() {
        if (!VM.isBooted()) {
            return;
        }

        forkSecondaryFinalizer(new Runnable() {
            private volatile boolean running;
            public void run() {
                // in case of recursive call to run()
                if (running)
                    return;
                final JavaLangAccess jla = SharedSecrets.getJavaLangAccess();
                running = true;
                for (;;) {
                    Finalizer f = (Finalizer)queue.poll();
                    if (f == null) break;
                    f.runFinalizer(jla);
                }
            }
        });
    }
}
```
