# 初始化 TLAB

```cpp
////////////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/threadLocalAllocBuffer.cpp //
////////////////////////////////////////////////////////////////////////////

void ThreadLocalAllocBuffer::initialize() {
  initialize(nullptr,                    // start
             nullptr,                    // top
             nullptr);                   // end

  set_desired_size(initial_desired_size());

  size_t capacity = Universe::heap()->tlab_capacity(thread()) / HeapWordSize;
  if (capacity > 0) {
    // Keep alloc_frac as float and not double to avoid the double to float conversion
    float alloc_frac = desired_size() * target_refills() / (float)capacity;
    _allocation_fraction.sample(alloc_frac);
  }

  set_refill_waste_limit(initial_refill_waste_limit());

  reset_statistics();
}
```

