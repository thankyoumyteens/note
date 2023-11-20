# GC_locker

GC_locker 是 JNI 线程访问临界区时的加锁机制。临界区（Critical Section）是指在多线程环境下，一段需要确保同一时刻只有一个线程能够访问的代码区域。

比如，当使用本地方法 JNI 函数访问 JVM 中的字符串或数组数据时，需要用到 jni_GetStringCritical 和 jni_ReleaseStringCritical 两个函数。

> jdk8u60-master\jdk\src\share\native\common\jni_util.c

```cpp
static const char* getString8859_1Chars(JNIEnv *env, jstring jstr) {
    // 从JVM返回字符串指针
    int i;
    char *result;
    jint len = (*env)->GetStringLength(env, jstr);
    const jchar *str = (*env)->GetStringCritical(env, jstr, 0);
    if (str == 0) {
        return 0;
    }
    // 分配内存
    result = MALLOC_MIN4(len);
    if (result == 0) {
        // 内存不足，抛出OOM异常
        (*env)->ReleaseStringCritical(env, jstr, str);
        JNU_ThrowOutOfMemoryError(env, 0);
        return 0;
    }
    // 拷贝字符串的值
    for (i=0; i<len; i++) {
        jchar unicode = str[i];
        if (unicode <= 0x00ff)
            result[i] = (char)unicode;
        else
            result[i] = '?';
    }

    result[len] = 0;
    (*env)->ReleaseStringCritical(env, jstr, str);
    return result;
}
```

> jdk8u60-master\hotspot\src\share\vm\prims\jni.cpp

```cpp
/**
 * jni_GetStringCritical
 */
JNI_ENTRY(const jchar*, jni_GetStringCritical(JNIEnv *env, jstring string, jboolean *isCopy))
  JNIWrapper("GetStringCritical");
#ifndef USDT2
  DTRACE_PROBE3(hotspot_jni, GetStringCritical__entry, env, string, isCopy);
#else
  HOTSPOT_JNI_GETSTRINGCRITICAL_ENTRY(
                                      env, string, (uintptr_t *) isCopy);
#endif
  // 进入临界区，使用GC_locker对临界区加锁
  GC_locker::lock_critical(thread);
  if (isCopy != NULL) {
    *isCopy = JNI_FALSE;
  }
  // 读取JVM中的字符串
  oop s = JNIHandles::resolve_non_null(string);
  int s_len = java_lang_String::length(s);
  typeArrayOop s_value = java_lang_String::value(s);
  int s_offset = java_lang_String::offset(s);
  const jchar* ret;
  if (s_len > 0) {
    ret = s_value->char_at_addr(s_offset);
  } else {
    ret = (jchar*) s_value->base(T_CHAR);
  }
#ifndef USDT2
  DTRACE_PROBE1(hotspot_jni, GetStringCritical__return, ret);
#else
 HOTSPOT_JNI_GETSTRINGCRITICAL_RETURN(
                                      (uint16_t *) ret);
#endif
  return ret;
JNI_END

/**
 * jni_ReleaseStringCritical
 */
JNI_ENTRY(void, jni_ReleaseStringCritical(JNIEnv *env, jstring str, const jchar *chars))
  JNIWrapper("ReleaseStringCritical");
#ifndef USDT2
  DTRACE_PROBE3(hotspot_jni, ReleaseStringCritical__entry, env, str, chars);
#else
  HOTSPOT_JNI_RELEASESTRINGCRITICAL_ENTRY(
                                          env, str, (uint16_t *) chars);
#endif
  // 离开临界区，使用GC_locker对临界区解锁
  GC_locker::unlock_critical(thread);
#ifndef USDT2
  DTRACE_PROBE(hotspot_jni, ReleaseStringCritical__return);
#else
HOTSPOT_JNI_RELEASESTRINGCRITICAL_RETURN(
);
#endif
JNI_END
```

## 进入临界区

每个线程都有一个参数\_jni_active_critical，用来记录当前进入的临界区个数，如果\_jni_active_critical > 0，说明该线程已经在临界区。

如果该线程还没进入临界区，且\_needs_gc 标识为 true，则执行 jni_lock 方法。\_needs_gc 默认为 false，只有在特殊情况下才会被设置为 true。\_jni_lock_count 记录正在临界区内的线程个数。

> jdk8u60-master\hotspot\src\share\vm\memory\gcLocker.inline.hpp

```cpp
inline void GC_locker::lock_critical(JavaThread* thread) {
  // 当_jni_active_critical大于0时，in_critical()返回true
  if (!thread->in_critical()) {
    if (needs_gc()) {
      // 如果该线程还没进入临界区，且_needs_gc为true
      jni_lock(thread);
      return;
    }
    increment_debug_jni_lock_count();
  }
  // 进入临界区
  thread->enter_critical();
}
```

> jdk8u60-master\hotspot\src\share\vm\memory\gcLocker.cpp

```cpp
void GC_locker::jni_lock(JavaThread* thread) {
  assert(!thread->in_critical(), "shouldn't currently be in a critical region");
  MutexLocker mu(JNICritical_lock);
  // 当_needs_gc为true，且_jni_lock_count大于0时，
  // is_active_and_needs_gc()返回true
  // _doing_gc表示enter_critical()方法中正在进行GC
  while (is_active_and_needs_gc() || _doing_gc) {
    // 阻塞线程
    JNICritical_lock->wait();
  }
  // 进入临界区
  thread->enter_critical();
  // 更新正在临界区内的线程个数
  _jni_lock_count++;
  increment_debug_jni_lock_count();
}
```

## 发生 Young GC

如果有线程已经进入了临界区，此时发生了 Young GC：

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
/**
 * Young GC入口
 */
bool G1CollectedHeap::do_collection_pause_at_safepoint(double target_pause_time_ms) {
  assert_at_safepoint(true);
  guarantee(!is_gc_active(), "collection is not reentrant");
  // 判断是否有线程在临界区，如果有则舍弃本次gc，并把_needs_gc参数设置为true
  if (GC_locker::check_active_before_gc()) {
    return false;
  }
  // ...
}
```

在开始 Young GC 之前，会判断是否有线程在临界区，如果有线程已经进入了临界区，则舍弃本次 gc，并把\_needs_gc 参数设置为 true：

> jdk8u60-master\hotspot\src\share\vm\memory\gcLocker.cpp

```cpp
bool GC_locker::check_active_before_gc() {
  assert(SafepointSynchronize::is_at_safepoint(), "only read at safepoint");
  // _jni_lock_count大于0时，is_active()返回true
  if (is_active() && !_needs_gc) {
    verify_critical_count();
    // _needs_gc设为true
    _needs_gc = true;
  }
  return is_active();
}
```

因为有线程进入了临界区，导致本次触发的 Young GC 被丢弃了，但是内存分配时空间不足的问题还需要解决，所以在离开临界区时，如果发现有 GC 被舍弃了，JVM 会重新执行一次这个 GC。

## 离开临界区

如果该线程已经在临界区中，且\_needs_gc 标识为 true，则执行 jni_unlock 方法。

> jdk8u60-master\hotspot\src\share\vm\memory\gcLocker.inline.hpp

```cpp
inline void GC_locker::unlock_critical(JavaThread* thread) {
  if (thread->in_last_critical()) {
    if (needs_gc()) {
      // 如果该线程已经在临界区中，且_needs_gc为true，
      // 表示有GC被舍弃了，需要补回来
      jni_unlock(thread);
      return;
    }
    decrement_debug_jni_lock_count();
  }
  // 离开临界区
  thread->exit_critical();
}
```

> jdk8u60-master\hotspot\src\share\vm\memory\gcLocker.cpp

```cpp
void GC_locker::jni_unlock(JavaThread* thread) {
  assert(thread->in_last_critical(), "should be exiting critical region");
  MutexLocker mu(JNICritical_lock);
  // 更新正在临界区内的线程个数
  _jni_lock_count--;
  decrement_debug_jni_lock_count();
  // 离开临界区
  thread->exit_critical();
  // _needs_gc为true，且_jni_lock_count小于等于0，即临界区中最后一个线程也离开了
  if (needs_gc() && !is_active_internal()) {
    // 标记正在进行GC
    _doing_gc = true;
    {
      MutexUnlocker munlock(JNICritical_lock);
      // GC
      // Universe::heap ()方法返回的是当前JVM使用的堆类，
      // 因为使用的是G1垃圾回收器，所以返回的是G1CollectedHeap
      Universe::heap()->collect(GCCause::_gc_locker);
    }
    // GC结束
    _doing_gc = false;
    _needs_gc = false;
    // 唤醒其它要进入临界区的线程
    JNICritical_lock->notify_all();
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
/**
 * GC
 */
void G1CollectedHeap::collect(GCCause::Cause cause) {
  assert_heap_not_locked();

  uint gc_count_before;
  uint old_marking_count_before;
  uint full_gc_count_before;
  bool retry_gc;

  do {
    retry_gc = false;

    {
      MutexLocker ml(Heap_lock);

      gc_count_before = total_collections();
      full_gc_count_before = total_full_collections();
      old_marking_count_before = _old_marking_cycles_started;
    }
    // 根据GC原因判断要做哪种GC
    if (should_do_concurrent_full_gc(cause)) {
      // Mixed GC
      VM_G1IncCollectionPause op(gc_count_before,
                                 0,     /* word_size */
                                 true,  /* should_initiate_conc_mark */
                                 g1_policy()->max_pause_time_ms(),
                                 cause);
      op.set_allocation_context(AllocationContext::current());
      // 执行GC
      VMThread::execute(&op);
      if (!op.pause_succeeded()) {
        if (old_marking_count_before == _old_marking_cycles_started) {
          retry_gc = op.should_retry_gc();
        }

        if (retry_gc) {
          if (GC_locker::is_active_and_needs_gc()) {
            GC_locker::stall_until_clear();
          }
        }
      }
    } else {
      // 从GC_locker传入的GC原因是GCCause::_gc_locker，
      // 所以会进行Young GC
      if (cause == GCCause::_gc_locker || cause == GCCause::_wb_young_gc
          DEBUG_ONLY(|| cause == GCCause::_scavenge_alot)) {

        // Young GC
        VM_G1IncCollectionPause op(gc_count_before,
                                   0,     /* word_size */
                                   false, /* should_initiate_conc_mark */
                                   g1_policy()->max_pause_time_ms(),
                                   cause);
        // 执行GC
        VMThread::execute(&op);
      } else {
        // Full GC.
        VM_G1CollectFull op(gc_count_before, full_gc_count_before, cause);
        // 执行GC
        VMThread::execute(&op);
      }
    }
  } while (retry_gc);
}
```
