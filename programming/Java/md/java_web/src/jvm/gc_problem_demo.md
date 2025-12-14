# 本地模拟

### 1. 模拟有问题的服务

```java
package com.example;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;

public class GCDemo {
    private static final int CORE_THREADS = 8;
    private static final int QUEUE_CAPACITY = 10000;
    private static final ExecutorService POOL = new ThreadPoolExecutor(
            CORE_THREADS, CORE_THREADS,
            0L, TimeUnit.MILLISECONDS,
            new LinkedBlockingQueue<>(QUEUE_CAPACITY),
            new ThreadPoolExecutor.AbortPolicy()
    );

    private static final Random RANDOM = new Random();
    private static final AtomicLong REQ_COUNT = new AtomicLong();
    private static final AtomicLong SLOW_COUNT = new AtomicLong();

    public static void main(String[] args) throws Exception {
        System.out.println("GCDemo started. Press Cmd+C to exit.");

        // 单独开一个监控线程，打印简单的吞吐量和 P99 模拟
        startMonitorThread();

        // 模拟持续有请求进来
        while (true) {
            try {
                POOL.submit(() -> handleRequest());
            } catch (RejectedExecutionException e) {
                // 队列满了，模拟降级/丢请求
            }
            // 控制整体 QPS，适当调节
            Thread.sleep(1);
        }
    }

    private static void handleRequest() {
        long start = System.nanoTime();
        REQ_COUNT.incrementAndGet();

        // 1. 正常场景下，制造大量短命临时对象
        List<Map<String, Object>> list = new ArrayList<>();
        for (int i = 0; i < 2000; i++) {
            Map<String, Object> map = new HashMap<>();
            map.put("id", i);
            map.put("name", "name-" + i);
            map.put("value", new byte[1024]); // 1KB
            list.add(map);
        }

        // 2. 偶发的“批量导出/大查询”，堆积大量对象到老年代
        if (RANDOM.nextInt(100) == 0) { // 1% 概率触发
            SLOW_COUNT.incrementAndGet();
            List<byte[]> bigList = new ArrayList<>();
            // 模拟一次性加载大量数据
            for (int i = 0; i < 50000; i++) {
                bigList.add(new byte[1024]); // 1KB * 50k ≈ 50MB
            }
            // 模拟业务处理耗时
            try {
                Thread.sleep(200);
            } catch (InterruptedException ignored) {
            }
        }

        // 3. 模拟一点 CPU 计算
        double x = 0;
        for (int i = 0; i < 10000; i++) {
            x += Math.sqrt(i);
        }

        long rtMicros = (System.nanoTime() - start) / 1000;
        RTRecorder.record(rtMicros);
    }

    // 简单的 RT 统计，用滑动窗口来模拟 P99
    static class RTRecorder {
        private static final int WINDOW_SIZE = 5000;
        private static final long[] WINDOW = new long[WINDOW_SIZE];
        private static volatile int idx = 0;

        public static synchronized void record(long rtMicro) {
            WINDOW[idx++ % WINDOW_SIZE] = rtMicro;
        }

        public static synchronized long p99Micros() {
            long[] copy = Arrays.copyOf(WINDOW, WINDOW_SIZE);
            Arrays.sort(copy);
            return copy[(int) (WINDOW_SIZE * 0.99)];
        }
    }

    private static void startMonitorThread() {
        new Thread(() -> {
            long lastCount = 0;
            while (true) {
                try {
                    Thread.sleep(5000);
                } catch (InterruptedException ignored) {
                }
                long curCount = REQ_COUNT.get();
                long qps = (curCount - lastCount) / 5;
                lastCount = curCount;
                long p99 = RTRecorder.p99Micros();
                long slow = SLOW_COUNT.get();

                System.out.printf(
                        "[MONITOR] totalReq=%d, qps=%d, p99=%.2fms, slowTrigger=%d%n",
                        curCount, qps, p99 / 1000.0, slow
                );
            }
        }, "monitor-thread").start();
    }
}
```

### 2. 设置启动时的 JVM 参数

```
-Xms512m -Xmx512m -XX:+UseParallelGC -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:gc.log
```

运行一会儿，等它“作死”一阵。

### 3. 通过 jstat 观察 GC 行为

用 jps 找出进程号:

```sh
walter@walter2743mbp pure-java % jps -l

79236 com.example.GCDemo
```

用 jstat 看 GC 情况：

```sh
walter@walter2743mbp pure-java % jstat -gcutil 79236 1000
  S0     S1     E      O      M     CCS    YGC     YGCT     FGC    FGCT     CGC    CGCT       GCT
  2.99   0.00   0.00  32.79  93.71  89.58   1984     2.308    10     0.091     -         -     2.398
  0.00  10.03  38.05  40.69  93.71  89.58   2007     2.328    10     0.091     -         -     2.419
  0.00   9.68   7.73  44.39  93.71  89.58   2023     2.345    10     0.091     -         -     2.436
  2.93   0.00   0.00  58.96  93.71  89.58   2042     2.363    10     0.091     -         -     2.454
  5.74   0.00  52.55  69.67  93.71  89.58   2062     2.383    10     0.091     -         -     2.473
  0.00   9.25  66.28  80.10  93.71  89.58   2083     2.406    10     0.091     -         -     2.496
  8.37   0.00   0.00  21.98  93.71  89.58   2108     2.437    11     0.105     -         -     2.542
  0.00   9.11   9.35  21.99  93.71  89.58   2129     2.457    11     0.105     -         -     2.561
  2.17   0.00   0.00  43.62  93.71  89.58   2150     2.479    11     0.105     -         -     2.584
  0.00   4.90   0.00  52.36  93.71  89.58   2173     2.506    11     0.105     -         -     2.610
  1.27   0.00   0.00  62.61  93.72  89.58   2202     2.538    11     0.105     -         -     2.643
  1.72   0.00   3.01  76.13  93.72  89.58   2230     2.574    11     0.105     -         -     2.679
  0.00  99.98   0.00  80.78  93.72  89.58   2251     2.600    11     0.105     -         -     2.705
  0.00   3.37   0.00  93.85  93.72  89.58   2277     2.634    11     0.105     -         -     2.738
 10.24   0.00   0.00  94.38  93.72  89.58   2300     2.659    11     0.105     -         -     2.763
  3.12   0.00  40.79  32.12  93.73  89.58   2323     2.702    12     0.112     -         -     2.814
  6.25   0.00   0.00  46.88  93.73  89.58   2343     2.727    12     0.112     -         -     2.839
  1.01   0.00  36.27  59.24  93.73  89.58   2367     2.756    12     0.112     -         -     2.868
  0.00   5.00   2.77  64.21  93.73  89.58   2390     2.782    12     0.112     -         -     2.894
 97.76   0.00   0.00  86.27  93.73  89.58   2411     2.826    12     0.112     -         -     2.938
  0.00  13.87  72.04  86.28  93.76  89.58   2430     2.845    12     0.112     -         -     2.957
  0.00   2.68   0.00  22.86  93.76  89.58   2458     2.882    13     0.123     -         -     3.006
  0.00   6.25   0.00  26.55  93.76  89.58   2476     2.901    13     0.123     -         -     3.025
 18.51   0.00   0.00  35.68  93.76  89.58   2493     2.920    13     0.123     -         -     3.044
  0.00   5.98   0.00  45.22  93.76  89.58   2512     2.942    13     0.123     -         -     3.065
```

重点观察的列：

- FGC（Full GC 次数）明显在涨
- FGCT（Full GC 累计时间）涨得比较快
- O（老年代使用率）即使发生 FGC，也掉得不多，经常又很快涨回去

### 4. 分析 GC 日志

gc.log 文件已经生成了，你可以用：

- GCeasy：https://gceasy.io/
- GCViewer（本地工具）

把 gc.log 丢进去。

你要重点观察的点：

1. GC Timeline：
   - Full GC 事件很多
   - 每次 Full GC Pause 时间在几十到几百毫秒甚至上秒
   - 和你控制台的 p99 日志时间对一对，会很贴近
2. 老年代使用曲线：
   - 一路往上爬
   - Full GC 之后降得不多，很快又上去
   - 工具可能会给出类似“Promotion Rate 高”的提示

### 5. 用 jmap 定位“谁在占内存”

```sh
walter@walter2743mbp pure-java % jmap -histo 79236 | head -n 30

 num     #instances         #bytes  class name
----------------------------------------------
   1:        255643      265845056  [B
   2:         19010       18091456  [I
   3:        108813        3482016  java.util.HashMap$Node
   4:         36022        2888192  [Ljava.util.HashMap$Node;
   5:          1238        1905368  [Ljava.lang.Object;
   6:         36028        1729344  java.util.HashMap
   7:         39407        1531384  [C
   8:         39398         945552  java.lang.String
   9:         33952         543232  java.lang.Integer
  10:           971         110808  java.lang.Class
  11:             5          40456  [J
  12:           255          18360  java.lang.reflect.Field
  13:           425          13600  java.util.concurrent.ConcurrentHashMap$Node
  14:           149          13112  java.lang.reflect.Method
  15:           210          11760  java.lang.invoke.MemberName
  16:           341          10912  sun.misc.FDBigInteger
  17:           212           8480  java.lang.ref.SoftReference
  18:           282           8384  [Ljava.lang.Class;
  19:           225           7200  java.lang.invoke.LambdaForm$Name
  20:           167           6904  [Ljava.lang.String;
  21:            17           6392  java.lang.Thread
  22:           256           6144  java.lang.Long
  23:            94           5640  [Ljava.lang.ref.SoftReference;
  24:           175           5600  java.lang.invoke.MethodType$ConcurrentWeakInternSet$WeakEntry
  25:           129           5160  java.lang.invoke.MethodType
  26:            22           4448  [Ljava.util.concurrent.ConcurrentHashMap$Node;
  27:            67           4288  java.net.URL
```

其中 `[B` 就是 `byte[]`，说明大量内存都被字节数组占着。

### 6. 再导一次堆 dump，用 MAT 分析（可选）

```sh
walter@walter2743mbp pure-java % jmap -dump:live,format=b,file=heap.bin 79236
Heap dump file created
```

用 Eclipse MAT 打开：

- 看 Dominator Tree，谁是最大的内存支配者
- 通常你会看到几个大 List / Map 持有一堆 `byte[]`
