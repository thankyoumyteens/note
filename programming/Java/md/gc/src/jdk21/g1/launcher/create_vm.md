# create_vm

系统初始化的具体步骤:

1. 初始化输出流模块
2. 配置 Launcher 属性
3. 初始化 OS 模块
4. 配置系统属性
5. 程序参数和虚拟机选项解析
6. 根据传入的参数继续初始化 OS 模块
7. 配置 GC 日志输出流模块
8. 加载代理(agent)库
9. 初始化线程队列
10. 初始化 TLS(ThreadLocalStorage) 模块
11. 调用 vm_init_globals 函数初始化全局数据结构
12. 创建主线程并加入线程队列
13. 创建虚拟机线程
14. 初始化 JDK 核心类,如 java.lang.String、java.util.HashMap 等
15. 初始化系统类加载器模块，并初始化系统字典
16. 启动 SLT(SurrogateLockerThread)线程
17. 启动 Signal Dispatcher 线程
18. 启动 Attach Listener 线程
19. 初始化即时编译器
20. 初始化 Chunk 模块
21. 初始化 Management 模块，启动 Service Thread 线程
22. 启动 Watcher Thread 线程

```cpp
// --- src/hotspot/share/runtime/threads.cpp --- //

jint Threads::create_vm(JavaVMInitArgs* args, bool* canTryAgain) {
  extern void JDK_Version_init();

  // Preinitialize version info.
  VM_Version::early_initialize();

  // Check version
  if (!is_supported_jni_version(args->version)) return JNI_EVERSION;

  // Initialize library-based TLS
  ThreadLocalStorage::init();

  // Initialize the output stream module
  ostream_init();

  // Process java launcher properties.
  Arguments::process_sun_java_launcher_properties(args);

  // Initialize the os module
  os::init();

  MACOS_AARCH64_ONLY(os::current_thread_enable_wx(WXWrite));

  // Record VM creation timing statistics
  TraceVmCreationTime create_vm_timer;
  create_vm_timer.start();

  // Initialize system properties.
  Arguments::init_system_properties();

  // So that JDK version can be used as a discriminator when parsing arguments
  JDK_Version_init();

  // Update/Initialize System properties after JDK version number is known
  Arguments::init_version_specific_system_properties();

  // Make sure to initialize log configuration *before* parsing arguments
  LogConfiguration::initialize(create_vm_timer.begin_time());

  // Parse arguments
  // Note: this internally calls os::init_container_support()
  jint parse_result = Arguments::parse(args);
  if (parse_result != JNI_OK) return parse_result;

  // Initialize NMT right after argument parsing to keep the pre-NMT-init window small.
  MemTracker::initialize();

  os::init_before_ergo();

  jint ergo_result = Arguments::apply_ergo();
  if (ergo_result != JNI_OK) return ergo_result;

  // Final check of all ranges after ergonomics which may change values.
  if (!JVMFlagLimit::check_all_ranges()) {
    return JNI_EINVAL;
  }

  // Final check of all 'AfterErgo' constraints after ergonomics which may change values.
  bool constraint_result = JVMFlagLimit::check_all_constraints(JVMFlagConstraintPhase::AfterErgo);
  if (!constraint_result) {
    return JNI_EINVAL;
  }

  if (PauseAtStartup) {
    os::pause();
  }

  HOTSPOT_VM_INIT_BEGIN();

  // Timing (must come after argument parsing)
  TraceTime timer("Create VM", TRACETIME_LOG(Info, startuptime));

  // Initialize the os module after parsing the args
  jint os_init_2_result = os::init_2();
  if (os_init_2_result != JNI_OK) return os_init_2_result;

#ifdef CAN_SHOW_REGISTERS_ON_ASSERT
  // Initialize assert poison page mechanism.
  if (ShowRegistersOnAssert) {
    initialize_assert_poison();
  }
#endif // CAN_SHOW_REGISTERS_ON_ASSERT

  SafepointMechanism::initialize();

  jint adjust_after_os_result = Arguments::adjust_after_os();
  if (adjust_after_os_result != JNI_OK) return adjust_after_os_result;

  // Initialize output stream logging
  ostream_init_log();

  // Launch -agentlib/-agentpath and converted -Xrun agents
  JvmtiAgentList::load_agents();

  // Initialize Threads state
  _number_of_threads = 0;
  _number_of_non_daemon_threads = 0;

  // Initialize global data structures and create system classes in heap
  vm_init_globals();

#if INCLUDE_JVMCI
  if (JVMCICounterSize > 0) {
    JavaThread::_jvmci_old_thread_counters = NEW_C_HEAP_ARRAY(jlong, JVMCICounterSize, mtJVMCI);
    memset(JavaThread::_jvmci_old_thread_counters, 0, sizeof(jlong) * JVMCICounterSize);
  } else {
    JavaThread::_jvmci_old_thread_counters = nullptr;
  }
#endif // INCLUDE_JVMCI

  // Initialize OopStorage for threadObj
  JavaThread::_thread_oop_storage = OopStorageSet::create_strong("Thread OopStorage", mtThread);

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

  // Initialize Java-Level synchronization subsystem
  ObjectMonitor::Initialize();
  ObjectSynchronizer::initialize();

  // Initialize global modules
  jint status = init_globals();
  if (status != JNI_OK) {
    main_thread->smr_delete();
    *canTryAgain = false; // don't let caller call JNI_CreateJavaVM again
    return status;
  }

  // Create WatcherThread as soon as we can since we need it in case
  // of hangs during error reporting.
  WatcherThread::start();

  // Add main_thread to threads list to finish barrier setup with
  // on_thread_attach.  Should be before starting to build Java objects in
  // init_globals2, which invokes barriers.
  {
    MutexLocker mu(Threads_lock);
    Threads::add(main_thread);
  }

  status = init_globals2();
  if (status != JNI_OK) {
    Threads::remove(main_thread, false);
    // It is possible that we managed to fully initialize Universe but have then
    // failed by throwing an exception. In that case our caller JNI_CreateJavaVM
    // will want to report it, so we can't delete the main thread.
    if (!main_thread->has_pending_exception()) {
      main_thread->smr_delete();
    }
    *canTryAgain = false; // don't let caller call JNI_CreateJavaVM again
    return status;
  }

  JFR_ONLY(Jfr::on_create_vm_1();)

  // Should be done after the heap is fully created
  main_thread->cache_global_variables();

  // Any JVMTI raw monitors entered in onload will transition into
  // real raw monitor. VM is setup enough here for raw monitor enter.
  JvmtiExport::transition_pending_onload_raw_monitors();

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

  assert(Universe::is_fully_initialized(), "not initialized");
  if (VerifyDuringStartup) {
    // Make sure we're starting with a clean slate.
    VM_Verify verify_op;
    VMThread::execute(&verify_op);
  }

  // We need this to update the java.vm.info property in case any flags used
  // to initially define it have been changed. This is needed for both CDS
  // since UseSharedSpaces may be changed after java.vm.info
  // is initially computed. See Abstract_VM_Version::vm_info_string().
  // This update must happen before we initialize the java classes, but
  // after any initialization logic that might modify the flags.
  Arguments::update_vm_info_property(VM_Version::vm_info_string());

  JavaThread* THREAD = JavaThread::current(); // For exception macros.
  HandleMark hm(THREAD);

  // Always call even when there are not JVMTI environments yet, since environments
  // may be attached late and JVMTI must track phases of VM execution
  JvmtiExport::enter_early_start_phase();

  // Notify JVMTI agents that VM has started (JNI is up) - nop if no agents.
  JvmtiExport::post_early_vm_start();

  // Launch -Xrun agents early if EagerXrunInit is set
  if (EagerXrunInit) {
    JvmtiAgentList::load_xrun_agents();
  }

  initialize_java_lang_classes(main_thread, CHECK_JNI_ERR);

  quicken_jni_functions();

  // No more stub generation allowed after that point.
  StubCodeDesc::freeze();

  // Set flag that basic initialization has completed. Used by exceptions and various
  // debug stuff, that does not work until all basic classes have been initialized.
  set_init_completed();

  LogConfiguration::post_initialize();
  Metaspace::post_initialize();
  MutexLocker::post_initialize();

  HOTSPOT_VM_INIT_END();

  // record VM initialization completion time
#if INCLUDE_MANAGEMENT
  Management::record_vm_init_completed();
#endif // INCLUDE_MANAGEMENT

  log_info(os)("Initialized VM with process ID %d", os::current_process_id());

  // Signal Dispatcher needs to be started before VMInit event is posted
  os::initialize_jdk_signal_support(CHECK_JNI_ERR);

  // Start Attach Listener if +StartAttachListener or it can't be started lazily
  if (!DisableAttachMechanism) {
    AttachListener::vm_start();
    if (StartAttachListener || AttachListener::init_at_startup()) {
      AttachListener::init();
    }
  }

  // Launch -Xrun agents if EagerXrunInit is not set.
  if (!EagerXrunInit) {
    JvmtiAgentList::load_xrun_agents();
  }

  Chunk::start_chunk_pool_cleaner_task();

  // Start the service thread
  // The service thread enqueues JVMTI deferred events and does various hashtable
  // and other cleanups.  Needs to start before the compilers start posting events.
  ServiceThread::initialize();

  // Start the monitor deflation thread:
  MonitorDeflationThread::initialize();

  // initialize compiler(s)
#if defined(COMPILER1) || COMPILER2_OR_JVMCI
#if INCLUDE_JVMCI
  bool force_JVMCI_intialization = false;
  if (EnableJVMCI) {
    // Initialize JVMCI eagerly when it is explicitly requested.
    // Or when JVMCILibDumpJNIConfig or JVMCIPrintProperties is enabled.
    force_JVMCI_intialization = EagerJVMCI || JVMCIPrintProperties || JVMCILibDumpJNIConfig;

    if (!force_JVMCI_intialization) {
      // 8145270: Force initialization of JVMCI runtime otherwise requests for blocking
      // compilations via JVMCI will not actually block until JVMCI is initialized.
      force_JVMCI_intialization = UseJVMCICompiler && (!UseInterpreter || !BackgroundCompilation);
    }
  }
#endif
  CompileBroker::compilation_init_phase1(CHECK_JNI_ERR);
  // Postpone completion of compiler initialization to after JVMCI
  // is initialized to avoid timeouts of blocking compilations.
  if (JVMCI_ONLY(!force_JVMCI_intialization) NOT_JVMCI(true)) {
    CompileBroker::compilation_init_phase2();
  }
#endif

  // Start string deduplication thread if requested.
  if (StringDedup::is_enabled()) {
    StringDedup::start();
  }

  // Pre-initialize some JSR292 core classes to avoid deadlock during class loading.
  // It is done after compilers are initialized, because otherwise compilations of
  // signature polymorphic MH intrinsics can be missed
  // (see SystemDictionary::find_method_handle_intrinsic).
  initialize_jsr292_core_classes(CHECK_JNI_ERR);

  // This will initialize the module system.  Only java.base classes can be
  // loaded until phase 2 completes
  call_initPhase2(CHECK_JNI_ERR);

  JFR_ONLY(Jfr::on_create_vm_2();)

  // Always call even when there are not JVMTI environments yet, since environments
  // may be attached late and JVMTI must track phases of VM execution
  JvmtiExport::enter_start_phase();

  // Notify JVMTI agents that VM has started (JNI is up) - nop if no agents.
  JvmtiExport::post_vm_start();

  // Final system initialization including security manager and system class loader
  call_initPhase3(CHECK_JNI_ERR);

  // cache the system and platform class loaders
  SystemDictionary::compute_java_loaders(CHECK_JNI_ERR);

#if INCLUDE_CDS
  // capture the module path info from the ModuleEntryTable
  ClassLoader::initialize_module_path(THREAD);
  if (HAS_PENDING_EXCEPTION) {
    java_lang_Throwable::print(PENDING_EXCEPTION, tty);
    vm_exit_during_initialization("ClassLoader::initialize_module_path() failed unexpectedly");
  }
#endif

#if INCLUDE_JVMCI
  if (force_JVMCI_intialization) {
    JVMCI::initialize_compiler(CHECK_JNI_ERR);
    CompileBroker::compilation_init_phase2();
  }
#endif

  if (NativeHeapTrimmer::enabled()) {
    NativeHeapTrimmer::initialize();
  }

  // Always call even when there are not JVMTI environments yet, since environments
  // may be attached late and JVMTI must track phases of VM execution
  JvmtiExport::enter_live_phase();

  // Make perfmemory accessible
  PerfMemory::set_accessible(true);

  // Notify JVMTI agents that VM initialization is complete - nop if no agents.
  JvmtiExport::post_vm_initialized();

  JFR_ONLY(Jfr::on_create_vm_3();)

#if INCLUDE_MANAGEMENT
  Management::initialize(THREAD);

  if (HAS_PENDING_EXCEPTION) {
    // management agent fails to start possibly due to
    // configuration problem and is responsible for printing
    // stack trace if appropriate. Simply exit VM.
    vm_exit(1);
  }
#endif // INCLUDE_MANAGEMENT

  StatSampler::engage();
  if (CheckJNICalls)                  JniPeriodicChecker::engage();

#if INCLUDE_RTM_OPT
  RTMLockingCounters::init();
#endif

  call_postVMInitHook(THREAD);
  // The Java side of PostVMInitHook.run must deal with all
  // exceptions and provide means of diagnosis.
  if (HAS_PENDING_EXCEPTION) {
    CLEAR_PENDING_EXCEPTION;
  }

  // Let WatcherThread run all registered periodic tasks now.
  // NOTE:  All PeriodicTasks should be registered by now. If they
  //   aren't, late joiners might appear to start slowly (we might
  //   take a while to process their first tick).
  WatcherThread::run_all_tasks();

  create_vm_timer.end();
#ifdef ASSERT
  _vm_complete = true;
#endif

  if (DumpSharedSpaces) {
    MetaspaceShared::preload_and_dump();
    ShouldNotReachHere();
  }

  return JNI_OK;
}
```
