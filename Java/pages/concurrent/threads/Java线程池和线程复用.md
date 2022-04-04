# ThreadPoolExecutor

java中的线程池的使用是通过调用ThreadPoolExecutor来实现的。

```java
public ThreadPoolExecutor(int corePoolSize,
                          int maximumPoolSize,
                          long keepAliveTime,
                          TimeUnit unit,
                          BlockingQueue<Runnable> workQueue,
                          ThreadFactory threadFactory,
                          RejectedExecutionHandler handler)
```

- corePoolSize：该线程池中核心线程的数量
- maximumPoolSize：该线程池中线程总数的最大值
- keepAliveTime：当线程数量超过corePoolSize时，空闲线程的存活时间
- unit：keepAliveTime的单位
- workQueue：任务队列，维护着等待执行的任务（Runnable对象）
- threadFactory：创建线程的接口
- RejectedExecutionHandler：任务拒绝策略

# 线程池的工作流程

![](img/Screenshot_20220313_185217.jpg)

判断线程池中的线程数是否小于核心线程数（用户自定义），若小于核心线程数，线程池会新建线程并执行任务。随着任务的增多，线程池中的线程数会慢慢增加至核心线程数。如果此时还有任务提交，就会判断阻塞队列是否已满，若没满，则会将任务放入到阻塞队列中，等待获得工作线程并执行。如果任务提交非常多，使得阻塞队列达到上限，会去判断线程数是否小于最大线程数，若小于最大线程数，线程池会创建非核心线程线程去执行任务。如果仍然有大量任务提交，使得线程数等于最大线程数，如果此时还有任务提交，就会按照拒绝策略进行拒绝。

# 线程池的拒绝策略

- AbortPolicy：直接抛出异常，阻止线程正常运行
- CallerRunsPolicy：如果被丢弃的线程任务未关闭，则执行该线程任务，CallerRunsPolicy拒绝策略不会真的丢弃任务
- DiscardOldestPolicy：移除线程队列中最早的一个线程任务，并尝试提交当前任务
- DiscardPolicy：丢弃当前的线程任务而不做任何处理
- 自定义拒绝策略：实现RejectedExecutionHandler接口

# 实现线程复用

Thread.start()只能调用一次，一旦这个调用结束，则该线程就到了stop状态，不能再次调用start。

则要达到复用的目的，只要将线程的run方法写成无限循环，不断检查任务队列中是否还有要执行的Runnable对象，有就直接调用它的run()方法。

```java
public void run() {
    while(true) {
        if(taskqueue.isNotEmpty()) {
           Runnable task = taskqueue.dequeue();
           task.run();
        }
    }
}
```
