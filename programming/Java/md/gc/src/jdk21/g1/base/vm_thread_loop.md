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
```

## 等待 VM_Operation

```cpp
////////////////////////////////////////////
// src/hotspot/share/runtime/vmThread.cpp //
////////////////////////////////////////////

/**
 * 等待VM_Operation
 */
void VMThread::wait_for_operation() {
  assert(Thread::current()->is_VM_thread(), "Must be the VM thread");
  MonitorLocker ml_op_lock(VMOperation_lock, Mutex::_no_safepoint_check_flag);

  // 清除之前的VM_Operation
  // 在最开始_next_vm_operation会指向VM_Cleanup对象
  // VM_Cleanup用于jvm定期执行的清理工作
  _next_vm_operation = nullptr;
  // 唤醒等待的线程(execute函数中调用ml.wait()函数进入等待),
  // 让它们可以继续尝试给_next_vm_operation设置VM_Operation
  ml_op_lock.notify_all();

  while (!should_terminate()) {
    self_destruct_if_needed();
    // 有新的VM_Operation
    // 返回, 交给inner_execute函数去执行
    if (_next_vm_operation != nullptr) {
      return;
    }

    // 判断是否需要执行所有线程的定期握手
    if (handshake_alot()) {
      {
        // 解锁
        MutexUnlocker mul(VMOperation_lock);
        HandshakeALotClosure hal_cl;
        // 执行握手
        Handshake::execute(&hal_cl);
      }
      // 在上面的解锁期间, Handshake::execute会设置
      // 执行握手的VM_Operation,
      // 或者可能会有其它线程抢先
      // 调用VMThread::execute设置新的VM_Operation
      // 所以这里需要再判断一下
      if (_next_vm_operation != nullptr) {
        return;
      }
    }
    assert(_next_vm_operation == nullptr, "Must be");
    assert(_cur_vm_operation  == nullptr, "Must be");

    // 队列中没有其它的VM_Operation要执行
    // 开始判断是否需要执行定期清理的VM_Operation
    // jvm会定期进入安全点(-XX:GuaranteedSafepointInterval, 默认1秒)
    // 执行清理(线程的缓存数据等)等操作
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
```

### 定期握手

```cpp
////////////////////////////////////////////
// src/hotspot/share/runtime/vmThread.cpp //
////////////////////////////////////////////

/**
 * 判断是否需要握手
 */
bool VMThread::handshake_alot() {
  assert(_cur_vm_operation == nullptr, "should not have an op yet");
  assert(_next_vm_operation == nullptr, "should not have an op yet");
  // HandshakeALot 默认为false
  if (!HandshakeALot) {
    return false;
  }
  static jlong last_halot_ms = 0;
  jlong now_ms = nanos_to_millis(os::javaTimeNanos());
  // 默认1秒握一次手
  jlong interval = GuaranteedSafepointInterval != 0 ? GuaranteedSafepointInterval : 1000;
  jlong deadline_ms = interval + last_halot_ms;
  // 距离上次握手是否超过1秒
  if (now_ms > deadline_ms) {
    last_halot_ms = now_ms;
    return true;
  }
  return false;
}

/////////////////////////////////////////////
// src/hotspot/share/runtime/handshake.cpp //
/////////////////////////////////////////////

/**
 * 执行握手
 */
void Handshake::execute(HandshakeClosure* hs_cl) {
  // 把HandshakeClosure包装成VM_Operation
  HandshakeOperation cto(hs_cl, nullptr, Thread::current());
  VM_HandshakeAllThreads handshake(&cto);
  // 加入VM_Operation队列
  VMThread::execute(&handshake);
}
```

### 定期进入安全点

```cpp
////////////////////////////////////////////
// src/hotspot/share/runtime/vmThread.cpp //
////////////////////////////////////////////

/**
 * 判断是否需要定期进入安全点
 */
void VMThread::setup_periodic_safepoint_if_needed() {
  assert(_cur_vm_operation  == nullptr, "Already have an op");
  assert(_next_vm_operation == nullptr, "Already have an op");
  // 距离上次进入安全点过了多久
  jlong interval_ms = SafepointTracing::time_since_last_safepoint_ms();
  // 是否需要进入安全点
  bool max_time_exceeded = GuaranteedSafepointInterval != 0 &&
                           (interval_ms >= GuaranteedSafepointInterval);
  if (!max_time_exceeded) {
    return;
  }
  // cleanup_op和safepointALot_op都需要进入安全点执行
  if (SafepointSynchronize::is_cleanup_needed()) {
    // VM_Cleanup
    _next_vm_operation = &cleanup_op;
  } else if (SafepointALot) {
    // VM_SafepointALot什么也不做, 只是为了让所有线程定期进入安全点
    _next_vm_operation = &safepointALot_op;
  }
}

bool SafepointSynchronize::is_cleanup_needed() {
  // Need a safepoint if some inline cache buffers is non-empty
  if (!InlineCacheBuffer::is_empty()) return true;
  if (StringTable::needs_rehashing()) return true;
  if (SymbolTable::needs_rehashing()) return true;
  return false;
}

////////////////////////////////////////////////
// src/hotspot/share/runtime/vmOperations.hpp //
////////////////////////////////////////////////

class VM_Cleanup: public VM_EmptyOperation {
 public:
  VMOp_Type type() const { return VMOp_Cleanup; }
};

class VM_SafepointALot: public VM_EmptyOperation {
 public:
  VMOp_Type type() const { return VMOp_SafepointALot; }
};

class VM_EmptyOperation : public VM_Operation {
public:
  virtual void doit() final {}
  virtual bool skip_thread_oop_barriers() const final {
    // doit函数和safepoint清理任务都不会在Java线程中读取oop
    return true;
  }
};
```

<!-- TODO VM_SafepointALot 功能待确认, VM_Cleanup 到底用在哪了 -->

## 执行 VM_Operation

```cpp
////////////////////////////////////////////
// src/hotspot/share/runtime/vmThread.cpp //
////////////////////////////////////////////

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
  // 用来自动释放线程执行时产生的对象句柄
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

    // 执行VM_Operation中的evaluate函数
    // 会调用doit函数
    // doit函数会由不同的VM_Operation各自重写
    op->evaluate();

    // VM_Operation执行完成, 是否要触发事件
    if (event.should_commit()) {
      post_vm_operation_event(&event, op);
    }

    HOTSPOT_VMOPS_END(
                     (char *) op->name(), strlen(op->name()),
                     op->evaluate_at_safepoint() ? 0 : 1);
  }
}
```

## doit 函数

VM_Operation 实际要执行的逻辑会写在 doit 函数中。

```cpp
///////////////////////////////////////////////
// src/hotspot/share/runtime/vmOperation.hpp //
///////////////////////////////////////////////

class VM_Operation : public StackObj {
 private:
  // 执行VM_Operation的线程
  Thread*         _calling_thread;
  // ...
 public:
  VM_Operation() : _calling_thread(nullptr) {}

  // 会被VMThread调用, 这个函数不能被重写
  void evaluate();

  // evaluate函数内部会调用doit函数
  // 如果调用VMThread::execute((VM_Operation*)函数的线程是JavaThread,
  // 那么JavaThread在把控制权交给VMThread之前会先调用doit_prologue函数,
  // 如果doit_prologue函数返回true, 那么这个VM_Operation就会继续执行,
  // 并且在VM_Operation执行完成后, JVM会通过JavaThread执行一次doit_epilogue函数
  // 如果doit_prologue函数返回false, 那么这个VM_Operation不会继续执行
  virtual void doit()                            = 0;
  virtual bool doit_prologue()                   { return true; };
  virtual void doit_epilogue()                   {};

  // 如果VM_Operation中不需要访问线程内部的栈帧的话,
  // 需要重写这个函数, 让它返回true
  virtual bool skip_thread_oop_barriers() const { return false; }

  // An operation can either be done inside a safepoint
  // or concurrently with Java threads running.
  virtual bool evaluate_at_safepoint() const { return true; }
  // ...
};
```
