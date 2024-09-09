# 令牌桶算法

令牌桶算法以一个指定的速率产生令牌并放入令牌桶，每次用户请求到来时会从桶里拿走一个令牌，如果桶内没有令牌可拿，则拒绝请求。

```java
public class TokenBucketLimiter {

    /**
     * 令牌
     */
    public static final String TOKEN = "token";
    /**
     * 令牌桶容量
     */
    private static final int limit = 10;
    /**
     * 令牌的产生间隔时间 单位: 毫秒
     */
    private static final int period = 1000;
    /**
     * 令牌每次产生的个数
     */
    private static final int amount = 2;
    /**
     * 阻塞队列 用于存放令牌
     */
    private static final ArrayBlockingQueue<String> blockingQueue = new ArrayBlockingQueue<>(limit);
    ;

    /**
     * 生产令牌
     */
    public static void start() {
        new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(period);
                    for (int i = 0; i < amount; i++) {
                        blockingQueue.put(TOKEN);
                    }
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        }).start();
    }

    private static boolean sendRequest() {
        // 获取令牌
        return blockingQueue.poll() != null;
    }

    public static void main(String[] args) {
        start();
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
