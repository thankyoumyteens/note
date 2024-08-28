# 初始化

触发初始化的时机:

- 遇到 new, getstatic, putstatic 或 invokestatic 这些需要引用类或接口的指令时
- 初次调用 java.lang.invoke.MethodHandle 实例时，返回结果为 REF_getStatic, REF_putStatic 或 REF_invokeStatic 的方法句柄
- 调用反射方法时，如 Class 类或 java.lang.reflect 包
- 初始化类的子类时
- 类被设计用做 JVM 启动时的初始类

```cpp
// --- src/hotspot/share/oops/instanceKlass.cpp --- //

void InstanceKlass::initialize_impl(TRAPS) {
  HandleMark hm(THREAD);

  // 在初始化过程正式开始之前，必须保证该类型已经完成链接
  // Make sure klass is linked (verified) before initialization
  // A class could already be verified, since it has been reflected upon.
  link_class(CHECK);

  DTRACE_CLASSINIT_PROBE(required, -1);

  bool wait = false;
  bool throw_error = false;

  JavaThread* jt = THREAD;

  // refer to the JVM book page 47 for description of steps
  // Step 1
  {
    // 加锁
    MonitorLocker ml(THREAD, _init_monitor);

    // Step 2
    // 如果此时还有别的线程正在初始化这个instanceKlass(状态：being_initialized)
    // 则进入等待，待当前线程被唤醒后再重复这一步骤
    while (is_being_initialized() && !is_init_thread(jt)) {
      wait = true;
      jt->set_class_to_be_initialized(this);
      ml.wait();
      jt->set_class_to_be_initialized(nullptr);
    }

    // 如果当前线程正在对该类型初始化，则这一定是初始化的一个递归调用，
    // 此时释放class对象上的锁并正常地结束
    // Step 3
    if (is_being_initialized() && is_init_thread(jt)) {
      DTRACE_CLASSINIT_PROBE_WAIT(recursive, -1, wait);
      return;
    }

    // 如果类型已被初始化，则释放class对象上的锁并正常地结束
    // Step 4
    if (is_initialized()) {
      DTRACE_CLASSINIT_PROBE_WAIT(concurrent, -1, wait);
      return;
    }

    // (5)如果instanceKlass处于错误状态,
    // 则释放class对象上的锁并抛出NoClassDefFoundError
    // Step 5
    if (is_in_error_state()) {
      throw_error = true;
    } else {
      // 否则，设置instanceKlass状态为being_initialized，
      // 并释放该instanceKlass对象上的锁
      // Step 6
      set_init_state(being_initialized);
      set_init_thread(jt);
    }
  }

  // Throw error outside lock
  if (throw_error) {
    DTRACE_CLASSINIT_PROBE_WAIT(erroneous, -1, wait);
    ResourceMark rm(THREAD);
    Handle cause(THREAD, get_initialization_error(THREAD));

    stringStream ss;
    ss.print("Could not initialize class %s", external_name());
    if (cause.is_null()) {
      THROW_MSG(vmSymbols::java_lang_NoClassDefFoundError(), ss.as_string());
    } else {
      THROW_MSG_CAUSE(vmSymbols::java_lang_NoClassDefFoundError(),
                      ss.as_string(), cause);
    }
  }

  // Step 7
  // Next, if C is a class rather than an interface, initialize it's super class and super
  // interfaces.
  if (!is_interface()) {
    Klass* super_klass = super();
    if (super_klass != nullptr && super_klass->should_be_initialized()) {
      super_klass->initialize(THREAD);
    }
    // If C implements any interface that declares a non-static, concrete method,
    // the initialization of C triggers initialization of its super interfaces.
    // Only need to recurse if has_nonstatic_concrete_methods which includes declaring and
    // having a superinterface that declares, non-static, concrete methods
    if (!HAS_PENDING_EXCEPTION && has_nonstatic_concrete_methods()) {
      initialize_super_interfaces(THREAD);
    }

    // If any exceptions, complete abruptly, throwing the same exception as above.
    if (HAS_PENDING_EXCEPTION) {
      Handle e(THREAD, PENDING_EXCEPTION);
      CLEAR_PENDING_EXCEPTION;
      {
        EXCEPTION_MARK;
        add_initialization_error(THREAD, e);
        // Locks object, set state, and notify all waiting threads
        set_initialization_state_and_notify(initialization_error, THREAD);
        CLEAR_PENDING_EXCEPTION;
      }
      DTRACE_CLASSINIT_PROBE_WAIT(super__failed, -1, wait);
      THROW_OOP(e());
    }
  }


  // Step 8
  {
    DTRACE_CLASSINIT_PROBE_WAIT(clinit, -1, wait);
    if (class_initializer() != nullptr) {
      // Timer includes any side effects of class initialization (resolution,
      // etc), but not recursive entry into call_class_initializer().
      PerfClassTraceTime timer(ClassLoader::perf_class_init_time(),
                               ClassLoader::perf_class_init_selftime(),
                               ClassLoader::perf_classes_inited(),
                               jt->get_thread_stat()->perf_recursion_counts_addr(),
                               jt->get_thread_stat()->perf_timers_addr(),
                               PerfClassTraceTime::CLASS_CLINIT);
      call_class_initializer(THREAD);
    } else {
      // The elapsed time is so small it's not worth counting.
      if (UsePerfData) {
        ClassLoader::perf_classes_inited()->inc();
      }
      call_class_initializer(THREAD);
    }
  }

  // Step 9
  if (!HAS_PENDING_EXCEPTION) {
    set_initialization_state_and_notify(fully_initialized, THREAD);
    debug_only(vtable().verify(tty, true);)
  }
  else {
    // Step 10 and 11
    Handle e(THREAD, PENDING_EXCEPTION);
    CLEAR_PENDING_EXCEPTION;
    // JVMTI has already reported the pending exception
    // JVMTI internal flag reset is needed in order to report ExceptionInInitializerError
    JvmtiExport::clear_detected_exception(jt);
    {
      EXCEPTION_MARK;
      add_initialization_error(THREAD, e);
      set_initialization_state_and_notify(initialization_error, THREAD);
      CLEAR_PENDING_EXCEPTION;   // ignore any exception thrown, class initialization error is thrown below
      // JVMTI has already reported the pending exception
      // JVMTI internal flag reset is needed in order to report ExceptionInInitializerError
      JvmtiExport::clear_detected_exception(jt);
    }
    DTRACE_CLASSINIT_PROBE_WAIT(error, -1, wait);
    if (e->is_a(vmClasses::Error_klass())) {
      THROW_OOP(e());
    } else {
      JavaCallArguments args(e);
      THROW_ARG(vmSymbols::java_lang_ExceptionInInitializerError(),
                vmSymbols::throwable_void_signature(),
                &args);
    }
  }
  DTRACE_CLASSINIT_PROBE_WAIT(end, -1, wait);
}
```
