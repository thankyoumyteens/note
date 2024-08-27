# synchronized

通过保证多个线程互斥访问临界区（共享存储）, 使用 `wait`, `notify`, `notifyAll` 方法来实现线程间的通信。

wait 用于在一个已经进入了同步锁的线程内，让自己暂时让出锁，以便其他正在等待此锁的线程可以得到锁并运行，当前线程必须拥有此对象的锁，才能调用某个对象的 wait 方法能让当前线程阻塞。调用某个对象的 wait 方法后, 会释放此对象的锁。

调用某个对象的 notify 方法能够唤醒一个正在等待这个对象的锁的线程，如果有多个线程都在等待这个对象的锁，则只能随机唤醒其中一个线程。notify 或者 notifyAll 方法并不是真正释放锁，必须等到 synchronized 语句块执行完才真正释放锁。

调用 notifyAll 方法能够唤醒所有正在等待这个对象的锁的线程，唤醒的线程获得锁的概率是随机的，取决于 cpu 调度。

```java
import java.util.ArrayList;
import java.util.List;

public class Demo {
    public static void main(String[] args) {
        // 锁对象
        Object lock = new Object();
        // 共享资源
        List<String> list = new ArrayList<>();

        // 线程A
        new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ignored) {
            }
            synchronized (lock) {
                list.add("来自线程A");
                // 唤醒B线程
                lock.notify();
            }
        }).start();

        // 线程B
        new Thread(() -> {
            synchronized (lock) {
                if (list.isEmpty()) {
                    try {
                        // 释放锁, 等待A线程唤醒
                        lock.wait();
                    } catch (InterruptedException ignored) {
                    }
                }
                for (String s : list) {
                    System.out.println(s);
                }
            }
        }).start();
    }
}
```

以下是 wait() 方法的一些关键点:

1. 释放锁: 线程在调用 wait() 方法时, 必须首先拥有该对象的锁。调用 wait() 后, 线程会释放锁, 并等待其他线程调用相同对象的 notify() 或 notifyAll() 方法
2. 进入等待池: 放弃锁后, 线程会进入与该对象关联的等待池中等待
3. 响应通知: 当其他线程调用了 notify() 或 notifyAll() 方法后, 等待池中的线程会被唤醒。notify() 唤醒等待池中的一个线程, 而 notifyAll() 唤醒所有等待的线程
4. 重新竞争锁: 被唤醒的线程需要重新竞争获取锁。只有成功获取到锁之后, 线程才能继续执行 wait() 方法之后的代码
5. 等待和超时: wait() 方法还可以带有一个超时参数, 例如 wait(long timeout)。如果指定了超时时间, 线程会在超时后自动醒来, 即使没有收到通知
6. InterruptedException: 在等待过程中, 如果线程被中断, wait() 方法会抛出 InterruptedException 异常, 并且线程的中断状态会被清除
