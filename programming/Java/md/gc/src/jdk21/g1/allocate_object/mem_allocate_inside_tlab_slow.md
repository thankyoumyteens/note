# 在新的 TLAB 中分配

```cpp
//////////////////////////////////////////////////
// src/hotspot/share/gc/shared/memAllocator.cpp //
//////////////////////////////////////////////////

/**
 * 申请一个新的TLAB, 并在新的TLAB中分配对象内存
 */
HeapWord* MemAllocator::mem_allocate_inside_tlab_slow(Allocation& allocation) const {
  HeapWord* mem = nullptr;
  ThreadLocalAllocBuffer& tlab = _thread->tlab();

  if (JvmtiExport::should_post_sampled_object_alloc()) {
    tlab.set_back_allocation_end();
    mem = tlab.allocate(_word_size);

    // We set back the allocation sample point to try to allocate this, reset it
    // when done.
    allocation._tlab_end_reset_for_sample = true;

    if (mem != nullptr) {
      return mem;
    }
  }

  // TLAB剩余的空间大于可以浪费掉的最大空间
  // 每个TLAB都会维护一个refill_waste_limit,
  // 用于判断当前TLAB不够分配时, 是否需要申请新的TLAB,
  // 假设要分配的对象a的大小为10k, refill_waste_limit是5k:
  // 1. 如果当前TLAB剩余3k, 那么这个TLAB就会被舍弃,
  //    JVM会创建一个新的TLAB来为对象a分配空间
  // 2. 如果当前TLAB剩余6k, 那么这个TLAB就会被保留,
  //    等待分配其它较小的对象, JVM会直接在堆中为对象a分配空间
  if (tlab.free() > tlab.refill_waste_limit()) {
    // 保留这个TLAB
    // 增大refill_waste_limit,
    // 避免频繁在堆中直接分配对象
    tlab.record_slow_allocation(_word_size);
    // 返回null,
    // 以调用mem_allocate_outside_tlab()
    // 直接在region中分配这个对象
    return nullptr;
  }

  // 创建一个新的TLAB来为对象分配空间

  // 为了避免内存碎片, 新的TLAB会比之前分配的更小
  size_t new_tlab_size = tlab.compute_size(_word_size);
  // 把当前TLAB中剩余的空间填充为dummy对象
  tlab.retire_before_allocation();
  // Eden空间不足, 新的TLAB创建失败
  if (new_tlab_size == 0) {
    return nullptr;
  }

  // 计算新的TLAB所需的最小空间
  size_t min_tlab_size = ThreadLocalAllocBuffer::compute_min_size(_word_size);
  // 创建新的TLAB, new_tlab_size不能小于min_tlab_size, 否则创建失败
  // 由于是新的TLAB, 对象从头开始分配,
  // 所以mem既是TLAB的开始地址, 又是待分配的对象的开始地址
  mem = Universe::heap()->allocate_new_tlab(min_tlab_size, new_tlab_size, &allocation._allocated_tlab_size);
  // 新的TLAB创建失败
  if (mem == nullptr) {
    assert(allocation._allocated_tlab_size == 0,
           "Allocation failed, but actual size was updated. min: " SIZE_FORMAT
           ", desired: " SIZE_FORMAT ", actual: " SIZE_FORMAT,
           min_tlab_size, new_tlab_size, allocation._allocated_tlab_size);
    return nullptr;
  }
  assert(allocation._allocated_tlab_size != 0, "Allocation succeeded but actual size not updated. mem at: "
         PTR_FORMAT " min: " SIZE_FORMAT ", desired: " SIZE_FORMAT,
         p2i(mem), min_tlab_size, new_tlab_size);
  // 格式化新的TLAB空间
  if (ZeroTLAB) {
    // 把整个TLAB内存空间初始化为0
    Copy::zero_to_words(mem, allocation._allocated_tlab_size);
  } else {
#ifdef ASSERT
    // Skip mangling the space corresponding to the object header to
    // ensure that the returned space is not considered parsable by
    // any concurrent GC thread.
    // 跳过对象头
    size_t hdr_size = oopDesc::header_size();
    // 填充: 0xBAADBABE
    Copy::fill_to_words(mem + hdr_size, allocation._allocated_tlab_size - hdr_size, badHeapWordVal);
#endif // ASSERT
  }
  // 初始化TLAB的相关字段
  tlab.fill(mem, mem + _word_size, allocation._allocated_tlab_size);
  // 返回对象的开始地址
  return mem;
}

////////////////////////////////////////////////////////////
// src/hotspot/share/gc/shared/threadLocalAllocBuffer.cpp //
////////////////////////////////////////////////////////////

void ThreadLocalAllocBuffer::fill(HeapWord* start,
                                  HeapWord* top,
                                  size_t    new_size) {
  _number_of_refills++;
  _allocated_size += new_size;
  print_stats("fill");
  assert(top <= start + new_size - alignment_reserve(), "size too small");
  // 初始化TLAB
  initialize(start, top, start + new_size - alignment_reserve());

  // 为新的TLAB初始化refill_waste_limit值
  set_refill_waste_limit(initial_refill_waste_limit());
}
```
