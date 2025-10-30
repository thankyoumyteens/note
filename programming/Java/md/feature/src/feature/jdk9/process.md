# 进程 API

Java 9 引入了全新的进程 API（Process API），位于 java.lang 和 java.lang.ProcessHandle 包下，解决了传统 Process 类功能薄弱、无法有效管理和监控进程的问题。新 API 提供了获取进程信息（如 PID、父进程、启动时间）、监控进程状态、获取进程后代等能力，大幅增强了 Java 对操作系统进程的控制能力。

## 传统 Process 类的局限性

ava 9 之前，通过 `Runtime.getRuntime().exec()` 或 `ProcessBuilder` 创建的进程由 `java.lang.Process` 类表示，但功能非常有限：

- 仅能获取输入流、输出流和错误流，以及等待进程结束 `waitFor()`、销毁进程 `destroy()` 等基础操作
- 无法直接获取进程的 PID、父进程信息、启动时间、CPU 使用率等关键元数据
- 无法监控进程的状态变化（如从运行到终止）

## Java 9 进程 API 的核心类

| 类/接口              | 作用                                                       |
| -------------------- | ---------------------------------------------------------- |
| `Process`            | 原有类增强，新增 `toHandle()` 方法获取 `ProcessHandle`。   |
| `ProcessHandle`      | 表示一个原生进程的句柄，提供进程元数据和状态控制。         |
| `ProcessHandle.Info` | 嵌套接口，包含进程的详细信息（如命令、启动时间、用户等）。 |

## 获取当前进程信息

```java
// 获取当前进程句柄
ProcessHandle currentProcess = ProcessHandle.current();

// 获取 PID（进程 ID）
long pid = currentProcess.pid();
System.out.println("当前进程 PID: " + pid);

// 获取进程信息（Info）
ProcessHandle.Info info = currentProcess.info();

// 打印进程详细信息（命令、启动时间、用户等）
System.out.println("启动命令: " + info.command().orElse("未知"));
System.out.println("启动时间: " + info.startInstant().orElse(null)); // 返回 Instant
System.out.println("所属用户: " + info.user().orElse("未知"));
```

## 启动外部进程并监控

```java
try {
    // 启动外部进程
    Process process = new ProcessBuilder("java", "-version").start();

    // 获取进程句柄
    ProcessHandle handle = process.toHandle();
    System.out.println("外部进程 PID: " + handle.pid());

    // 监控进程是否存活
    System.out.println("进程是否存活: " + handle.isAlive());

    // 等待进程结束（最多等待 5 秒）
    boolean exited = handle.onExit().get(5, TimeUnit.SECONDS) != null;
    System.out.println("5 秒内是否结束: " + exited);

    // 进程结束后打印信息
    handle.onExit().thenAccept(ph -> {
        System.out.println("进程已结束");
    });

} catch (Exception e) {
    e.printStackTrace();
}
```

## 获取父进程与子进程

```java
// 获取当前进程的父进程
ProcessHandle parent = ProcessHandle.current().parent().orElse(null);
if (parent != null) {
    System.out.println("父进程 PID: " + parent.pid());
}

// 获取当前进程的所有子进程（直接子进程）
Stream<ProcessHandle> children = ProcessHandle.current().children();
children.forEach(child -> System.out.println("子进程 PID: " + child.pid()));

// 获取所有后代进程（子进程、孙进程等）
Stream<ProcessHandle> descendants = ProcessHandle.current().descendants();
descendants.forEach(desc -> System.out.println("后代进程 PID: " + desc.pid()));
```

## 销毁进程

```java
ProcessHandle handle = ...;

// 正常销毁（发送 SIGTERM 信号，类似 Process.destroy()）
handle.destroy();

// 强制销毁（发送 SIGKILL 信号，类似 Process.destroyForcibly()）
handle.destroyForcibly();

// 检查是否已被销毁
boolean isDestroyed = !handle.isAlive();
```
