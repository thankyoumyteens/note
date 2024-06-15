# VM_HandshakeAllThreads

在执行握手时, HandshakeALotClosure 会包装成 VM_HandshakeAllThreads 执行。

```cpp
// --- src/hotspot/share/runtime/handshake.cpp --- //

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

## HandshakeALotClosure

```cpp
// --- src/hotspot/share/runtime/vmThread.cpp --- //

class HandshakeALotClosure : public HandshakeClosure {
 public:
  HandshakeALotClosure() : HandshakeClosure("HandshakeALot") {}
  void do_thread(Thread* thread) {
#ifdef ASSERT
    JavaThread::cast(thread)->verify_states_for_handshake();
#endif
  }
};
```

## VM_HandshakeAllThreads

```cpp
// --- src/hotspot/share/runtime/handshake.cpp --- //

class VM_HandshakeAllThreads: public VM_Operation {
  HandshakeOperation* const _op;
 public:
  VM_HandshakeAllThreads(HandshakeOperation* op) : _op(op) {}

  const char* cause() const { return _op->name(); }

  bool evaluate_at_safepoint() const { return false; }

  void doit() {
    jlong start_time_ns = os::javaTimeNanos();

    JavaThreadIteratorWithHandle jtiwh;
    int number_of_threads_issued = 0;
    for (JavaThread* thr = jtiwh.next(); thr != nullptr; thr = jtiwh.next()) {
      thr->handshake_state()->add_operation(_op);
      number_of_threads_issued++;
    }
    if (UseSystemMemoryBarrier) {
      SystemMemoryBarrier::emit();
    }

    if (number_of_threads_issued < 1) {
      log_handshake_info(start_time_ns, _op->name(), 0, 0, "no threads alive");
      return;
    }
    // _op was created with a count == 1 so don't double count.
    _op->add_target_count(number_of_threads_issued - 1);

    log_trace(handshake)("Threads signaled, begin processing blocked threads by VMThread");
    HandshakeSpinYield hsy(start_time_ns);
    // Keeps count on how many of own emitted handshakes
    // this thread execute.
    int emitted_handshakes_executed = 0;
    do {
      // Check if handshake operation has timed out
      check_handshake_timeout(start_time_ns, _op);

      // Have VM thread perform the handshake operation for blocked threads.
      // Observing a blocked state may of course be transient but the processing is guarded
      // by mutexes and we optimistically begin by working on the blocked threads
      jtiwh.rewind();
      for (JavaThread* thr = jtiwh.next(); thr != nullptr; thr = jtiwh.next()) {
        // A new thread on the ThreadsList will not have an operation,
        // hence it is skipped in handshake_try_process.
        HandshakeState::ProcessResult pr = thr->handshake_state()->try_process(_op);
        hsy.add_result(pr);
        if (pr == HandshakeState::_succeeded) {
          emitted_handshakes_executed++;
        }
      }
      hsy.process();
    } while (!_op->is_completed());

    // This pairs up with the release store in do_handshake(). It prevents future
    // loads from floating above the load of _pending_threads in is_completed()
    // and thus prevents reading stale data modified in the handshake closure
    // by the Handshakee.
    OrderAccess::acquire();

    log_handshake_info(start_time_ns, _op->name(), number_of_threads_issued, emitted_handshakes_executed);
  }

  VMOp_Type type() const { return VMOp_HandshakeAllThreads; }
};
```
