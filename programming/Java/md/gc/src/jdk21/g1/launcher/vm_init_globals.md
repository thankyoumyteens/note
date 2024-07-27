# 初始化全局数据

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
