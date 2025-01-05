# 锁升级

在 mark word 中, 锁标志位占用 2 个 bit, 结合 1bit 的是否偏向锁标志位, 就能用来标识当前对象持有的锁的状态。

```java
public class DemoObj {

    public static void main(String[] args) {
        DemoObj obj = new DemoObj();
        System.out.println(ClassLayout.parseInstance(obj).toPrintable());
    }
}
```

## 无锁

对象处于无锁状态时, mark word 为 0x0000000000000001:

```java
demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x0000000000000001 (non-biasable; age: 0)
  8   4        (object header: class)    0xf800c146
 12   4        (object alignment gap)
Instance size: 16 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total
```

## 偏向锁

在 JVM 启动后 4 秒后创建的对象才会开启偏向锁, 可以使用参数 -XX:BiasedLockingStartupDelay=0 取消这个延迟时间。开启偏向锁后, mark word 变为 0x0000000000000005(最后 3 位是 101):

```java
demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x0000000000000005 (biasable; age: 0)
  8   4        (object header: class)    0xf800c105
 12   4        (object alignment gap)
Instance size: 16 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total
```

在没有线程竞争的条件下, 第一个获取锁的线程通过 CAS 将自己的线程 Id 写入到该对象的 mark word 中, 若后续该线程再次获取锁, 需要比较当前线程 Id 和对象 mark word 中的线程 Id 是否一致, 如果一致那么可以直接获取, 并且锁对象始终保持对该线程的偏向, 也就是说偏向锁不会主动释放。

```java
public class DemoObj {

    public static void main(String[] args) throws InterruptedException {
        // 等待JVM开启偏向锁
        Thread.sleep(5000);
        DemoObj obj = new DemoObj();
        synchronized (obj) {
            System.out.println(ClassLayout.parseInstance(obj).toPrintable());
        }
        synchronized (obj) {
            System.out.println(ClassLayout.parseInstance(obj).toPrintable());
        }
    }
}
```

输出:

```java
demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x000001d2db13e805 (biased: 0x0000000074b6c4fa; epoch: 0; age: 0)
  8   4        (object header: class)    0xf800c105
 12   4        (object alignment gap)
Instance size: 16 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total

demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x000001d2db13e805 (biased: 0x0000000074b6c4fa; epoch: 0; age: 0)
  8   4        (object header: class)    0xf800c105
 12   4        (object alignment gap)
Instance size: 16 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total
```

mark word 中的 0x1d2db13e 就是当前线程的 Id。

## 轻量级锁

当两个或以上线程交替获取锁, 但并没有在对象上并发的获取锁时, 偏向锁升级为轻量级锁。线程采取 CAS 的自旋方式尝试获取锁。

```java
public class DemoObj {

    public static void main(String[] args) throws InterruptedException {
        // 等待JVM开启偏向锁
        Thread.sleep(5000);
        DemoObj obj = new DemoObj();
        synchronized (obj) {
            System.out.println(ClassLayout.parseInstance(obj).toPrintable());
        }
        Thread thread = new Thread(() -> {
            synchronized (obj) {
                System.out.println(ClassLayout.parseInstance(obj).toPrintable());
            }
        });
        thread.start();
        thread.join();
        System.out.println(ClassLayout.parseInstance(obj).toPrintable());
    }
}
```

输出:

```java
demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x000002cbd23cd805 (biased: 0x00000000b2f48f36; epoch: 0; age: 0)
  8   4        (object header: class)    0xf800c105
 12   4        (object alignment gap)
Instance size: 16 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total

demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x000000f2cc4fefa0 (thin lock: 0x000000f2cc4fefa0)
  8   4        (object header: class)    0xf800c105
 12   4        (object alignment gap)
Instance size: 16 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total

demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x0000000000000001 (non-biasable; age: 0)
  8   4        (object header: class)    0xf800c105
 12   4        (object alignment gap)
Instance size: 16 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total
```

1. 首先进入偏向锁, mark word 为 0x000002cbd23cd805
2. thread 线程自旋等待主线程释放锁后获得锁, 并把锁升级成轻量级锁, mark word 为 0x000000f2cc4fefa0
3. thread 线程释放锁后, obj 无线程竞争, 恢复为无锁。如果之后有线程再尝试获取 user 对象的锁, 会直接加轻量级锁, 而不是偏向锁

## 重量级锁

当两个或以上线程并发的在同一个对象上进行同步时, 为了避免无用自旋消耗 cpu, 轻量级锁会升级成重量级锁。

```java
public class DemoObj {

    public static void main(String[] args) throws InterruptedException {
        // 等待JVM开启偏向锁
        Thread.sleep(5000);
        DemoObj obj = new DemoObj();

        new Thread(() -> {
            synchronized (obj) {
                try {
                    System.out.println(ClassLayout.parseInstance(obj).toPrintable());
                    // 等待另一个线程来竞争锁
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        }).start();
        new Thread(() -> {
            synchronized (obj) {
                try {
                    System.out.println(ClassLayout.parseInstance(obj).toPrintable());
                    // 等待另一个线程来竞争锁
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        }).start();
    }
}
```

输出:

```java
demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x000002927e4e440a (fat lock: 0x000002927e4e440a)
  8   4        (object header: class)    0xf800c105
 12   4        (object alignment gap)
Instance size: 16 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total

demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x000002927e4e440a (fat lock: 0x000002927e4e440a)
  8   4        (object header: class)    0xf800c105
 12   4        (object alignment gap)
Instance size: 16 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total
```

在两个线程同时竞争锁时, 会升级为重量级锁, mark word 为 0x000002927e4e440a, 最后两位是 10。

## Lock Record

Lock Record 用于偏向锁优化和轻量级锁优化。它保存 mark word 的原始值, 还包含识别锁对象所必需的元数据。

jvm 中对应的代码:

```cpp
class BasicObjectLock {
 private:
  BasicLock _lock; // mark word 的原始值
  oop       _obj; // 持有锁的对象
};


class BasicLock {
 private:
  volatile markOop _displaced_header;
};
```

当字节码解释器执行 monitorenter 字节码轻量地锁住一个对象时, 就会在获取锁的线程的栈上显式或隐式分配一个 lock record。同一个线程重入同一个锁的话, 会创建多个 lock record(只有最早的一个 lock record 会记录 mark word 的原始值, 但它们的 `_obj` 都会指向这个对象)。
