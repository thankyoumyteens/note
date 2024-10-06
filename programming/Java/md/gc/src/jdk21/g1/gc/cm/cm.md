# 并发标记

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

void G1CollectedHeap::start_concurrent_cycle(bool concurrent_operation_is_full_mark) {
  assert(!_cm_thread->in_progress(), "Can not start concurrent operation while in progress");

  MutexLocker x(CGC_lock, Mutex::_no_safepoint_check_flag);
  if (concurrent_operation_is_full_mark) {
    _cm->post_concurrent_mark_start();
    _cm_thread->start_full_mark();
  } else {
    _cm->post_concurrent_undo_start();
    _cm_thread->start_undo_mark();
  }
  CGC_lock->notify();
}
```
