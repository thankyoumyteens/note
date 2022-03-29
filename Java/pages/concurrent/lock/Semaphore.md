# Semaphore

Semaphore是一种基于计数的信号量。

在许可信号的竞争队列超过阈值后，新加入的申请许可信号的线程将被阻塞，直到有其他许可信号被释放。

```java
// 信号量初始化为3个
Semaphore sp = new Semaphore(3);
Thread thread=new Thread(new Runnable() {
    public void run() {
        try {
            // 占用1个信号量
            // 信号量不足时会阻塞
            semaphore.acquire();
            System.out.println();
            // 释放占用的信号量
            semaphore.release();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
});
thread.start();
```
