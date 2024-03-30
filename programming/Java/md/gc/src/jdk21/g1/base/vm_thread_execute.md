# VMThread::execute

如果需要 GC 的话, G1 会创建一个 VM_G1CollectForAllocation 对象交给 VMThread 执行。 JVM 会将 VMThread 的 `_next_vm_operation` 属性设置为当前的 VM_G1CollectForAllocation 对象, 之后 JavaThread 会一直阻塞, 直到当前的 VM_G1CollectForAllocation 执行结束。

```cpp
////////////////////////////////////////////
// src/hotspot/share/runtime/vmThread.cpp //
////////////////////////////////////////////

void VMThread::execute(VM_Operation* op) {
  // 获取当前正在执行的线程
  Thread* t = Thread::current();
  // 如果当前线程是VMThread, 直接执行传入的VM_Operation
  if (t->is_VM_thread()) {
    op->set_calling_thread(t);
    ((VMThread*)t)->inner_execute(op);
    return;
  }

  // 防止在GC执行过程中重复执行GC
  SkipGCALot sgcalot(t);

  // 当前线程是JavaThread或者WatcherThread
  if (t->is_Java_thread()) {
    JavaThread::cast(t)->check_for_valid_safepoint_state();
  }

  // doit_prologue()默认返回true
  if (!op->doit_prologue()) {
    // GC在同一时间只需要执行一次,
    // 但可能会被多个Java线程加入队列
    // 当有多个GC需要同时执行时,
    // 其它的VM_Operation会返回false
    return;
  }

  op->set_calling_thread(t);

  wait_until_executed(op);

  op->doit_epilogue();
}
```
