# 线程的状态

Java 线程定义了 6 种状态, 线程在任何时刻只能处于其中一种状态。

- 新建(NEW): 线程已经创建(创建了 Thread 对象), 但还没有启动(没调用 start 方法)
- 终止(TERMINATED): 已经结束执行(run 方法执行完了)的线程

![](../../img/thread_state.png)
