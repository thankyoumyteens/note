# vm_exit

```cpp
// --- src/hotspot/share/runtime/java.cpp --- //

void vm_exit(int code) {
  Thread* thread =
      ThreadLocalStorage::is_initialized() ? Thread::current_or_null() : nullptr;
  if (thread == nullptr) {
    // very early initialization failure -- just exit
    vm_direct_exit(code);
  }

  // We'd like to add an entry to the XML log to show that the VM is
  // terminating, but we can't safely do that here. The logic to make
  // XML termination logging safe is tied to the termination of the
  // VMThread, and it doesn't terminate on this exit path. See 8222534.

  if (VMThread::vm_thread() != nullptr) {
    if (thread->is_Java_thread()) {
      // We must be "in_vm" for the code below to work correctly.
      // Historically there must have been some exit path for which
      // that was not the case and so we set it explicitly - even
      // though we no longer know what that path may be.
      JavaThread::cast(thread)->set_thread_state(_thread_in_vm);
    }

    // Fire off a VM_Exit operation to bring VM to a safepoint and exit
    VM_Exit op(code);

    // 4945125 The vm thread comes to a safepoint during exit.
    // GC vm_operations can get caught at the safepoint, and the
    // heap is unparseable if they are caught. Grab the Heap_lock
    // to prevent this. The GC vm_operations will not be able to
    // queue until after we release it, but we never do that as we
    // are terminating the VM process.
    MutexLocker ml(Heap_lock);

    VMThread::execute(&op);
    // should never reach here; but in case something wrong with VM Thread.
    vm_direct_exit(code);
  } else {
    // VM thread is gone, just exit
    vm_direct_exit(code);
  }
  ShouldNotReachHere();
}
```
