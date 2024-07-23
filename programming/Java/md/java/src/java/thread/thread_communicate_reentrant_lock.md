# ReentrantLock/Condition 消息队列

通过保证多个线程互斥访问临界区（共享存储）, 使用 Condition 的 `await`, `signal`, `signalAll` 方法来实现线程间的通信。

```java
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

public class Demo2 {
    public static void main(String[] args) {
        // 锁对象
        ReentrantLock lock = new ReentrantLock();
        Condition condition = lock.newCondition();
        // 共享资源
        List<String> list = new ArrayList<>();

        // 线程A
        new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ignored) {
            }
            lock.lock();
            list.add("来自线程A");
            // 唤醒B线程
            condition.signal();
            lock.unlock();
        }).start();

        // 线程B
        new Thread(() -> {
            lock.lock();
            if (list.isEmpty()) {
                try {
                    // 释放锁, 等待A线程唤醒
                    condition.await();
                } catch (InterruptedException ignored) {
                }
            }
            for (String s : list) {
                System.out.println(s);
            }
            lock.unlock();
        }).start();
    }
}
```

以下是 Condition 和 await() 方法的一些关键点: 

1. 释放锁: 当一个线程调用 await() 方法时, 它会释放当前持有的锁, 并进入与 Condition 关联的等待池（condition waiting set）
2. 等待条件: 线程会等待直到其他线程调用相同 Condition 的 signal() 或 signalAll() 方法, 或者等待超时
3. 重新竞争锁: 当线程被 signal() 或 signalAll() 方法唤醒, 或者超时时, 它会重新尝试获取锁。只有成功获取锁后, 线程才能继续执行 await() 方法之后的代码
4. 超时: await() 方法可以带有一个超时参数, 例如 await(long timeout, TimeUnit unit)。如果指定了超时时间, 线程会在超时后自动醒来, 即使没有收到通知
5. InterruptedException: 在等待过程中, 如果线程被中断, await() 方法会抛出 InterruptedException 异常, 并且线程的中断状态会被清除
