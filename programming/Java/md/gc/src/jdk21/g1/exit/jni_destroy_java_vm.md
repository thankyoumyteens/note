# jni_DestroyJavaVM

```cpp
// --- src/hotspot/share/prims/jni.cpp --- //

jint JNICALL jni_DestroyJavaVM(JavaVM *vm) {
  jint result = JNI_ERR;
  // On Windows, we need SEH protection
#if defined(_WIN32) && !defined(USE_VECTORED_EXCEPTION_HANDLING)
  __try {
#endif
    result = jni_DestroyJavaVM_inner(vm);
#if defined(_WIN32) && !defined(USE_VECTORED_EXCEPTION_HANDLING)
  } __except(topLevelExceptionFilter((_EXCEPTION_POINTERS*)_exception_info())) {
    // Nothing to do.
  }
#endif
  return result;
}

static jint JNICALL jni_DestroyJavaVM_inner(JavaVM *vm) {
  HOTSPOT_JNI_DESTROYJAVAVM_ENTRY(vm);
  jint res = JNI_ERR;
  DT_RETURN_MARK(DestroyJavaVM, jint, (const jint&)res);

  if (vm_created == NOT_CREATED) {
    res = JNI_ERR;
    return res;
  }

  JNIEnv *env;
  JavaVMAttachArgs destroyargs;
  destroyargs.version = CurrentVersion;
  destroyargs.name = (char *)"DestroyJavaVM";
  destroyargs.group = nullptr;
  res = vm->AttachCurrentThread((void **)&env, (void *)&destroyargs);
  if (res != JNI_OK) {
    return res;
  }

  JavaThread* thread = JavaThread::current();

  // Make sure we are actually in a newly attached thread, with no
  // existing Java frame.
  if (thread->has_last_Java_frame()) {
    return JNI_ERR;
  }

  // Since this is not a JVM_ENTRY we have to set the thread state manually before entering.

  // We are going to VM, change W^X state to the expected one.
  MACOS_AARCH64_ONLY(WXMode oldmode = thread->enable_wx(WXWrite));

  ThreadStateTransition::transition_from_native(thread, _thread_in_vm);
  Threads::destroy_vm();
  // Don't bother restoring thread state, VM is gone.
  vm_created = NOT_CREATED;
  return JNI_OK;
}
```
