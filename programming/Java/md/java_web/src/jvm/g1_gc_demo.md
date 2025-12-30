# 模拟一轮完整的 G1 周期

```java
package com.example;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * 模拟 G1 各阶段的一个小程序：
 * - 持续分配对象，触发 Young GC
 * - 保留部分对象，晋升到老年代，触发 Concurrent Mark + Mixed GC
 */
public class G1PhasesDemo {

    // 控制运行时间（秒）
    private static final int RUN_SECONDS = 180;
    // 工作线程数
    private static final int WORKER_THREADS = 4;
    // 每个线程每轮分配的对象数
    private static final int ALLOC_PER_ROUND = 10_000;
    // 每个对象大小（字节）——用 byte[] 模拟
    private static final int OBJECT_SIZE = 1024; // 1 KB
    // 留存比例（模拟长生代）
    private static final double SURVIVE_RATE = 0.05; // 5%

    static void main(String[] args) throws Exception {
        System.out.println("G1 Phases Demo started. PID=" + ProcessHandle.current().pid());
        System.out.println("Run seconds: " + RUN_SECONDS);

        long endTime = System.currentTimeMillis() + RUN_SECONDS * 1000L;
        CountDownLatch latch = new CountDownLatch(WORKER_THREADS);

        for (int i = 0; i < WORKER_THREADS; i++) {
            Thread t = new Thread(new Worker(endTime, latch), "worker-" + i);
            t.setDaemon(false);
            t.start();
        }

        // 主线程也周期性做点小分配，避免完全空闲
        long lastLog = System.currentTimeMillis();
        List<byte[]> mainHolder = new ArrayList<>();
        Random r = new Random();

        while (System.currentTimeMillis() < endTime) {
            // 主线程分配少量对象
            for (int i = 0; i < 100; i++) {
                byte[] b = new byte[OBJECT_SIZE];
                if (r.nextDouble() < 0.02) {
                    mainHolder.add(b); // 偶尔留一些增加存活对象
                }
            }
            // 每 5 秒打印一次心跳
            long now = System.currentTimeMillis();
            if (now - lastLog > 5000) {
                System.out.println("[main] still running... holder size=" + mainHolder.size());
                lastLog = now;
            }
            // 稍微歇一会，避免 100% CPU
            TimeUnit.MILLISECONDS.sleep(50);
        }

        latch.await();
        System.out.println("G1 Phases Demo finished.");
    }

    private static class Worker implements Runnable {
        private final long endTime;
        private final CountDownLatch latch;
        private final Random random = new Random();

        // 每个 worker 自己的“长寿对象池”
        private final List<byte[]> survivorHolder = new ArrayList<>();

        Worker(long endTime, CountDownLatch latch) {
            this.endTime = endTime;
            this.latch = latch;
        }

        @Override
        public void run() {
            try {
                while (System.currentTimeMillis() < endTime) {
                    // 每一轮大量分配
                    for (int i = 0; i < ALLOC_PER_ROUND; i++) {
                        byte[] data = new byte[OBJECT_SIZE];

                        // 部分对象加入 survivorHolder，增加存活率，帮助晋升到老年代
                        if (random.nextDouble() < SURVIVE_RATE) {
                            survivorHolder.add(data);
                        }
                    }

                    // 控制一下 survivorHolder 的大小，避免 OOM
                    if (survivorHolder.size() > 50_000) {
                        // 模拟有些“老对象”下线
                        int removeCount = survivorHolder.size() / 2;
                        for (int i = 0; i < removeCount; i++) {
                            survivorHolder.remove(survivorHolder.size() - 1);
                        }
                    }

                    // 稍微 sleep 一下，给 GC 一点时间调度
                    TimeUnit.MILLISECONDS.sleep(20);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                latch.countDown();
            }
        }
    }
}
```

## 启动

使用 JDK25, JVM 参数如下:

```
-XX:+UseG1GC
-Xms512m
-Xmx512m
-XX:MaxGCPauseMillis=200
-XX:+UnlockExperimentalVMOptions
-Xlog:gc*:file=gc.log:time,uptime,level,tags
```

GC 日志会打印到 gc.log 中(只打印 info 日志)。

如果想打印所有日志可以使用下面的:

```
-Xlog:gc*,gc+heap=debug,gc+age=trace,gc+ergo=debug,gc+phases=trace,gc+humongous=debug:file=gc.log:time,uptime,level,tags
```

## JVM 启动 + G1 初始化

```log
[2025-12-30T19:39:56.469+0800][0.004s][info][gc,init] CardTable entry size: 512
[2025-12-30T19:39:56.469+0800][0.004s][info][gc     ] Using G1
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Version: 25.0.1+8-LTS (release)
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] CPUs: 14 total, 14 available
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Memory: 36864M
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Large Page Support: Disabled
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] NUMA Support: Disabled
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Compressed Oops: Enabled (Zero based)
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Heap Region Size: 1M
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Heap Min Capacity: 512M
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Heap Initial Capacity: 512M
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Heap Max Capacity: 512M
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Pre-touch: Disabled
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Parallel Workers: 11
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Concurrent Workers: 3
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Concurrent Refinement Workers: 11
[2025-12-30T19:39:56.469+0800][0.005s][info][gc,init] Periodic GC: Disabled
```

## 正常 Young GC（没开始并发标记）

```log
[2025-12-30T19:39:56.528+0800][0.064s][info][gc,start    ] GC(0) Pause Young (Normal) (G1 Evacuation Pause)
[2025-12-30T19:39:56.529+0800][0.064s][info][gc,task     ] GC(0) Using 11 workers of 11 for evacuation
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,phases   ] GC(0)   Pre Evacuate Collection Set: 0.15ms
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,phases   ] GC(0)   Merge Heap Roots: 0.04ms
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,phases   ] GC(0)   Evacuate Collection Set: 0.52ms
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,phases   ] GC(0)   Post Evacuate Collection Set: 0.14ms
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,phases   ] GC(0)   Other: 0.39ms
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,heap     ] GC(0) Eden regions: 47->0(222)
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,heap     ] GC(0) Survivor regions: 0->3(6)
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,heap     ] GC(0) Old regions: 2->2
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,heap     ] GC(0) Humongous regions: 0->0
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,metaspace] GC(0) Metaspace: 1066K(1216K)->1066K(1216K) NonClass: 1002K(1088K)->1002K(1088K) Class: 63K(128K)->63K(128K)
[2025-12-30T19:39:56.530+0800][0.065s][info][gc          ] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 48M->4M(512M) 1.448ms
[2025-12-30T19:39:56.530+0800][0.065s][info][gc,cpu      ] GC(0) User=0.00s Sys=0.00s Real=0.01s
```

## 触发“Concurrent Start”的 Young GC：标记周期开始

```log
[2025-12-30T19:39:59.140+0800][2.675s][info][gc,start    ] GC(15) Pause Young (Concurrent Start) (G1 Evacuation Pause)
[2025-12-30T19:39:59.140+0800][2.676s][info][gc,task     ] GC(15) Using 11 workers of 11 for evacuation
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,phases   ] GC(15)   Pre Evacuate Collection Set: 0.29ms
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,phases   ] GC(15)   Merge Heap Roots: 0.11ms
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,phases   ] GC(15)   Evacuate Collection Set: 1.99ms
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,phases   ] GC(15)   Post Evacuate Collection Set: 1.61ms
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,phases   ] GC(15)   Other: 0.11ms
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,heap     ] GC(15) Eden regions: 154->0(142)
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,heap     ] GC(15) Survivor regions: 22->10(22)
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,heap     ] GC(15) Old regions: 309->333
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,heap     ] GC(15) Humongous regions: 0->0
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,metaspace] GC(15) Metaspace: 1075K(1216K)->1075K(1216K) NonClass: 1011K(1088K)->1011K(1088K) Class: 63K(128K)->63K(128K)
[2025-12-30T19:39:59.144+0800][2.680s][info][gc          ] GC(15) Pause Young (Concurrent Start) (G1 Evacuation Pause) (Evacuation Failure: Allocation) 484M->342M(512M) 4.328ms
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,cpu      ] GC(15) User=0.03s Sys=0.00s Real=0.00s
```

紧接着，会看到并发标记的总周期开始

```log
[2025-12-30T19:39:59.144+0800][2.680s][info][gc          ] GC(16) Concurrent Mark Cycle
[2025-12-30T19:39:59.144+0800][2.680s][info][gc,marking  ] GC(16) Concurrent Scan Root Regions
[2025-12-30T19:39:59.152+0800][2.688s][info][gc,marking  ] GC(16) Concurrent Scan Root Regions 8.087ms
```

在标记期间，应用线程继续跑，标记线程并发工作

```log
[2025-12-30T19:39:59.152+0800][2.688s][info][gc,marking  ] GC(16) Concurrent Mark
[2025-12-30T19:39:59.152+0800][2.688s][info][gc,marking  ] GC(16) Concurrent Mark From Roots
[2025-12-30T19:39:59.152+0800][2.688s][info][gc,task     ] GC(16) Using 3 workers of 3 for marking
[2025-12-30T19:39:59.161+0800][2.696s][info][gc,marking  ] GC(16) Concurrent Mark From Roots 8.348ms
[2025-12-30T19:39:59.161+0800][2.696s][info][gc,marking  ] GC(16) Concurrent Preclean
[2025-12-30T19:39:59.161+0800][2.696s][info][gc,marking  ] GC(16) Concurrent Preclean 0.016ms
```

Remark 阶段：短暂停顿，补上并发期的变更

```log
[2025-12-30T19:39:59.161+0800][2.697s][info][gc,start    ] GC(16) Pause Remark
[2025-12-30T19:39:59.162+0800][2.697s][info][gc          ] GC(16) Pause Remark 367M->362M(512M) 0.786ms
[2025-12-30T19:39:59.162+0800][2.697s][info][gc,cpu      ] GC(16) User=0.00s Sys=0.00s Real=0.00s
[2025-12-30T19:39:59.162+0800][2.697s][info][gc,marking  ] GC(16) Concurrent Mark 9.325ms
[2025-12-30T19:39:59.162+0800][2.697s][info][gc,marking  ] GC(16) Concurrent Rebuild Remembered Sets and Scrub Regions
[2025-12-30T19:39:59.165+0800][2.701s][info][gc,marking  ] GC(16) Concurrent Rebuild Remembered Sets and Scrub Regions 3.548ms
```

Cleanup 阶段：决定哪些 Region 可以回收

```log
[2025-12-30T19:39:59.165+0800][2.701s][info][gc,start    ] GC(16) Pause Cleanup
[2025-12-30T19:39:59.165+0800][2.701s][info][gc          ] GC(16) Pause Cleanup 372M->372M(512M) 0.076ms
[2025-12-30T19:39:59.165+0800][2.701s][info][gc,cpu      ] GC(16) User=0.00s Sys=0.00s Real=0.00s
[2025-12-30T19:39:59.165+0800][2.701s][info][gc,marking  ] GC(16) Concurrent Clear Claimed Marks
[2025-12-30T19:39:59.165+0800][2.701s][info][gc,marking  ] GC(16) Concurrent Clear Claimed Marks 0.009ms
[2025-12-30T19:39:59.165+0800][2.701s][info][gc,marking  ] GC(16) Concurrent Cleanup for Next Mark
[2025-12-30T19:39:59.166+0800][2.701s][info][gc,marking  ] GC(16) Concurrent Cleanup for Next Mark 0.323ms
```

最后是并发标记周期正式结束的标志

```log
[2025-12-30T19:39:59.166+0800][2.701s][info][gc          ] GC(16) Concurrent Mark Cycle 21.601ms
```

## 为之后的 Mixed GC 做准备

这是一轮 G1 的 Young GC，但标注为 Pause Young (Prepare Mixed)，说明前面的并发标记已经完成，这次 Young GC 在为后续 Mixed GC 做准备，并且已经开始回收一部分 Old 区，因此能看到 Old regions 从 328 降到 263。

```log
[2025-12-30T19:39:59.232+0800][2.768s][info][gc,start    ] GC(17) Pause Young (Prepare Mixed) (G1 Evacuation Pause)
[2025-12-30T19:39:59.232+0800][2.768s][info][gc,task     ] GC(17) Using 11 workers of 11 for evacuation
[2025-12-30T19:39:59.234+0800][2.769s][info][gc,phases   ] GC(17)   Pre Evacuate Collection Set: 0.20ms
[2025-12-30T19:39:59.234+0800][2.769s][info][gc,phases   ] GC(17)   Merge Heap Roots: 0.09ms
[2025-12-30T19:39:59.234+0800][2.769s][info][gc,phases   ] GC(17)   Evacuate Collection Set: 0.91ms
[2025-12-30T19:39:59.234+0800][2.769s][info][gc,phases   ] GC(17)   Post Evacuate Collection Set: 0.21ms
[2025-12-30T19:39:59.234+0800][2.769s][info][gc,phases   ] GC(17)   Other: 0.06ms
[2025-12-30T19:39:59.234+0800][2.769s][info][gc,heap     ] GC(17) Eden regions: 142->0(214)
[2025-12-30T19:39:59.234+0800][2.769s][info][gc,heap     ] GC(17) Survivor regions: 10->8(19)
[2025-12-30T19:39:59.234+0800][2.769s][info][gc,heap     ] GC(17) Old regions: 328->263
[2025-12-30T19:39:59.234+0800][2.769s][info][gc,heap     ] GC(17) Humongous regions: 0->0
[2025-12-30T19:39:59.234+0800][2.770s][info][gc,metaspace] GC(17) Metaspace: 1075K(1216K)->1075K(1216K) NonClass: 1011K(1088K)->1011K(1088K) Class: 63K(128K)->63K(128K)
[2025-12-30T19:39:59.234+0800][2.770s][info][gc          ] GC(17) Pause Young (Prepare Mixed) (G1 Evacuation Pause) 479M->268M(512M) 1.612ms
[2025-12-30T19:39:59.234+0800][2.770s][info][gc,cpu      ] GC(17) User=0.01s Sys=0.01s Real=0.00s
```

## Mixed GC：开始同时回收部分 Old 区

```log
[2025-12-30T19:39:59.384+0800][2.919s][info][gc,start    ] GC(18) Pause Young (Mixed) (G1 Evacuation Pause)
[2025-12-30T19:39:59.384+0800][2.919s][info][gc,task     ] GC(18) Using 11 workers of 11 for evacuation
[2025-12-30T19:39:59.387+0800][2.923s][info][gc,phases   ] GC(18)   Pre Evacuate Collection Set: 0.29ms
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,phases   ] GC(18)   Merge Heap Roots: 0.13ms
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,phases   ] GC(18)   Evacuate Collection Set: 2.87ms
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,phases   ] GC(18)   Post Evacuate Collection Set: 0.32ms
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,phases   ] GC(18)   Other: 0.14ms
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,heap     ] GC(18) Eden regions: 214->0(284)
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,heap     ] GC(18) Survivor regions: 8->19(27)
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,heap     ] GC(18) Old regions: 263->178
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,heap     ] GC(18) Humongous regions: 0->0
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,metaspace] GC(18) Metaspace: 1075K(1216K)->1075K(1216K) NonClass: 1011K(1088K)->1011K(1088K) Class: 63K(128K)->63K(128K)
[2025-12-30T19:39:59.388+0800][2.923s][info][gc          ] GC(18) Pause Young (Mixed) (G1 Evacuation Pause) 482M->195M(512M) 4.094ms
[2025-12-30T19:39:59.388+0800][2.923s][info][gc,cpu      ] GC(18) User=0.02s Sys=0.00s Real=0.00s
```
