# Executor

java 提供了 Executor 接口用来管理线程池。

```java
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class Demo {

    public static void main(String[] args) throws InterruptedException {
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
                /* corePoolSize */ 2,
                /* maximumPoolSize */ 2,
                /* keepAliveTime */ 0,
                /* unit */ TimeUnit.MILLISECONDS,
                /* workQueue */ new LinkedBlockingQueue<>(),
                /*threadFactory*/ Thread::new,
                /*handler*/ new ThreadPoolExecutor.AbortPolicy()
        );

        executor.execute(() -> System.out.println("Hello, World!"));
        executor.execute(() -> System.out.println("Hello, World!"));
        executor.execute(() -> System.out.println("Hello, World!"));

        executor.close();
    }
}
```
