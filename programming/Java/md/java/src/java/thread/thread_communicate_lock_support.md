# LockSupport

park 阻塞线程, unpark 唤醒线程。

```java
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.locks.LockSupport;

public class Demo {
    public static void main(String[] args) {
        // 共享资源
        List<String> list = new ArrayList<>();

        // 线程B
        Thread threadB = new Thread(() -> {
            if (list.isEmpty()) {
                // 等待A线程唤醒
                LockSupport.park();
            }
            for (String s : list) {
                System.out.println(s);
            }
        });

        // 线程A
        new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ignored) {
            }
            list.add("来自线程A");
            // 唤醒B线程
            LockSupport.unpark(threadB);
        }).start();


        threadB.start();
    }
}
```
