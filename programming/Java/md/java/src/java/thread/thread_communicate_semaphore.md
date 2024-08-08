# 信号量

信号量用来控制同时访问某个资源的线程数量。一个线程在进入公共资源时需要先获取一个许可, 如果获取不到许可则要等待其它线程释放许可, 每个线程在离开公共资源时都会释放许可。

信号量支持两种模式: 公平和非公平。非公平模式下, 信号量不保证线程获取许可的顺序。

```java
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Semaphore;
import java.util.concurrent.locks.LockSupport;

public class Demo {
    public static void main(String[] args) {
        // 公平模式信号量, 初始资源数为0
        Semaphore semaphore = new Semaphore(0, true);
        // 共享资源
        List<String> list = new ArrayList<>();

        // 线程B
        Thread threadB = new Thread(() -> {
            try {
                // 等待A线程增加资源
                semaphore.acquire();
                for (String s : list) {
                    System.out.println(s);
                }
            } catch (InterruptedException ignored) {
            }
        });

        // 线程A
        new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ignored) {
            }
            list.add("来自线程A");
            // 增加资源, 唤醒B线程
            semaphore.release();
        }).start();


        threadB.start();
    }
}
```
