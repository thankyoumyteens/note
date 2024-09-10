# 漏桶算法

漏桶算法限流的基本原理：水(对应请求)从进水口进入到漏桶里，漏桶以一定的速度出水(请求放行)，当水流入速度过大，桶内的总水量大于桶容量会直接溢出，请求被拒绝。

缺点: 漏桶出口的速度固定，不能灵活的应对后端能力提升。

```java
public class LeakBucketLimiter {

    // 桶的容量
    public static long capacity = 2;
    // 当前水量
    public static long water = 0;
    // 水流速度/s
    public static long rate = 1;
    // 最后一次加水时间
    public static long lastTime = System.currentTimeMillis();

    private static boolean sendRequest() {
        long now = System.currentTimeMillis();
        // 计算当前流出的水量, 速度 * 时间
        long l = (now - lastTime) / 1000 * rate;
        // 桶中剩余的水量
        water = Math.max(0, (water - l));

        if (capacity - water < 1) {
            // 若桶满,则拒绝
            return false;
        } else {
            // 还有容量, 则加水
            water += 1;
            // 更新最后一次加水时间
            lastTime = now;
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
