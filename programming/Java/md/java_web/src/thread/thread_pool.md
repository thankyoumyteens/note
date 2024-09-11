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

## 常用的阻塞队列

- ArrayBlockingQueue: 基于数组实现的有界阻塞队列(创建时必须指定容量), 按照先进先出原则对元素进行排序。ArrayBlockingQueue 使用同一个锁来控制入队和出队
- LinkedBlockingQueue: 基于链表实现的有界阻塞队列, 但它的容量默认为 `Integer.MAX_VALUE`, 是一个非常大的值, 也可以认为是无界队列。LinkedBlockingQueue 采用了两个独立的锁来分别控制入队和出队, 队列的并发性能更高
- PriorityBlockingQueue: 支持优先级的无界队列, 元素在默认情况下采用自然顺序升序排列。可以自定义实现 compareTo 方法来指定元素的排序规则
- SynchronousQueue: 不存储元素的阻塞队列。每个 put 操作都必须等待一个 take 操作完成, 否则不能继续添加元素
- DelayQueue: 支持延时获取元素的无界阻塞队列

## 确定核心线程数

程序分为两种:

1. IO 密集型任务: 比如文件读写, 网络请求, 数据库读写
2. CPU 密集型任务: 比如计算型代码, 复杂的算法

设置核心线程数:

1. IO 密集型任务: 核心线程数为 `2n + 1`, n 是 CPU 的核心数。多开一些线程来处理 IO 请求
2. CPU 密集型任务: 核心线程数为 `n + 1`, n 是 CPU 的核心数。减少线程的切换来增加效率
