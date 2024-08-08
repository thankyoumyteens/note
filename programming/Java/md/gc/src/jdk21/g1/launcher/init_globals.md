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

1. Management 模块: 启动名为 `Service Thread` 的守护线程。若系统开启了选项-XX: ManagementServer, 则加载并创建 `sun.management.Agent` 类, 执行其 startAgent 方法启动 JMX Server
2. RuntimeService 模块: 提供运行时模块的性能监控和管理服务, 如 applicationTime, jvmCapabilities 等
3. ThreadService 模块: 提供线程和内部同步系统的性能监控和管理服务, 包括维护线程列表、线程相关的性能统计、线程快照、线程堆栈跟踪和线程转储等功能
4. ClassLoadingService: 提供类加载模块的性能监控和管理服务

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

Code Cache 是指代码高速缓存, 主要用来生成和存储本地代码。这些代码片段包括已编译好的 Java 方法和 RuntimeStubs 等。

通过 VM 选项 CodeCacheExpansionSize, InitialCodeCacheSize 和 ReservedCodeCacheSize 可以配置该空间大小。

```cpp
// --- src/hotspot/share/code/codeCache.cpp --- //

void codeCache_init() {
  CodeCache::initialize();
}
```

## StubRoutines

`StubRoutines` 主要用于处理那些不能直接通过编译后的字节码指令完成的操作。它提供了一系列的“stub”方法或例程, 这些方法通常是由 JVM 调用来执行特定的任务。

比如: 

1. 当 JVM 需要调用一个方法, 但该方法的实际地址未知时（例如, 在接口方法调用或虚方法调用中）, 会使用 stub 来间接进行调用
2. 当字节码指令遇到可能抛出异常的情况时, 如除以零、数组越界等, 会跳转到相应的 stub 例程来处理异常
3. 在运行时, JIT 编译器可能会生成特定的代码段来替代原有的解释执行过程, 这些代码段也被称为 stubs

```cpp
// --- src/hotspot/share/runtime/stubRoutines.cpp --- //

void initial_stubs_init()      { StubRoutines::initialize_initial_stubs(); }

// must happen before universe::genesis
void StubRoutines::initialize_initial_stubs() {
  if (_initial_stubs_code == nullptr) {
    _initial_stubs_code = initialize_stubs(StubCodeGenerator::Initial_stubs,
                                           _initial_stubs_code_size, 10,
                                           "StubRoutines generation initial stubs",
                                           "StubRoutines (initial stubs)",
                                           "_initial_stubs_code_size");
  }
}

static BufferBlob* initialize_stubs(StubCodeGenerator::StubsKind kind,
                                    int code_size, int max_aligned_stubs,
                                    const char* timer_msg,
                                    const char* buffer_name,
                                    const char* assert_msg) {
  ResourceMark rm;
  TraceTime timer(timer_msg, TRACETIME_LOG(Info, startuptime));
  // Add extra space for large CodeEntryAlignment
  int size = code_size + CodeEntryAlignment * max_aligned_stubs;
  BufferBlob* stubs_code = BufferBlob::create(buffer_name, size);
  if (stubs_code == nullptr) {
    vm_exit_out_of_memory(code_size, OOM_MALLOC_ERROR, "CodeCache: no room for %s", buffer_name);
  }
  CodeBuffer buffer(stubs_code);
  StubGenerator_generate(&buffer, kind);
  // When new stubs added we need to make sure there is some space left
  // to catch situation when we should increase size again.
  assert(code_size == 0 || buffer.insts_remaining() > 200, "increase %s", assert_msg);

  LogTarget(Info, stubs) lt;
  if (lt.is_enabled()) {
    LogStream ls(lt);
    ls.print_cr("%s\t [" INTPTR_FORMAT ", " INTPTR_FORMAT "] used: %d, free: %d",
                buffer_name, p2i(stubs_code->content_begin()), p2i(stubs_code->content_end()),
                buffer.total_content_size(), buffer.insts_remaining());
  }
  return stubs_code;
}
```

## Universe

Universe 模块将按照两个阶段进行初始化。

1. 第一阶段, 根据 VM 选项配置的 GC 策略及算法, 选择垃圾回收器和堆的种类, 初始化堆。根据 VM 选项 UseCompressedOops 进行相关配置。若 VM 选项 UseTLAB 开启 TLAB, 则初始化 TLAB
2. 第二阶段, 将对共享空间进行配置以及初始化 vmSymbols 和 SystemDictionary 等全局数据结构

```cpp
// --- src/hotspot/share/memory/universe.cpp --- //

jint universe_init() {
  assert(!Universe::_fully_initialized, "called after initialize_vtables");
  guarantee(1 << LogHeapWordSize == sizeof(HeapWord),
         "LogHeapWordSize is incorrect.");
  guarantee(sizeof(oop) >= sizeof(HeapWord), "HeapWord larger than oop?");
  guarantee(sizeof(oop) % sizeof(HeapWord) == 0,
            "oop size is not not a multiple of HeapWord size");

  TraceTime timer("Genesis", TRACETIME_LOG(Info, startuptime));

  initialize_global_behaviours();

  GCLogPrecious::initialize();

#ifdef _LP64
  MetaspaceShared::adjust_heap_sizes_for_dumping();
#endif // _LP64

  GCConfig::arguments()->initialize_heap_sizes();

  jint status = Universe::initialize_heap();
  if (status != JNI_OK) {
    return status;
  }

  Universe::initialize_tlab();

  Metaspace::global_initialize();

  // Initialize performance counters for metaspaces
  MetaspaceCounters::initialize_performance_counters();

  // Checks 'AfterMemoryInit' constraints.
  if (!JVMFlagLimit::check_all_constraints(JVMFlagConstraintPhase::AfterMemoryInit)) {
    return JNI_EINVAL;
  }

  // Create memory for metadata.  Must be after initializing heap for
  // DumpSharedSpaces.
  ClassLoaderData::init_null_class_loader_data();

  // We have a heap so create the Method* caches before
  // Metaspace::initialize_shared_spaces() tries to populate them.
  Universe::_finalizer_register_cache = new LatestMethodCache();
  Universe::_loader_addClass_cache    = new LatestMethodCache();
  Universe::_throw_illegal_access_error_cache = new LatestMethodCache();
  Universe::_throw_no_such_method_error_cache = new LatestMethodCache();
  Universe::_do_stack_walk_cache = new LatestMethodCache();

#if INCLUDE_CDS
  DynamicArchive::check_for_dynamic_dump();
  if (UseSharedSpaces) {
    // Read the data structures supporting the shared spaces (shared
    // system dictionary, symbol table, etc.)
    MetaspaceShared::initialize_shared_spaces();
  }
  if (Arguments::is_dumping_archive()) {
    MetaspaceShared::prepare_for_dumping();
  }
#endif

  SymbolTable::create_table();
  StringTable::create_table();

  if (strlen(VerifySubSet) > 0) {
    Universe::initialize_verify_flags();
  }

  ResolvedMethodTable::create_table();

  return JNI_OK;
}
```

## 解释器

初始化解释器(interpreter), 并注册 StubQueue。解释器初始化分为两部分, 另一部分在 `init_globals2` 函数中。

```cpp
// --- src/hotspot/share/interpreter/interpreter.cpp --- //

// The reason that interpreter initialization is split into two parts is that the first part
// needs to run before methods are loaded (which with CDS implies linked also), and the other
// part needs to run after. The reason is that when methods are loaded (with CDS) or linked
// (without CDS), the i2c adapters are generated that assert we are currently in the interpreter.
// Asserting that requires knowledge about where the interpreter is in memory. Therefore,
// establishing the interpreter address must be done before methods are loaded. However,
// we would like to actually generate the interpreter after methods are loaded. That allows
// us to remove otherwise hardcoded offsets regarding fields that are needed in the interpreter
// code. This leads to a split if 1. reserving the memory for the interpreter, 2. loading methods
// and 3. generating the interpreter.
void interpreter_init_stub() {
  Interpreter::initialize_stub();
}
```

## 模板表

初始化模板表模块, 将创建模版解释器使用的模板表。
