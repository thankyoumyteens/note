# 线程池

## 线程池的核心参数

```java
public ThreadPoolExecutor(int corePoolSize,
                          int maximumPoolSize,
                          long keepAliveTime,
                          TimeUnit unit,
                          BlockingQueue<Runnable> workQueue,
                          ThreadFactory threadFactory,
                          RejectedExecutionHandler handler);
```

- 核心线程数(corePoolSize)：线程池中始终保持的线程数量，即使它们处于空闲状态
- 最大线程数(maximumPoolSize)：线程池中允许的最大线程数量
- 保持活动时间(keepAliveTime)：非核心线程(建临时线)空闲时在终止前等待新任务的最长时间
- 时间单位(unit)：保持活动时间的时间单位
- 工作队列(workQueue)：当没有空闲的核心线程时, 用于存放新来的待执行任务的阻塞队列
- 线程工厂(threadFactory)：用于定制线程对象的创建
- 拒绝策略(handler)：当任务太多，无法被线程池及时处理时，采取的策略

## 线程池的执行原理

1. 一开始, 线程池会创建 corePoolSize 个线程来执行任务
2. 当任务的数量超过 corePoolSize 时, 后续的任务将会进入 workQueue 排队
3. 当 workQueue 也满了之后, 线程池会继续创建临时线程来执行新到的任务, 线程池中的线程总数不会超过 maximumPoolSize
4. 如果新到的任务处理完成, 临时线程会继续处理 workQueue 中排队的任务, 如果临时线程线程在空闲状态(任务都处理完了)超过 keepAliveTime, 就会被自动销毁
5. 当工作线程的数量到达 maximumPoolSize, 且 workQueue 还是满的时侯, 将根据设置的拒绝策略处理新到的任务

## 常用的拒绝策略

- AbortPolicy: 丢弃任务, 并抛出 RejectedExecutionException 异常
- CallerRunsPolicy: 哪个线程发起的任务, 哪个线程自己去执行这个任务
- DiscardOldestPolicy: 丢弃 workQueue 中最老的一个任务, 并将新任务加入
- DiscardPolicy: 直接丢弃任务, 不做任何操作
