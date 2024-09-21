# PerfMemory

JVM 由 PerfMemory 模块管理 Perf Data 区的创建、销毁和分配。PerfMemory 是运行时记录 JVM 信息的载体。

```cpp
// --- src/hotspot/share/runtime/perfMemory.hpp --- //

class PerfMemory : AllStatic {
  private:
    static char*  _start;
    static char*  _end;
    static char*  _top;
    static size_t _capacity;
    static PerfDataPrologue*  _prologue;
    static int    _initialized;
    static bool   _destroyed;
};
```

在虚拟机初始化时，会调用 perfMemory_init 函数初始化 PerfMemory 模块。perfMemory_init 函数实际调用 PerfMemory::initialize 函数对该内存区域初始化。

```cpp
// --- src/hotspot/share/runtime/perfMemory.cpp --- //

void PerfMemory::initialize() {

  if (is_initialized())
    return;

  size_t capacity = align_up((size_t)PerfDataMemorySize,
                             os::vm_allocation_granularity());

  log_debug(perf, memops)("PerfDataMemorySize = %d,"
                          " os::vm_allocation_granularity = " SIZE_FORMAT
                          ", adjusted size = " SIZE_FORMAT,
                          PerfDataMemorySize,
                          os::vm_allocation_granularity(),
                          capacity);

  // 分配PerfData内存区，这块内存用来存放VM性能数据
  // 这块内存在不同os下允许通过不同的方式实现分配，
  // 一般情况下，在linux和windows 下是通过共享内存方式实现的
  create_memory_region(capacity);

  if (_start == nullptr) {

    // the PerfMemory region could not be created as desired. Rather
    // than terminating the JVM, we revert to creating the instrumentation
    // on the C heap. When running in this mode, external monitoring
    // clients cannot attach to and monitor this JVM.
    //
    // the warning is issued only in debug mode in order to avoid
    // additional output to the stdout or stderr output streams.
    //
    // PerfMemory按期望方式(共享内存)分配可能失败，则转向使用C堆malloc分配方式。
    // 运行在此模式下，外部的监控客户端工具则不能attach到JVM
    if (PrintMiscellaneous && Verbose) {
      // debug模式下会输出warning信息
      warning("Could not create PerfData Memory region, reverting to malloc");
    }

    _prologue = NEW_C_HEAP_OBJ(PerfDataPrologue, mtInternal);
  }
  else {

    // PerfMemory已按期望方式创建

    log_debug(perf, memops)("PerfMemory created: address = " INTPTR_FORMAT ","
                            " size = " SIZE_FORMAT,
                            p2i(_start),
                            _capacity);

    _prologue = (PerfDataPrologue *)_start;
    _end = _start + _capacity;
    _top = _start + sizeof(PerfDataPrologue);
  }

  assert(_prologue != nullptr, "prologue pointer must be initialized");

#ifdef VM_LITTLE_ENDIAN
  _prologue->magic = (jint)0xc0c0feca;
  _prologue->byte_order = PERFDATA_LITTLE_ENDIAN;
#else
  _prologue->magic = (jint)0xcafec0c0;
  _prologue->byte_order = PERFDATA_BIG_ENDIAN;
#endif

  _prologue->major_version = PERFDATA_MAJOR_VERSION;
  _prologue->minor_version = PERFDATA_MINOR_VERSION;
  _prologue->accessible = 0;

  _prologue->entry_offset = sizeof(PerfDataPrologue);
  _prologue->num_entries = 0;
  _prologue->used = 0;
  _prologue->overflow = 0;
  _prologue->mod_time_stamp = 0;

  Atomic::release_store(&_initialized, 1);
}
```
