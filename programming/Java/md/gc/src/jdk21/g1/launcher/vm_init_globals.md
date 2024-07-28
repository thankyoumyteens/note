# 初始化全局数据

初始化的过程包括:

1. 初始化 Java 基本类型
2. 分配全局事件缓存区，初始化事件队列
3. 初始化全局锁
4. 初始化 JVM 性能统计数据(Perf Data)区，可由 VM 选项 UsePerfData 控制是否开启。若开启 VM 选项 PerfTraceMemOps，可在初始化时打印该空间的分配信息

```cpp
// --- src/hotspot/share/runtime/threads.cpp#create_vm --- //

// Initialize global data structures and create system classes in heap
vm_init_globals();

// --- src/hotspot/share/runtime/init.cpp --- //

void vm_init_globals() {
  check_ThreadShadow();
  basic_types_init();
  eventlog_init();
  mutex_init();
  universe_oopstorage_init();
  perfMemory_init();
  SuspendibleThreadSet_init();
}
```
