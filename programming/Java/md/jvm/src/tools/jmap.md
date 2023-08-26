# jmap

jmap(Memory Map for Java)命令用于生成堆转储快照(一般称为heapdump或dump文件)。jmap还可以查询finalize执行队列、Java堆和方法区的详细信息，如空间使用率、当前用的是哪种收集器等。

jmap命令格式：

```
jmap [ option ] vmid
```

vmid表示目标Java虚拟机进程ID，可以使用jps命令获取。

option选项：

- -dump：生成Java堆转储快照。格式为-dump:\[live,]format=b,file=filename。live子参数是可选的，表示只转储存活的对象。通常情况下，dump出来的堆快照是整个JVM的堆快照
- -finalizerinfo：打印等待终结的对象信息
- -heap：打印Java堆详细信息，如使用哪种收集器、参数配置、分代状况等
- -histo：打印Java堆中对象统计信息，包括类、实例数量、合计容量
- -permstat：以ClassLoader为统计口径打印永久代(Permgen)空间使用情况
- -F：当-dump没有响应时，强制生成dump快照

## jmap执行样例

```
jmap -dump:format=b,file=eclipse.bin 3500
Dumping heap to C:\Users\IcyFenix\eclipse.bin ...
Heap dump file created
```
