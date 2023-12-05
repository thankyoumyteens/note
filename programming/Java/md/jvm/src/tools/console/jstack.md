# jstack

jstack(Stack Trace for Java)命令用于生成 JVM 当前时刻的线程快照。

jstack 命令格式:

```
jstack [ option ] vmid
```

option 选项:

- -F: 当正常输出的请求不被响应时, 强制输出线程堆栈
- -l: 除堆栈外, 显示关于锁的附加信息
- -m: 打印 java 内存映射

从 JDK 5 起, java.lang.Thread 类新增了一个 getAllStackTraces()方法用于获取虚拟机中所有线程的 StackTraceElement 对象。使用这个方法可以通过简单的几行代码完成 jstack 的大部分功能。

```jsp
<%@ page import="java.util.Map"%>
<html>
<head>
<title>服务器线程信息</title>
</head>
<body>
<pre>
<%
    for (Map.Entry<Thread, StackTraceElement[]> stackTrace : Thread.getAllStackTraces().entrySet()) {
        Thread thread = (Thread) stackTrace.getKey();
        StackTraceElement[] stack = (StackTraceElement[]) stackTrace.getValue();
        if (thread.equals(Thread.currentThread())) {
            continue;
        }
        out.print("\n线程：" + thread.getName() + "\n");
        for (StackTraceElement element : stack) {
            out.print("\t"+element+"\n");
        }
    }
%>
</pre>
</body>
</html>
```
