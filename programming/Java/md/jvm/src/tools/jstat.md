# jstat

jstat(JVM Statistics Monitoring Tool)是用于监视虚拟机各种运行状态信息的命令行工具。它可以显示本地或者远程虚拟机进程中的类加载、内存、垃圾收集、即时编译等运行时数据，在没有GUI图形界面、只提供了纯文本控制台环境的服务器上，它将是运行期定位虚拟机性能问题的常用工具。

jstat命令格式：

```
jstat [ option vmid [interval[s|ms] [count]] ]
```

如果是本地虚拟机进程，参数vmid与LVMID是一致的。如果是远程虚拟机进程，那VMID的格式应当是：

```
[protocol:][//]lvmid[@hostname[:port]/servername]
```

参数interval和count代表查询间隔和次数，如果省略这2个参数，说明只查询一次。假设需要每250毫秒查询一次进程2764垃圾收集状况，一共查询20次，那命令应当是：

```
jstat -gc 2764 250 20
```

选项option代表用户希望查询的虚拟机信息，主要分为三类：类加载、垃圾收集、运行期编译状
况。

option常用选项：

- -class：类加载、卸载、总空间、加载数量
- -gc：垃圾收集情况
- -gccapacity：堆空间、新生代、老年代、永久代、jvm各代容量
- -gcutil：垃圾收集、已使用、未使用、已使用百分比
- -gccause：垃圾收集的个数、原因
- -gcnew：新生代垃圾收集状况
- -gcnewcapacity：新生代、老年代容量
- -gcold：老年代垃圾收集状况
- -gcoldcapacity：老年代容量
- -gcpermcapacity：永久代容量
- -compiler：编译状态
- -printcompilation：显示即时编译的状况

## jstat执行样例

```
jstat -gcutil 2764
S0     S1     E      O      P       YGC    YGCT    FGC    FGCT    GCT
0.00   0.00   6.20   41.42  47.20   16     0.105   3      0.472   0.577
```

查询结果表明：这台服务器的新生代Eden区(E，表示Eden)使用了6.2%的空间，2个Survivor区(S0、S1，表示Survivor0、Survivor1)里面都是空的，老年代(O，表示Old)和永久代(P，表示Permanent)则分别使用了41.42%和47.20%的空间。程序运行以来共发生Minor GC(YGC，表示Young GC)16次，总耗时0.105秒。发生Full GC(FGC，表示Full GC)3次，总耗时(FGCT，表示Full GC Time)为0.472秒。所有GC总耗时(GCT，表示GC Time)为0.577秒。
