# 初始化 OS 模块

OS 模块的初始化包括两个环节:

1. `init()` 函数：第一次初始化的时机是在全局参数传入之前
2. `init_2()` 函数：第二次初始化是在全局参数传入之后

## init

第一次初始化能够完成一些固定的配置，主要包括以下几项内容:

1. 设置页大小
2. 设置处理器数量
3. 初始化 proc，打开“/proc/$pid”
4. 获得物理内存大小，保存在全局变量 `_physical_memory` 中
5. 获得原生主线程的句柄：获得指向原生线程的指针，并将其保存在全局变量 `_main_thread` 中
6. 系统时钟初始化

```cpp
// --- src/hotspot/os/bsd/os_bsd.cpp --- //

// this is called _before_ the most of global arguments have been parsed
void os::init(void) {
  char dummy;   // used to get a guess on initial stack address

  size_t page_size = (size_t)getpagesize();
  OSInfo::set_vm_page_size(page_size);
  OSInfo::set_vm_allocation_granularity(page_size);
  if (os::vm_page_size() == 0) {
    fatal("os_bsd.cpp: os::init: getpagesize() failed (%s)", os::strerror(errno));
  }
  _page_sizes.add(os::vm_page_size());

  Bsd::initialize_system_info();

  // _main_thread points to the thread that created/loaded the JVM.
  Bsd::_main_thread = pthread_self();

  Bsd::clock_init();

  os::Posix::init();
}

void os::Bsd::initialize_system_info() {
  int mib[2];
  size_t len;
  int cpu_val;
  julong mem_val;

  // get processors count via hw.ncpus sysctl
  mib[0] = CTL_HW;
  mib[1] = HW_NCPU;
  len = sizeof(cpu_val);
  if (sysctl(mib, 2, &cpu_val, &len, nullptr, 0) != -1 && cpu_val >= 1) {
    assert(len == sizeof(cpu_val), "unexpected data size");
    set_processor_count(cpu_val);
  } else {
    set_processor_count(1);   // fallback
  }

#if defined(__APPLE__) && defined(__x86_64__)
  // initialize processor id map
  for (int i = 0; i < processor_id_map_size; i++) {
    processor_id_map[i] = processor_id_unassigned;
  }
#endif

  // get physical memory via hw.memsize sysctl (hw.memsize is used
  // since it returns a 64 bit value)
  mib[0] = CTL_HW;

#if defined (HW_MEMSIZE) // Apple
  mib[1] = HW_MEMSIZE;
#elif defined(HW_PHYSMEM) // Most of BSD
  mib[1] = HW_PHYSMEM;
#elif defined(HW_REALMEM) // Old FreeBSD
  mib[1] = HW_REALMEM;
#else
  #error No ways to get physmem
#endif

  len = sizeof(mem_val);
  if (sysctl(mib, 2, &mem_val, &len, nullptr, 0) != -1) {
    assert(len == sizeof(mem_val), "unexpected data size");
    _physical_memory = mem_val;
  } else {
    _physical_memory = 256 * 1024 * 1024;       // fallback (XXXBSD?)
  }

#ifdef __OpenBSD__
  {
    // limit _physical_memory memory view on OpenBSD since
    // datasize rlimit restricts us anyway.
    struct rlimit limits;
    getrlimit(RLIMIT_DATA, &limits);
    _physical_memory = MIN2(_physical_memory, (julong)limits.rlim_cur);
  }
#endif
}
```

## init_2

OS 模块还有一部分配置是允许外部参数进行控制的。当解析完全局参数后，就可以根据参数进行配置。

1. 快速线程时钟初始化
2. 使用 mmap 分配共享内存，配置大页内存
3. 初始化内核信号，安装信号处理函数 SR_handler，用作线程执行过程中的 suspended/resumed 处理。操作系统信号(signal)，作为进程间通信的一种手段，用来通知进程发生了某种类型的系统事件
4. 配置线程栈：设置栈大小、分配线程初始栈等
5. 设置文件描述符数量
6. 初始化时钟，用来串行化线程创建
7. 向系统注册 atexit 函数
8. 初始化线程优先级策略

```cpp
// --- src/hotspot/os/bsd/os_bsd.cpp --- //

// this is called _after_ the global arguments have been parsed
jint os::init_2(void) {

  // This could be set after os::Posix::init() but all platforms
  // have to set it the same so we have to mirror Solaris.
  DEBUG_ONLY(os::set_mutex_init_done();)

  os::Posix::init_2();

  if (PosixSignals::init() == JNI_ERR) {
    return JNI_ERR;
  }

  // Check and sets minimum stack sizes against command line options
  if (set_minimum_stack_sizes() == JNI_ERR) {
    return JNI_ERR;
  }

  // Not supported.
  FLAG_SET_ERGO(UseNUMA, false); // 使用NUMA
  FLAG_SET_ERGO(UseNUMAInterleaving, false);

  // 最大文件描述符数量
  if (MaxFDLimit) {
    // set the number of file descriptors to max. print out error
    // if getrlimit/setrlimit fails but continue regardless.
    struct rlimit nbr_files;
    int status = getrlimit(RLIMIT_NOFILE, &nbr_files);
    if (status != 0) {
      log_info(os)("os::init_2 getrlimit failed: %s", os::strerror(errno));
    } else {
      nbr_files.rlim_cur = nbr_files.rlim_max;

#ifdef __APPLE__
      // Darwin returns RLIM_INFINITY for rlim_max, but fails with EINVAL if
      // you attempt to use RLIM_INFINITY. As per setrlimit(2), OPEN_MAX must
      // be used instead
      nbr_files.rlim_cur = MIN(OPEN_MAX, nbr_files.rlim_cur);
#endif

      status = setrlimit(RLIMIT_NOFILE, &nbr_files);
      if (status != 0) {
        log_info(os)("os::init_2 setrlimit failed: %s", os::strerror(errno));
      }
    }
  }

  // at-exit methods are called in the reverse order of their registration.
  // atexit functions are called on return from main or as a result of a
  // call to exit(3C). There can be only 32 of these functions registered
  // and atexit() does not set errno.

  // 允许向系统注册atexit函数
  if (PerfAllowAtExitRegistration) {
    // only register atexit functions if PerfAllowAtExitRegistration is set.
    // atexit functions can be delayed until process exit time, which
    // can be problematic for embedded VM situations. Embedded VMs should
    // call DestroyJavaVM() to assure that VM resources are released.

    // note: perfMemory_exit_helper atexit function may be removed in
    // the future if the appropriate cleanup code can be added to the
    // VM_Exit VMOperation's doit method.
    if (atexit(perfMemory_exit_helper) != 0) {
      warning("os::init_2 atexit(perfMemory_exit_helper) failed");
    }
  }

  // initialize thread priority policy
  prio_init();

#ifdef __APPLE__
  // dynamically link to objective c gc registration
  void *handleLibObjc = dlopen(OBJC_LIB, RTLD_LAZY);
  if (handleLibObjc != nullptr) {
    objc_registerThreadWithCollectorFunction = (objc_registerThreadWithCollector_t) dlsym(handleLibObjc, OBJC_GCREGISTER);
  }
#endif

  return JNI_OK;
}

// -- src/hotspot/os/posix/signals_posix.cpp -- //

int PosixSignals::init() {
  // initialize suspend/resume support - must do this before signal_sets_init()
  if (SR_initialize() != 0) {
    vm_exit_during_initialization("SR_initialize failed");
    return JNI_ERR;
  }

  signal_sets_init();

  // Initialize data for jdk.internal.misc.Signal and BREAK_SIGNAL's handler.
  if (!ReduceSignalUsage) {
    jdk_misc_signal_init();
  }

  install_signal_handlers();

  return JNI_OK;
}
```
