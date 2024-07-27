# 启动线程

JDK 中的 6 种线程状态:

1. NEW: 新创建但尚未启动的线程处于这种状态。通过 new 关键字创建了 `java.lang.Thread` 类(或其子类)的对象
2. BLOCKED: 线程受阻塞并等待某个监视器对象锁。当线程执行 synchronized 方法或代码块, 但未获得相应对象锁时处于这种状态
3. RUNNABLE: 正在 Java 虚拟机中执行的线程处于这种状态。有三种情形:
   - 一种情形是 Thread 类的对象调用了 `start()` 函数, 这时的线程就等待时间片轮转到自己, 以便获得 CPU
   - 另一种情形是线程在处于 RUNNABLE 状态时并没有运行完自己的 `run()` 函数, 时间片用完之后回到 RUNNABLE 状态
   - 还有一种情形就是处于 BLOCKED 状态的线程结束了当前的 BLOCKED 状态之后重新回到 RUNNABLE 状态
4. TERMINATED: 已退出的线程处于这种状态
5. TIMED_WAITING: 等待另一个线程来执行某一特定操作, 需要指定等待时间, 不会无限期地等待
6. WAITING: 无限期地等待另一个线程来执行某一特定操作

在 JVM 层面, HotSpot 内部定义了线程的 5 种基本状态:

1. `-thread_new`: 表示刚启动, 正处在初始化过程中
2. `-thread_in_native`: 表示运行本地代码
3. `-thread_in_vm`: 表示在 VM 中运行
4. `-thread_in_Java`: 表示运行 Java 代码
5. `-thread_blocked`: 表示阻塞

为了支持内部状态转换，还补充定义了其他几种过渡状态：`_<thread_state_type>_trans`，其中 thread_state_type 分别表示上述 5 种基本状态类型。

在 HotSpot 中，定义了如下几种线程类型:

```cpp
// --- src/hotspot/share/runtime/os.hpp --- //

enum ThreadType {
  vm_thread,
  gc_thread,         // GC thread
  java_thread,       // Java, JVMTIAgent and Service threads.
  compiler_thread,
  watcher_thread,
  asynclog_thread,   // dedicated to flushing logs
  os_thread
};
```

## 创建 Java 主线程

主线程(main thread)是执行 `public static void main (String[] args)` 方法的线程。对应 OS 线程 ID 为 1 的名为 `main` 的线程。

系统初始化时，虚拟机首先创建的线程就是主线程。

```cpp
// --- src/hotspot/share/runtime/threads.cpp#create_vm --- //

// Attach the main thread to this os thread
JavaThread* main_thread = new JavaThread();
main_thread->set_thread_state(_thread_in_vm);
main_thread->initialize_thread_current();
// must do this before set_active_handles
main_thread->record_stack_base_and_size();
main_thread->register_thread_stack_with_NMT();
main_thread->set_active_handles(JNIHandleBlock::allocate_block());
MACOS_AARCH64_ONLY(main_thread->init_wx());

if (!main_thread->set_as_starting_thread()) {
  vm_shutdown_during_initialization(
                                    "Failed necessary internal allocation. Out of swap space");
  main_thread->smr_delete();
  *canTryAgain = false; // don't let caller call JNI_CreateJavaVM again
  return JNI_ENOMEM;
}

// Enable guard page *after* os::create_main_thread(), otherwise it would
// crash Linux VM, see notes in os_linux.cpp.
main_thread->stack_overflow_state()->create_stack_guard_pages();
```

1. JVM 创建一个 JavaThread 类型的线程变量(刚创建时状态为 `_thread_new`)
2. 将线程状态设置为 `_thread_in_vm`，表明该线程正处于在 JVM 中执行的状态
3. 记录线程栈的基址和大小, 初始化线程本地存储区(TLS)
4. 为线程设置 JNI 句柄
5. 通过 OS 模块创建原始线程(OSThread), 并设置为可运行状态
6. 初始化主线程栈

现在 main_thread 实际上是一个 JVM 内部线程，其状态为 JVM 内部定义的线程状态 `_thread_in_vm`。

接下来需要把它对应到 java 层的 java.lang.Thread

```cpp
// --- src/hotspot/share/runtime/threads.cpp#create_vm --- //

initialize_java_lang_classes(main_thread, CHECK_JNI_ERR);

// --- src/hotspot/share/runtime/threads.cpp --- //

void Threads::initialize_java_lang_classes(JavaThread* main_thread, TRAPS) {
  TraceTime timer("Initialize java.lang classes", TRACETIME_LOG(Info, startuptime));

  initialize_class(vmSymbols::java_lang_String(), CHECK);

  // Inject CompactStrings value after the static initializers for String ran.
  java_lang_String::set_compact_strings(CompactStrings);

  // Initialize java_lang.System (needed before creating the thread)
  initialize_class(vmSymbols::java_lang_System(), CHECK);
  // The VM creates & returns objects of this class. Make sure it's initialized.
  initialize_class(vmSymbols::java_lang_Class(), CHECK);
  initialize_class(vmSymbols::java_lang_ThreadGroup(), CHECK);
  Handle thread_group = create_initial_thread_group(CHECK);
  Universe::set_main_thread_group(thread_group());
  initialize_class(vmSymbols::java_lang_Thread(), CHECK);
  create_initial_thread(thread_group, main_thread, CHECK);

  // The VM creates objects of this class.
  initialize_class(vmSymbols::java_lang_Module(), CHECK);

#ifdef ASSERT
  InstanceKlass *k = vmClasses::UnsafeConstants_klass();
  assert(k->is_not_initialized(), "UnsafeConstants should not already be initialized");
#endif

  // initialize the hardware-specific constants needed by Unsafe
  initialize_class(vmSymbols::jdk_internal_misc_UnsafeConstants(), CHECK);
  jdk_internal_misc_UnsafeConstants::set_unsafe_constants();

  // The VM preresolves methods to these classes. Make sure that they get initialized
  initialize_class(vmSymbols::java_lang_reflect_Method(), CHECK);
  initialize_class(vmSymbols::java_lang_ref_Finalizer(), CHECK);

  // Phase 1 of the system initialization in the library, java.lang.System class initialization
  call_initPhase1(CHECK);

  // Get the Java runtime name, version, and vendor info after java.lang.System is initialized.
  // Some values are actually configure-time constants but some can be set via the jlink tool and
  // so must be read dynamically. We treat them all the same.
  InstanceKlass* ik = SystemDictionary::find_instance_klass(THREAD, vmSymbols::java_lang_VersionProps(),
                                                            Handle(), Handle());
  {
    ResourceMark rm(main_thread);
    JDK_Version::set_java_version(get_java_version_info(ik, vmSymbols::java_version_name()));

    JDK_Version::set_runtime_name(get_java_version_info(ik, vmSymbols::java_runtime_name_name()));

    JDK_Version::set_runtime_version(get_java_version_info(ik, vmSymbols::java_runtime_version_name()));

    JDK_Version::set_runtime_vendor_version(get_java_version_info(ik, vmSymbols::java_runtime_vendor_version_name()));

    JDK_Version::set_runtime_vendor_vm_bug_url(get_java_version_info(ik, vmSymbols::java_runtime_vendor_vm_bug_url_name()));
  }

  // an instance of OutOfMemory exception has been allocated earlier
  initialize_class(vmSymbols::java_lang_OutOfMemoryError(), CHECK);
  initialize_class(vmSymbols::java_lang_NullPointerException(), CHECK);
  initialize_class(vmSymbols::java_lang_ClassCastException(), CHECK);
  initialize_class(vmSymbols::java_lang_ArrayStoreException(), CHECK);
  initialize_class(vmSymbols::java_lang_ArithmeticException(), CHECK);
  initialize_class(vmSymbols::java_lang_StackOverflowError(), CHECK);
  initialize_class(vmSymbols::java_lang_IllegalMonitorStateException(), CHECK);
  initialize_class(vmSymbols::java_lang_IllegalArgumentException(), CHECK);
}

// Creates the initial Thread, and sets it to running.
static void create_initial_thread(Handle thread_group, JavaThread* thread,
                                 TRAPS) {
  InstanceKlass* ik = vmClasses::Thread_klass();
  assert(ik->is_initialized(), "must be");
  instanceHandle thread_oop = ik->allocate_instance_handle(CHECK);

  // Cannot use JavaCalls::construct_new_instance because the java.lang.Thread
  // constructor calls Thread.current(), which must be set here for the
  // initial thread.
  java_lang_Thread::set_thread(thread_oop(), thread);
  thread->set_threadOopHandles(thread_oop());

  Handle string = java_lang_String::create_from_str("main", CHECK);

  JavaValue result(T_VOID);
  JavaCalls::call_special(&result, thread_oop,
                          ik,
                          vmSymbols::object_initializer_name(),
                          vmSymbols::threadgroup_string_void_signature(),
                          thread_group,
                          string,
                          CHECK);

  // Set thread status to running since main thread has
  // been started and running.
  java_lang_Thread::set_thread_status(thread_oop(),
                                      JavaThreadStatus::RUNNABLE);
}
```

## 创建 VMThread

VMThread 是在 JVM 内部执行 VMOperation 的线程。VMOperation 实现了 JVM 内部的核心操作。当 VMThread 线程创建成功后，在整个运行期间不断等待, 接受并执行指定的 VMOperation。

```cpp
// --- src/hotspot/share/runtime/threads.cpp#create_vm --- //

// Create the VMThread
{ TraceTime timer("Start VMThread", TRACETIME_LOG(Info, startuptime));

  VMThread::create();
  VMThread* vmthread = VMThread::vm_thread();

  if (!os::create_thread(vmthread, os::vm_thread)) {
    vm_exit_during_initialization("Cannot create VM thread. "
                                  "Out of system resources.");
  }

  // Wait for the VM thread to become ready, and VMThread::run to initialize
  // Monitors can have spurious returns, must always check another state flag
  {
    MonitorLocker ml(Notify_lock);
    os::start_thread(vmthread);
    while (!vmthread->is_running()) {
      ml.wait();
    }
  }
}
```

## 创建守护线程

守护线程包括 `Signal Dispatcher`, `Attach Listener`, `Watcher Thread` 等。
