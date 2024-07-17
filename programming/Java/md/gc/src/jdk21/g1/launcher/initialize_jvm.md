# InitializeJVM

```cpp
// --- src/java.base/share/native/libjli/java.c --- //

/*
 * Initializes the Java Virtual Machine. Also frees options array when
 * finished.
 */
static jboolean
InitializeJVM(JavaVM **pvm, JNIEnv **penv, InvocationFunctions *ifn)
{
    JavaVMInitArgs args;
    jint r;

    memset(&args, 0, sizeof(args));
    args.version  = JNI_VERSION_1_2;
    args.nOptions = numOptions;
    args.options  = options;
    args.ignoreUnrecognized = JNI_FALSE;

    if (JLI_IsTraceLauncher()) {
        int i = 0;
        printf("JavaVM args:\n    ");
        printf("version 0x%08lx, ", (long)args.version);
        printf("ignoreUnrecognized is %s, ",
               args.ignoreUnrecognized ? "JNI_TRUE" : "JNI_FALSE");
        printf("nOptions is %ld\n", (long)args.nOptions);
        for (i = 0; i < numOptions; i++)
            printf("    option[%2d] = '%s'\n",
                   i, args.options[i].optionString);
    }

    r = ifn->CreateJavaVM(pvm, (void **)penv, &args);
    JLI_MemFree(options);
    return r == JNI_OK;
}
```

## JNI_CreateJavaVM

创建 JVM 的程序模块是 JNI_CreateJavaVM。

JNI_CreateJavaVM 主要任务是调用 Threads 模块的 create_vm 函数，以完成最终的虚拟机创建和初始化工作。

在 Threads 模块中，实现了对虚拟机各个模块的初始化，以及创建虚拟机线程。

`JavaVM *vm` 和 `JNIEnv *env` 也是在 JNI_CreateJavaVM 中完成赋值的。

```cpp
// --- src/hotspot/share/prims/jni.cpp --- //

_JNI_IMPORT_OR_EXPORT_ jint JNICALL JNI_CreateJavaVM(JavaVM **vm, void **penv, void *args) {
  jint result = JNI_ERR;
  // On Windows, let CreateJavaVM run with SEH protection
#if defined(_WIN32) && !defined(USE_VECTORED_EXCEPTION_HANDLING)
  __try {
#endif
    result = JNI_CreateJavaVM_inner(vm, penv, args);
#if defined(_WIN32) && !defined(USE_VECTORED_EXCEPTION_HANDLING)
  } __except(topLevelExceptionFilter((_EXCEPTION_POINTERS*)_exception_info())) {
    // Nothing to do.
  }
#endif
  return result;
}

static jint JNI_CreateJavaVM_inner(JavaVM **vm, void **penv, void *args) {
  HOTSPOT_JNI_CREATEJAVAVM_ENTRY((void **) vm, penv, args);

  jint result = JNI_ERR;
  DT_RETURN_MARK(CreateJavaVM, jint, (const jint&)result);

  // We're about to use Atomic::xchg for synchronization.  Some Zero
  // platforms use the GCC builtin __sync_lock_test_and_set for this,
  // but __sync_lock_test_and_set is not guaranteed to do what we want
  // on all architectures.  So we check it works before relying on it.
#if defined(ZERO) && defined(ASSERT)
  {
    jint a = 0xcafebabe;
    jint b = Atomic::xchg(&a, (jint) 0xdeadbeef);
    void *c = &a;
    void *d = Atomic::xchg(&c, &b);
    assert(a == (jint) 0xdeadbeef && b == (jint) 0xcafebabe, "Atomic::xchg() works");
    assert(c == &b && d == &a, "Atomic::xchg() works");
  }
#endif // ZERO && ASSERT

  // At the moment it's only possible to have one Java VM,
  // since some of the runtime state is in global variables.

  // We cannot use our mutex locks here, since they only work on
  // Threads. We do an atomic compare and exchange to ensure only
  // one thread can call this method at a time

  // We use Atomic::xchg rather than Atomic::add/dec since on some platforms
  // the add/dec implementations are dependent on whether we are running
  // on a multiprocessor Atomic::xchg does not have this problem.
  if (Atomic::xchg(&vm_created, IN_PROGRESS) != NOT_CREATED) {
    return JNI_EEXIST;   // already created, or create attempt in progress
  }

  // If a previous creation attempt failed but can be retried safely,
  // then safe_to_recreate_vm will have been reset to 1 after being
  // cleared here. If a previous creation attempt succeeded and we then
  // destroyed that VM, we will be prevented from trying to recreate
  // the VM in the same process, as the value will still be 0.
  if (Atomic::xchg(&safe_to_recreate_vm, 0) == 0) {
    return JNI_ERR;
  }

  /**
   * Certain errors during initialization are recoverable and do not
   * prevent this method from being called again at a later time
   * (perhaps with different arguments).  However, at a certain
   * point during initialization if an error occurs we cannot allow
   * this function to be called again (or it will crash).  In those
   * situations, the 'canTryAgain' flag is set to false, which atomically
   * sets safe_to_recreate_vm to 1, such that any new call to
   * JNI_CreateJavaVM will immediately fail using the above logic.
   */
  bool can_try_again = true;

  result = Threads::create_vm((JavaVMInitArgs*) args, &can_try_again);
  if (result == JNI_OK) {
    JavaThread *thread = JavaThread::current();
    assert(!thread->has_pending_exception(), "should have returned not OK");
    // thread is thread_in_vm here
    *vm = (JavaVM *)(&main_vm);
    *(JNIEnv**)penv = thread->jni_environment();
    // mark creation complete for other JNI ops
    Atomic::release_store(&vm_created, COMPLETE);

#if INCLUDE_JVMCI
    if (EnableJVMCI) {
      if (UseJVMCICompiler) {
        // JVMCI is initialized on a CompilerThread
        if (BootstrapJVMCI) {
          JavaThread* THREAD = thread; // For exception macros.
          JVMCICompiler* compiler = JVMCICompiler::instance(true, CATCH);
          compiler->bootstrap(THREAD);
          if (HAS_PENDING_EXCEPTION) {
            HandleMark hm(THREAD);
            vm_exit_during_initialization(Handle(THREAD, PENDING_EXCEPTION));
          }
        }
      }
    }
#endif

    // Notify JVMTI
    if (JvmtiExport::should_post_thread_life()) {
       JvmtiExport::post_thread_start(thread);
    }

    JFR_ONLY(Jfr::on_thread_start(thread);)

    if (ReplayCompiles) ciReplay::replay(thread);

#ifdef ASSERT
    // Some platforms (like Win*) need a wrapper around these test
    // functions in order to properly handle error conditions.
    if (ErrorHandlerTest != 0) {
      VMError::controlled_crash(ErrorHandlerTest);
    }
#endif

    // Since this is not a JVM_ENTRY we have to set the thread state manually before leaving.
    ThreadStateTransition::transition_from_vm(thread, _thread_in_native);
    MACOS_AARCH64_ONLY(thread->enable_wx(WXExec));
  } else {
    // If create_vm exits because of a pending exception, exit with that
    // exception.  In the future when we figure out how to reclaim memory,
    // we may be able to exit with JNI_ERR and allow the calling application
    // to continue.
    if (Universe::is_fully_initialized()) {
      // otherwise no pending exception possible - VM will already have aborted
      Thread* current = Thread::current_or_null();
      if (current != nullptr) {
        JavaThread* THREAD = JavaThread::cast(current); // For exception macros.
        assert(HAS_PENDING_EXCEPTION, "must be - else no current thread exists");
        HandleMark hm(THREAD);
        vm_exit_during_initialization(Handle(THREAD, PENDING_EXCEPTION));
      }
    }

    if (can_try_again) {
      // reset safe_to_recreate_vm to 1 so that retrial would be possible
      safe_to_recreate_vm = 1;
    }

    // Creation failed. We must reset vm_created
    *vm = 0;
    *(JNIEnv**)penv = 0;
    // reset vm_created last to avoid race condition. Use OrderAccess to
    // control both compiler and architectural-based reordering.
    assert(vm_created == IN_PROGRESS, "must be");
    Atomic::release_store(&vm_created, NOT_CREATED);
  }

  // Flush stdout and stderr before exit.
  fflush(stdout);
  fflush(stderr);

  return result;

}
```
