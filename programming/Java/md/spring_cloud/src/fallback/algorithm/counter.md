# 计数器算法

在一段时间间隔内(时间窗/时间区间)，处理请求的最大数量固定，超过部分不做处理。

缺点: 如果在时间 00:59 时，瞬间发送了 100 个请求，并且 01:00 时又瞬间发送了 100 个请求，那么其实在 1 秒中，瞬间发送了 200 个请求。用户通过在时间窗口的重置节点处突发请求，可以突破限制。

```java
public class CounterLimiter {

    // 起始时间
    private static long startTime = System.currentTimeMillis();
    // 请求数量计数器
    private static final AtomicInteger accumulator = new AtomicInteger();

    private static final Object lock = new Object();

    private static boolean sendRequest() {
        // 时间区间: 1秒
        long interval = 1000;
        // 每个时间区间的最大请求数量
        long maxCount = 2;

        long now = System.currentTimeMillis();
        if (now < startTime + interval) {
            // 在时间区间之内
            int count = accumulator.incrementAndGet();
            return count <= maxCount;
        } else {
            // 在时间区间之外
            synchronized (lock) {
                // 再一次判断，防止重复初始化
                if (now >= startTime + interval) {
                    accumulator.set(0);
                    startTime = now;
                }
            }
            return true;
        }
    }

    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                if (sendRequest()) {
                    System.out.println("Send request successfully");
                } else {
                    System.out.println("Send request failed");
                }
            }).start();
            try {
                Thread.sleep(300);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
```
