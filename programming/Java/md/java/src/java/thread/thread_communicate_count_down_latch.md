# CountDownLatch

```java
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;

public class Demo3 {
    public static void main(String[] args) {
        // CountDownLatch
        CountDownLatch countDownLatch = new CountDownLatch(1);
        // 共享资源
        List<String> list = new ArrayList<>();

        // 线程A
        new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ignored) {
            }
            list.add("来自线程A");
            // 计数减到0, 唤醒B线程
            countDownLatch.countDown();
        }).start();

        // 线程B
        new Thread(() -> {
            if (list.isEmpty()) {
                try {
                    // 等待A线程把计数减到0
                    countDownLatch.await();
                } catch (InterruptedException ignored) {
                }
            }
            for (String s : list) {
                System.out.println(s);
            }
        }).start();
    }
}
```
