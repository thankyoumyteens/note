# refill_waste_limit

默认值

```cpp
// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/threadLocalAllocBuffer.cpp

// refill_waste_limit的初始化
size_t ThreadLocalAllocBuffer::initial_refill_waste_limit()     { return desired_size() / TLABRefillWasteFraction; }


// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/threadLocalAllocBuffer.inline.hpp

// 增大
void ThreadLocalAllocBuffer::record_slow_allocation(size_t obj_size) {
  // Raise size required to bypass TLAB next time. Why? Else there's
  // a risk that a thread that repeatedly allocates objects of one
  // size will get stuck on this slow path.

  set_refill_waste_limit(refill_waste_limit() + refill_waste_limit_increment());

  _slow_allocations++;

  log_develop_trace(gc, tlab)("TLAB: %s thread: " PTR_FORMAT " [id: %2d]"
                              " obj: " SIZE_FORMAT
                              " free: " SIZE_FORMAT
                              " waste: " SIZE_FORMAT,
                              "slow", p2i(thread()), thread()->osthread()->thread_id(),
                              obj_size, free(), refill_waste_limit());
}
```
