# interrupt 方法

```java
public class Tester {

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            while (true) {
                // 中断标志位
                boolean interrupted = Thread.currentThread().isInterrupted();
                // 判断中断标志位, 如果为true, 则退出循环
                if (interrupted) break;
                System.out.println("Thread is running");
            }
        });

        t1.start();
        Thread.sleep(1000);
        // 中断线程, 实际上是设置线程的中断标志位, 并不会真正中断线程
        t1.interrupt();
    }
}
```

## 中都拿正在阻塞的线程

```java
public class Tester {

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });

        t1.start();
        Thread.sleep(1000);
        // 中断正在阻塞的线程, 会唤醒线程, 并抛出InterruptedException异常
        t1.interrupt();
    }
}
```
