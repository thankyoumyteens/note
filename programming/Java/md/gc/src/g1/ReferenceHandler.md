# ReferenceHandler

ReferenceHandler 线程的作用是: 在 GC 结束后，当 pending 队列不为空的时候，循环将 pending 队列里面 Reference 取出，放入到它自己的 ReferenceQueue 里面。

```java
public abstract class Reference<T> {
    private static class ReferenceHandler extends Thread {

        private static void ensureClassInitialized(Class<?> clazz) {
            try {
                Class.forName(clazz.getName(), true, clazz.getClassLoader());
            } catch (ClassNotFoundException e) {
                throw (Error) new NoClassDefFoundError(e.getMessage()).initCause(e);
            }
        }

        static {
            ensureClassInitialized(InterruptedException.class);
            ensureClassInitialized(Cleaner.class);
        }

        ReferenceHandler(ThreadGroup g, String name) {
            super(g, name);
        }

        public void run() {
            while (true) {
                tryHandlePending(true);
            }
        }
    }

    static boolean tryHandlePending(boolean waitForNotify) {
        Reference<Object> r;
        // Cleaner是JDk 9之后提供的一个对象清理操作类
        // 主要的功能是替代finialize()方法
        // Cleaner也是Reference的子类
        Cleaner c;
        try {
            // pending是全局唯一的, 修改前需要加锁
            synchronized (lock) {
                if (pending != null) {
                    r = pending;
                    // 当前节点是Cleaner对象, 赋值给c
                    c = r instanceof Cleaner ? (Cleaner) r : null;
                    // pending指向链表的下一个节点
                    pending = r.discovered;
                    // 把当前节点移出链表
                    r.discovered = null;
                } else {
                    // 锁被其他线程占用, 等待
                    if (waitForNotify) {
                        lock.wait();
                    }
                    // 下次循环重试
                    return waitForNotify;
                }
            }
        } catch (OutOfMemoryError x) {
            Thread.yield();
            // 下次循环重试
            return true;
        } catch (InterruptedException x) {
            // 下次循环重试
            return true;
        }

        if (c != null) {
            // 执行Cleaner对象的clean()方法
            c.clean();
            return true;
        }
        // 把这个引用对象放到ReferenceQueue中
        ReferenceQueue<? super Object> q = r.queue;
        if (q != ReferenceQueue.NULL) q.enqueue(r);
        return true;
    }
}
```
