# 启动线程

JDK 中的 6 种线程状态:

1. NEW: 新创建但尚未启动的线程处于这种状态。通过 new 关键字创建了 `java.lang.Thread` 类(或其子类)的对象
2. BLOCKED: 线程受阻塞并等待某个监视器对象锁。当线程执行 synchronized 方法或代码块, 但未获得相应对象锁时处于这种状态
3. RUNNABLE: 正在 Java 虚拟机中执行的线程处于这种状态。有三种情形:
   - 一种情形是 Thread 类的对象调用了 `start()` 函数, 这时的线程就等待时间片轮转到自己, 以便获得 CPU
   - 另一种情形是线程在处于 RUNNABLE 状态时并没有运行完自己的 `run()` 函数, 时间片用完之后回到 RUNNABLE 状态
   - 还有一种情形就是处于 BLOCKED 状态的线程结束了当前的 BLOCKED 状态之后重新回到 RUNNABLE 状态
4. TERMINATED: 已退出的线程处于这种状态
5. TIMED_WAITING: 等待另一个线程来执行某一特定操作, 需要指定等待时间, 不会无限期地等待
6. WAITING: 无限期地等待另一个线程来执行某一特定操作

在 JVM 层面, HotSpot 内部定义了线程的 5 种基本状态:

1. `-thread_new`: 表示刚启动, 正处在初始化过程中
2. `-thread_in_native`: 表示运行本地代码
3. `-thread_in_vm`: 表示在 VM 中运行
4. `-thread_in_Java`: 表示运行 Java 代码
5. `-thread_blocked`: 表示阻塞

为了支持内部状态转换，还补充定义了其他几种过渡状态：`_<thread_state_type>_trans`，其中 thread_state_type 分别表示上述 5 种基本状态类型。

在 HotSpot 中，定义了如下几种线程类型:

```cpp
// --- src/hotspot/share/runtime/os.hpp --- //

enum ThreadType {
  vm_thread,
  gc_thread,         // GC thread
  java_thread,       // Java, JVMTIAgent and Service threads.
  compiler_thread,
  watcher_thread,
  asynclog_thread,   // dedicated to flushing logs
  os_thread
};
```

## 创建主线程
