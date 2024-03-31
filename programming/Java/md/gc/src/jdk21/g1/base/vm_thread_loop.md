# VMThread::loop

VMThread 启动后, 会一直执行 VMThread::loop(), 等待处理 VM_Operation, loop()函数会不断读取 `_next_vm_operation` 进行执行。

```cpp
////////////////////////////////////////////
// src/hotspot/share/runtime/vmThread.cpp //
////////////////////////////////////////////

void VMThread::loop() {
  assert(_cur_vm_operation == nullptr, "no current one should be executing");

  SafepointSynchronize::init(_vm_thread);

  // Need to set a calling thread for ops not passed
  // via the normal way.
  cleanup_op.set_calling_thread(_vm_thread);
  safepointALot_op.set_calling_thread(_vm_thread);

  while (true) {
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
 * 等待execute函数设置VM_Operation
 */
void VMThread::wait_for_operation() {
  assert(Thread::current()->is_VM_thread(), "Must be the VM thread");
  MonitorLocker ml_op_lock(VMOperation_lock, Mutex::_no_safepoint_check_flag);

  // 清除之前的VM_Operation
  // 在最开始_next_vm_operation会指向VM_Cleanup对象
  _next_vm_operation = nullptr;
  // 唤醒等待的线程(execute函数), 
  // 让它们可以继续给_next_vm_operation设置VM_Operation
  ml_op_lock.notify_all();

  while (!should_terminate()) {
    self_destruct_if_needed();
    if (_next_vm_operation != nullptr) {
      return;
    }
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

    setup_periodic_safepoint_if_needed();
    if (_next_vm_operation != nullptr) {
      return;
    }

    // We didn't find anything to execute, notify any waiter so they can install an op.
    ml_op_lock.notify_all();
    ml_op_lock.wait(GuaranteedSafepointInterval);
  }
}

/**
 * 执行VM_Operation
 */
void VMThread::inner_execute(VM_Operation* op) {
  assert(Thread::current()->is_VM_thread(), "Must be the VM thread");

  VM_Operation* prev_vm_operation = nullptr;
  if (_cur_vm_operation != nullptr) {
    // Check that the VM operation allows nested VM operation.
    // This is normally not the case, e.g., the compiler
    // does not allow nested scavenges or compiles.
    if (!_cur_vm_operation->allow_nested_vm_operations()) {
      fatal("Unexpected nested VM operation %s requested by operation %s",
            op->name(), _cur_vm_operation->name());
    }
    op->set_calling_thread(_cur_vm_operation->calling_thread());
    prev_vm_operation = _cur_vm_operation;
  }

  _cur_vm_operation = op;

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
  if (_cur_vm_operation->evaluate_at_safepoint() &&
      !SafepointSynchronize::is_at_safepoint()) {
    SafepointSynchronize::begin();
    if (has_timeout_task) {
      _timeout_task->arm(_cur_vm_operation->name());
    }
    end_safepoint = true;
  }

  evaluate_operation(_cur_vm_operation);

  if (end_safepoint) {
    if (has_timeout_task) {
      _timeout_task->disarm();
    }
    SafepointSynchronize::end();
  }

  _cur_vm_operation = prev_vm_operation;
}
```
