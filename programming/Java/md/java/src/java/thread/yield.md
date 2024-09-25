# yield 方法

yield 用于暗示线程调度器，当前线程愿意让出自己的 CPU 时间片给其他同优先级的线程。但是，这只是一个建议，线程调度器可以选择忽略这个建议, 即使调用了 yield，当前线程仍然可能立即重新获得 CPU 时间片。

```java
public class Tester {

    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 20; i++) {
                System.out.println("Thread 1: " + i);
                Thread.yield(); // 当前线程让出CPU时间片，但并不会释放锁
            }
        });

        t1.start();
    }
}
```
