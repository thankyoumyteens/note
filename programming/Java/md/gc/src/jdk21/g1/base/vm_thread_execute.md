# VMThread::execute

execute 函数会把传入的 VM_Operation 放入 VM_Operation 队列。 JVM 使用两个指针 `_cur_vm_operation` 和 `_next_vm_operation` 维护 VM_Operation 队列, `_next_vm_operation` 指向下一个要执行的 VM_Operation。

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
  // 它会把t线程中的_skip_gcalot属性设置为true
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
  // _calling_thread = thread;
  op->set_calling_thread(t);
  // 等待VM_Operation执行结束
  wait_until_executed(op);
  // 一些清理工作
  op->doit_epilogue();
}

/**
 * 等待VM_Operation执行结束
 */
void VMThread::wait_until_executed(VM_Operation* op) {
  MonitorLocker ml(VMOperation_lock,
                   Thread::current()->is_Java_thread() ?
                     Mutex::_safepoint_check_flag :
                     Mutex::_no_safepoint_check_flag);
  {
    TraceTime timer("Installing VM operation", TRACETIME_LOG(Trace, vmthread));
    while (true) {
      // 将_next_vm_operation设置为当前VM_Operation
      // 如果_next_vm_operation不为null, 函数会返回false
      if (VMThread::vm_thread()->set_next_operation(op)) {
        ml.notify_all();
        break;
      }
      // 等待排在前面的VM_Operation执行完成
      log_trace(vmthread)("A VM operation already set, waiting");
      ml.wait();
    }
  }
  {
    // 等待VM_Operation被执行
    TraceTime timer("Waiting for VM operation to be completed", TRACETIME_LOG(Trace, vmthread));
    // VM_Operation在loop函数中执行完成后,
    // loop函数会把_next_vm_operation设为null
    while (_next_vm_operation == op) {
      ml.wait();
    }
  }
}

/**
 * 将_next_vm_operation设置为当前VM_Operation
 */
bool VMThread::set_next_operation(VM_Operation *op) {
  if (_next_vm_operation != nullptr) {
    return false;
  }
  log_debug(vmthread)("Adding VM operation: %s", op->name());

  _next_vm_operation = op;

  HOTSPOT_VMOPS_REQUEST(
                   (char *) op->name(), strlen(op->name()),
                   op->evaluate_at_safepoint() ? 0 : 1);
  return true;
}
```
