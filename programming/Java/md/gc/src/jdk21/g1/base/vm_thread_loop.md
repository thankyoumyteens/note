# VMThread::loop

VMThread 启动后, 会一直执行 VMThread::loop(), 等待处理 VM_Operation, loop()函数会不断读取 `_next_vm_operation` 进行执行。

```cpp
////////////////////////////////////////////
// src/hotspot/share/runtime/vmThread.cpp //
////////////////////////////////////////////

void VMThread::loop() {
  assert(_cur_vm_operation == nullptr, "no current one should be executing");
  // 初始化jvm线程
  SafepointSynchronize::init(_vm_thread);

  // 为内置的VM_Operation设置执行线程
  cleanup_op.set_calling_thread(_vm_thread);
  safepointALot_op.set_calling_thread(_vm_thread);

  while (true) {
    // jvm准备退出时这个函数会返回ture
    if (should_terminate()) break;
    // 等待execute函数设置VM_Operation
    wait_for_operation();
    if (should_terminate()) break;
    assert(_next_vm_operation != nullptr, "Must have one");
    // 执行VM_Operation
    inner_execute(_next_vm_operation);
  }
}

/**
 * 等待VM_Operation
 */
void VMThread::wait_for_operation() {
  assert(Thread::current()->is_VM_thread(), "Must be the VM thread");
  MonitorLocker ml_op_lock(VMOperation_lock, Mutex::_no_safepoint_check_flag);

  // 清除之前的VM_Operation
  // 在最开始_next_vm_operation会指向VM_Cleanup对象
  _next_vm_operation = nullptr;
  // 唤醒等待的线程(execute函数中调用ml.wait()函数进入等待),
  // 让它们可以继续尝试给_next_vm_operation设置VM_Operation
  ml_op_lock.notify_all();

  while (!should_terminate()) {
    self_destruct_if_needed();
    // 有新的VM_Operation
    // 准备执行
    if (_next_vm_operation != nullptr) {
      return;
    }
    // TODO
    if (handshake_alot()) {
      {
        MutexUnlocker mul(VMOperation_lock);
        HandshakeALotClosure hal_cl;
        Handshake::execute(&hal_cl);
      }
      // When we unlocked above someone might have setup a new op.
      if (_next_vm_operation != nullptr) {
        return;
      }
    }
    assert(_next_vm_operation == nullptr, "Must be");
    assert(_cur_vm_operation  == nullptr, "Must be");
    // TODO
    setup_periodic_safepoint_if_needed();
    if (_next_vm_operation != nullptr) {
      return;
    }

    // 没找到需要执行的VM_Operation
    // 唤醒其它线程, 让它们设置VM_Operation
    ml_op_lock.notify_all();
    ml_op_lock.wait(GuaranteedSafepointInterval);
  }
}

/**
 * 执行VM_Operation
 * 传入的是_next_vm_operation
 */
void VMThread::inner_execute(VM_Operation* op) {
  assert(Thread::current()->is_VM_thread(), "Must be the VM thread");

  VM_Operation* prev_vm_operation = nullptr;
  if (_cur_vm_operation != nullptr) {
    // 检查传入的op是不是_cur_vm_operation的嵌套VM_Operation
    if (!_cur_vm_operation->allow_nested_vm_operations()) {
      fatal("Unexpected nested VM operation %s requested by operation %s",
            op->name(), _cur_vm_operation->name());
    }
    // 嵌套的VM_Operation和上级VM_Operation使用相同线程执行
    op->set_calling_thread(_cur_vm_operation->calling_thread());
    prev_vm_operation = _cur_vm_operation;
  }

  _cur_vm_operation = op;
  // TODO
  HandleMark hm(VMThread::vm_thread());

  const char* const cause = op->cause();
  EventMarkVMOperation em("Executing %sVM operation: %s%s%s%s",
      prev_vm_operation != nullptr ? "nested " : "",
      op->name(),
      cause != nullptr ? " (" : "",
      cause != nullptr ? cause : "",
      cause != nullptr ? ")" : "");

  log_debug(vmthread)("Evaluating %s %s VM operation: %s",
                       prev_vm_operation != nullptr ? "nested" : "",
                      _cur_vm_operation->evaluate_at_safepoint() ? "safepoint" : "non-safepoint",
                      _cur_vm_operation->name());

  bool end_safepoint = false;
  bool has_timeout_task = (_timeout_task != nullptr);
  // evaluate_at_safepoint(): 这个VM_Operation是否需要在安全点执行
  // is_at_safepoint(): 所有java线程是否都进入了安全点
  if (_cur_vm_operation->evaluate_at_safepoint() &&
      !SafepointSynchronize::is_at_safepoint()) {
    // 将所有线程执行到安全点并暂停它们
    SafepointSynchronize::begin();
    if (has_timeout_task) {
      // _timeout_task用来发出警告或终止执行时间太长的VM_Operation
      _timeout_task->arm(_cur_vm_operation->name());
    }
    end_safepoint = true;
  }
  // 执行VM_Operation
  evaluate_operation(_cur_vm_operation);

  if (end_safepoint) {
    if (has_timeout_task) {
      _timeout_task->disarm();
    }
    // 唤醒所有线程, 通知它们安全点中的操作已经执行完成
    SafepointSynchronize::end();
  }

  _cur_vm_operation = prev_vm_operation;
}

/**
 * 执行VM_Operation
 */
void VMThread::evaluate_operation(VM_Operation* op) {
  ResourceMark rm;

  {
    PerfTraceTime vm_op_timer(perf_accumulated_vm_operation_time());
    HOTSPOT_VMOPS_BEGIN(
                     (char *) op->name(), strlen(op->name()),
                     op->evaluate_at_safepoint() ? 0 : 1);

    EventExecuteVMOperation event;

    // 执行VM_Operation中的evaluate方法
    // 这个方法会由不同的VM_Operation各自重写
    op->evaluate();

    if (event.should_commit()) {
      post_vm_operation_event(&event, op);
    }

    HOTSPOT_VMOPS_END(
                     (char *) op->name(), strlen(op->name()),
                     op->evaluate_at_safepoint() ? 0 : 1);
  }
}
```
