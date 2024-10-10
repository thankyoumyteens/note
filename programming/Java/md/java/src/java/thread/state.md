# 线程的状态

Java 线程定义了 6 种状态, 线程在任何时刻只能处于其中一种状态。

- 新建(NEW): 线程已经创建(创建了 Thread 对象), 但还没有启动(没调用 start 方法)
- 运行(RUNNABLE): Java 的线程运行状态包括操作系统的线程状态中的就绪(Ready)和运行中(Running)两种状态, 也就是说, 处于此状态的线程有可能正在执行, 也可能正在等待操作系统为它分配时间片
- 无限期等待(WAITING)
- 超时等待(TIMED_WAITING)
- 阻塞(BLOCKED): 等待锁
- 终止(TERMINATED): 已经结束执行(run 方法执行完了)的线程

![](../../img/thread_state.png)
