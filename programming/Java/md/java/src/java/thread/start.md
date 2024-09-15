# start 方法

只有调用 start 方法后, 才会真正的创建线程并执行。

```java
// --- JDK 21 --- //

public void start() {
    synchronized (this) {
        // zero status corresponds to state "NEW".
        if (holder.threadStatus != 0)
            throw new IllegalThreadStateException();
        start0();
    }
}

private native void start0();
```

start0 是 native 方法, JVM 通过 JNI 调用

```cpp
// --- src/java.base/share/native/libjava/Thread.c --- //

static JNINativeMethod methods[] = {
    {"start0",           "()V",        (void *)&JVM_StartThread},
    // ...
};

// --- src/hotspot/share/prims/jvm.cpp --- //

JVM_ENTRY(void, JVM_StartThread(JNIEnv* env, jobject jthread))
    // ...
    JavaThread *native_thread = nullptr;
    // ...
    native_thread = new JavaThread(&thread_entry, sz);
    // ...
    Thread::start(native_thread);
JVM_END

// --- src/hotspot/share/runtime/javaThread.cpp --- //
JavaThread::JavaThread(ThreadFunction entry_point, size_t stack_sz) : JavaThread() {
  // ...
  os::create_thread(this, thr_type, stack_sz);
}

// --- src/hotspot/os/linux/os_linux.cpp --- //

bool os::create_thread(Thread* thread, ThreadType thr_type,
                       size_t req_stack_size) {
    // ...
    ret = pthread_create(&tid, &attr, (void* (*)(void*)) thread_native_entry, thread);
    // ...
}
```

pthread_create 是 linux 系统的 api, 用于创建线程。

thread_native_entry 是函数指针, 它会调用 java 的 Thread 类中的 run 方法:

```cpp
// --- src/hotspot/os/linux/os_linux.cpp --- //

static void *thread_native_entry(Thread *thread) {
    // ...
    thread->call_run();
    // ...
}
```

所以 Java 的每一个线程都对应操作系统中的一个线程。
