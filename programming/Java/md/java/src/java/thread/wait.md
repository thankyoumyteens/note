# wait 方法

调用 wait 方法前需要先获取锁。

```java
public class Tester {

    public static final Object LOCK = new Object();

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            try {
                // 抛异常 java.lang.IllegalMonitorStateException: current thread is not owner
                // 调用wait方法的线程必须拥有这个对象的锁
                LOCK.wait();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });

        t1.start();
    }
}
```

调用 wait 方法后, 线程会释放对象的锁, 然后让出 CPU 资源, 使得其他线程可以执行。该线程进入等待状态, 直到其他线程调用相同对象的 notify 或 notifyAll 方法, 或者当前线程的 wait 方法被中断。

```java
public class Tester {

    public static final Object LOCK = new Object();

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            try {
                synchronized (LOCK) {
                    // 等待被唤醒
                    LOCK.wait();
                }
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });

        t1.start();
    }
}
```

## notify 方法

notify 方法与 wait 方法配合使用。当一个线程调用了某个对象的 wait 方法进入等待状态后, 另一个线程可以通过调用相同对象的 notify 方法来唤醒等待池中的第一个等待线程。被唤醒的线程会尝试重新获取对象锁, 如果成功获取到锁, 它将继续执行代码中的后续操作。

和 wait 一样, 调用 notify 方法前也需要先获取锁。

```java
public class Tester {

    public static final Object LOCK = new Object();

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            try {
                synchronized (LOCK) {
                    LOCK.wait();
                    // 被唤醒后需要重新获取LOCK对象的锁
                    // 获取到锁后才会继续执行
                    System.out.println("醒了");
                }
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });

        t1.start();
        Thread.sleep(1000);
        synchronized (LOCK) {
            LOCK.notify();
        }
    }
}
```

## notifyAll 方法

notifyAll 方法会唤醒在此对象监视器上等待的所有线程。所有在等待池中的线程都会被移动到锁池中, 它们将竞争重新获取对象锁的机会。
