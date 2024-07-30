# 初始化全局模块

init_globals 函数实现了对全局模块的初始化。

```cpp
// --- src/hotspot/share/runtime/threads.cpp#create_vm --- //

// Initialize global modules
jint status = init_globals();
if (status != JNI_OK) {
  main_thread->smr_delete();
  *canTryAgain = false; // don't let caller call JNI_CreateJavaVM again
  return status;
}

// --- src/hotspot/share/runtime/init.cpp --- //

jint init_globals() {
  management_init();
  JvmtiExport::initialize_oop_storage();
  bytecodes_init();
  classLoader_init1();
  compilationPolicy_init();
  codeCache_init();
  VM_Version_init();              // depends on codeCache_init for emitting code
  initial_stubs_init();
  jint status = universe_init();  // dependent on codeCache_init and
                                  // initial_stubs_init and metaspace_init.
  if (status != JNI_OK)
    return status;

#ifdef LEAK_SANITIZER
  {
    // Register the Java heap with LSan.
    VirtualSpaceSummary summary = Universe::heap()->create_heap_space_summary();
    LSAN_REGISTER_ROOT_REGION(summary.start(), summary.reserved_size());
  }
#endif // LEAK_SANITIZER

  AsyncLogWriter::initialize();
  gc_barrier_stubs_init();   // depends on universe_init, must be before interpreter_init
  continuations_init();      // must precede continuation stub generation
  continuation_stubs_init(); // depends on continuations_init
  interpreter_init_stub();   // before methods get loaded
  accessFlags_init();
  InterfaceSupport_init();
  VMRegImpl::set_regName();  // need this before generate_stubs (for printing oop maps).
  SharedRuntime::generate_stubs();
  return JNI_OK;
}
```

## 初始化 JMX

JMX(Java Management Extensions) 用来管理和监测 Java 程序。

JMX 分为 4 个主要模块

1. Management 模块：启动名为 `Service Thread` 的守护线程。若系统开启了选项-XX：ManagementServer，则加载并创建 `sun.management.Agent` 类，执行其 startAgent 方法启动 JMX Server
2. RuntimeService 模块：提供运行时模块的性能监控和管理服务，如 applicationTime, jvmCapabilities 等
3. ThreadService 模块：提供线程和内部同步系统的性能监控和管理服务，包括维护线程列表、线程相关的性能统计、线程快照、线程堆栈跟踪和线程转储等功能
4. ClassLoadingService：提供类加载模块的性能监控和管理服务

```CPP
// --- src/hotspot/share/services/management.cpp --- //

void management_init() {
#if INCLUDE_MANAGEMENT
  Management::init();
  ThreadService::init();
  RuntimeService::init();
  ClassLoadingService::init();
  FinalizerService::init();
#else
  ThreadService::init();
#endif // INCLUDE_MANAGEMENT
}
```

## CodeCache

Code Cache 是指代码高速缓存，主要用来生成和存储本地代码。这些代码片段包括已编译好的 Java 方法和 RuntimeStubs 等。

通过 VM 选项 CodeCacheExpansionSize, InitialCodeCacheSize 和 ReservedCodeCacheSize 可以配置该空间大小。

```cpp
// --- src/hotspot/share/code/codeCache.cpp --- //

void codeCache_init() {
  CodeCache::initialize();
}
```

## StubRoutines
