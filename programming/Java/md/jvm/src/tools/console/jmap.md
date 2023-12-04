# jmap

jmap(Memory Map for Java)命令用于生成堆转储快照(一般称为 heapdump 或 dump 文件)。jmap 还可以查询 finalize 执行队列、Java 堆和方法区的详细信息, 如空间使用率、当前用的是哪种回收器等。

jmap 命令格式:

```sh
jmap [option] vmid
```

option 选项:

- -dump: 生成 Java 堆转储快照。格式为`-dump:[live,]format=b,file=文件路径`。live 子参数是可选的, 表示只转储存活的对象。通常情况下, dump 出来的堆快照是整个 JVM 的堆快照
- -finalizerinfo: 打印等待终结的对象信息
- -heap: 打印 Java 堆详细信息, 如使用哪种收集器、参数配置、分代状况等
- -histo: 打印 Java 堆中对象统计信息, 包括类、实例数量、合计容量
- -permstat: 以 ClassLoader 为统计口径打印永久代(Permgen)空间使用情况
- -F: 当-dump 没有响应时, 强制生成 dump 快照

## 输出 dump 文件

```sh
jmap -dump:live,format=b,file=d.bin 31836
Dumping heap to /root/d.bin ...
Heap dump file created [26416722 bytes in 0.232 secs]
```

导出后, 可以使用 MAT 来分析 dump 文件: [MemoryAnalyzer](https://ftp.jaist.ac.jp/pub/eclipse/mat/1.14.0/rcp/MemoryAnalyzer-1.14.0.20230315-win32.win32.x86_64.zip)

## 显示正在等待执行 finalize() 方法的对象

```sh
$ jmap -finalizerinfo 31836
No instances waiting for finalization found
```

## 显示 Java 堆的详细信息

```sh
jmap -heap 31836
Error: -heap option used
Cannot connect to core dump or remote debug server. Use jhsdb jmap instead
```

JDK 9 及以上版本需要使用 jhsdb jmap 来替代:

```sh
$ jhsdb jmap --heap --pid 31836
Attaching to process ID 31836, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 17.0.9+11-LTS

using thread-local object allocation.
Garbage-First (G1) GC with 1 thread(s)

# Java堆配置情况
Heap Configuration:
   MinHeapFreeRatio         = 40
   MaxHeapFreeRatio         = 70
   MaxHeapSize              = 490733568 (468.0MB)
   NewSize                  = 1363144 (1.2999954223632812MB)
   MaxNewSize               = 293601280 (280.0MB)
   OldSize                  = 5452592 (5.1999969482421875MB)
   NewRatio                 = 2
   SurvivorRatio            = 8
   MetaspaceSize            = 22020096 (21.0MB)
   CompressedClassSpaceSize = 1073741824 (1024.0MB)
   MaxMetaspaceSize         = 17592186044415 MB
   G1HeapRegionSize         = 1048576 (1.0MB)

# G1管理的堆空间使用情况
Heap Usage:
G1 Heap:
   regions  = 468
   capacity = 490733568 (468.0MB)
   used     = 13658480 (13.025741577148438MB)
   free     = 477075088 (454.97425842285156MB)
   2.783278114775307% used
G1 Young Generation:
Eden Space:
   regions  = 0
   capacity = 26214400 (25.0MB)
   used     = 0 (0.0MB)
   free     = 26214400 (25.0MB)
   0.0% used
Survivor Space:
   regions  = 0
   capacity = 0 (0.0MB)
   used     = 0 (0.0MB)
   free     = 0 (0.0MB)
   0.0% used
G1 Old Generation:
   regions  = 15
   capacity = 23068672 (22.0MB)
   used     = 13658480 (13.025741577148438MB)
   free     = 9410192 (8.974258422851562MB)
   59.207916259765625% used
```

## 显示堆中对象统计信息

```sh
$ jmap -histo 31836
# 编号    这个类的对象个数    占用的空间   类名(类所在的模块)
 num     #instances         #bytes  class name (module)
-------------------------------------------------------
   1:         52800        3045408  [B (java.base@17.0.9)
   2:          4726        1219296  [C (java.base@17.0.9)
   3:         49899        1197576  java.lang.String (java.base@17.0.9)
   4:         32685        1045920  java.util.concurrent.ConcurrentHashMap$Node (java.base@17.0.9)
   5:          7919         945696  java.lang.Class (java.base@17.0.9)
   6:          3948         912552  [I (java.base@17.0.9)
   7:          7743         681384  java.lang.reflect.Method (java.base@17.0.9)
   8:          6447         458216  [Ljava.lang.Object; (java.base@17.0.9)
   9:         10580         338560  java.util.HashMap$Node (java.base@17.0.9)
  10:          3486         329888  [Ljava.util.HashMap$Node; (java.base@17.0.9)
  11:           279         322992  [Ljava.util.concurrent.ConcurrentHashMap$Node; (java.base@17.0.9)
  ...
```

使用 `jmap -histo pid > a.log` 将其保存到日志，在一段时间后，使用文本对比工具，可以对比出 GC 回收了哪些对象。
