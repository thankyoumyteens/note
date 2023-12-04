# jstat

jstat(JVM Statistics Monitoring Tool)是用于监视虚拟机各种运行状态信息的命令行工具。

jstat 命令格式:

```sh
jstat [option] [vmid] [间隔时间/毫秒] [查询次数]
# 查询vmid为2764的进程的垃圾回收情况, 每250毫秒查询一次, 一共查询20次
jstat -gc 2764 250 20
```

option 常用选项:

- -class: 监视类加载、卸载数量、总空间以及类装载所耗费的时间
- -compiler: 输出即时编译器编译过的方法、耗时等信息
- -printcompilation: 输出已经被即时编译的方法
- -gc: 垃圾回收情况
- -gccapacity: 监视内容与 -gc 基本相同，但输出主要关注 Java 堆各个区域使用到的最大、最小空间
- -gcutil: 监视内容与 -gc 基本相同，但输出主要关注已使用空间占总空间的百分比
- -gccause: 与 -gcutil 功能一样，但是会额外输出导致上一次垃圾收集产生的原因
- -gcnew: 监视新生代的垃圾回收状况
- -gcnewcapacity: 监视内容与 -gcnew 基本相同，输出主要关注使用到的最大、最小空间
- -gcold: 监视老年代的垃圾回收状况
- -gcoldcapacity: 监视内容与 -gcold 基本相同，输出主要关注使用到的最大、最小空间
- -gcpermcapacity: 输出永久代使用到的最大、最小空间

## 类加载、卸载、总空间、加载数量

```sh
$ jstat -class 15948
Loaded  Bytes  Unloaded  Bytes     Time
  7459 14228.4        0     0.0       5.58
```

- Loaded: 已加载的 class 的数量
- Bytes: 所占用空间大小
- Unloaded: 未加载的 class 数量
- Bytes: 未加载的 class 占用的空间
- Time: 类加载耗费的时间

## 编译状态

```sh
$ jstat -compiler 15948
Compiled Failed Invalid   Time   FailedType FailedMethod
    4147      0       0    11.41          0
```

- Compiled: JIT 编译器已编译的方法的数量
- Failed: 编译失败的数量
- Invalid: 不可用的数量
- Time: 编译耗费的时间
- FailedType: 失败类型
- FailedMethod: 编译失败的方法

## 垃圾回收情况

```sh
$ jstat -gc 15948
    S0C         S1C         S0U         S1U          EC           EU           OC           OU          MC         MU       CCSC      CCSU     YGC     YGCT     FGC    FGCT     CGC    CGCT       GCT
     1024.0      1024.0       820.7         0.0       8256.0       5192.0      20480.0      16530.4    34176.0    33872.2    4288.0    4193.6     48     0.175     1     0.060     -         -     0.235
```

- S0C：Survivor0 的大小
- S1C：Survivor1 的大小
- S0U：Survivor0 已使用的大小
- S1U：Survivor1 已使用的大小
- EC：Eden 区的大小
- EU：Eden 区已使用的大小
- OC：老年代的大小
- OU：老年代已使用的大小
- MC：方法区的大小
- MU：方法区已使用的大小
- CCSC:压缩类空间(存放类的元数据)大小
- CCSU:压缩类空间已使用的大小
- YGC：Young GC 发生的次数
- YGCT：Young GC 消耗的时间
- FGC：Full GC 发生的次数
- FGCT：Full GC 消耗的时间
- CGC：并发 GC 发生的次数
- CGCT：并发 GC 消耗的时间
- GCT：垃圾回收消耗的总时间

## gcutil

```sh
jstat -gcutil 31836
  S0     S1     E      O      M     CCS    YGC     YGCT     FGC    FGCT     CGC    CGCT       GCT
  0.00  83.33  58.33  47.49  98.84  95.96     18     0.164     0     0.000     2     0.005     0.169
```

- S0：Survivor0 已使用的空间占总空间的比例
- S1：Survivor1 已使用的空间占总空间的比例
- E：Eden 已使用的空间占总空间的比例
- O：老年代已使用的空间占总空间的比例
- M：方法区已使用的空间占总空间的比例
- CCS：压缩类空间已使用的空间占总空间的比例
- YGC：Young GC 发生的次数
- YGCT：Young GC 消耗的时间
- FGC：Full GC 发生的次数
- FGCT：Full GC 消耗的时间
- CGC：并发 GC 发生的次数
- CGCT：并发 GC 消耗的时间
- GCT：垃圾回收消耗的总时间
