# 慢速分配对象

如果从 TLAB 中分配内存空间失败, 就会开始慢速分配。

```cpp
// jdk21-jdk-21-ga/src/hotspot/share/interpreter/interpreterRuntime.cpp
JRT_ENTRY(void, InterpreterRuntime::_new(JavaThread* current, ConstantPool* pool, int index))
  // 从常量池中取出klass对象
  Klass* k = pool->klass_at(index, CHECK);
  InstanceKlass* klass = InstanceKlass::cast(k);

  // 校验Klass是不是抽象类, 接口或者java.lang.Class, 如果是则抛出异常
  klass->check_valid_for_instantiation(true, CHECK);

  // 确保类已经初始化
  klass->initialize(CHECK);

  // 给对象分配内存空间
  oop obj = klass->allocate_instance(CHECK);
  // 将结果放到当前线程的_vm_result字段中,
  // 用来传递给解释器
  current->set_vm_result(obj);
JRT_END

// jdk21-jdk-21-ga/src/hotspot/share/oops/instanceKlass.cpp
void InstanceKlass::check_valid_for_instantiation(bool throwError, TRAPS) {
  // 确保klass不是抽象类或接口
  if (is_interface() || is_abstract()) {
    ResourceMark rm(THREAD);
    THROW_MSG(throwError ? vmSymbols::java_lang_InstantiationError()
              : vmSymbols::java_lang_InstantiationException(), external_name());
  }
  // 确保klass不是java.lang.Class
  if (this == vmClasses::Class_klass()) {
    ResourceMark rm(THREAD);
    THROW_MSG(throwError ? vmSymbols::java_lang_IllegalAccessError()
              : vmSymbols::java_lang_IllegalAccessException(), external_name());
  }
}

instanceOop InstanceKlass::allocate_instance(TRAPS) {
  // 这个类如果有一个非空的finalize()方法,
  // 则has_finalizer_flag为true
  bool has_finalizer_flag = has_finalizer();
  // 获取这个类要创建的对象的大小
  size_t size = size_helper();

  instanceOop i;
  // 给对象分配内存空间
  i = (instanceOop)Universe::heap()->obj_allocate(this, size, CHECK_NULL);
  // 判断是否要注册finalizer
  if (has_finalizer_flag && !RegisterFinalizersAtInit) {
    i = register_finalizer(i, CHECK_NULL);
  }
  return i;
}

// jdk21-jdk-21-ga/src/hotspot/share/memory/universe.hpp
static CollectedHeap* heap() {
  // 返回当前使用的垃圾回收器管理的堆,
  // 使用G1返回的是G1CollectedHeap
  return _collectedHeap;
}

// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/collectedHeap.inline.hpp
inline oop CollectedHeap::obj_allocate(Klass* klass, size_t size, TRAPS) {
  ObjAllocator allocator(klass, size, THREAD);
  // 给对象分配内存空间
  return allocator.allocate();
}

// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/memAllocator.cpp
oop MemAllocator::allocate() const {
  oop obj = nullptr;
  {
    Allocation allocation(*this, &obj);
    // 给对象分配内存空间
    HeapWord* mem = mem_allocate(allocation);
    if (mem != nullptr) {
      // 对象分配内存成功,
      // 初始化对象
      obj = initialize(mem);
    } else {
      // 对象分配内存失败,
      // 重置obj指针
      obj = nullptr;
    }
  }
  return obj;
}

// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/memAllocator.cpp
HeapWord* MemAllocator::mem_allocate(Allocation& allocation) const {
  if (UseTLAB) {
    // 尝试从TLAB中分配内存
    HeapWord* mem = mem_allocate_inside_tlab_fast();
    if (mem != nullptr) {
      return mem;
    }
  }
  // 在TLAB中分配失败, 开始慢速分配
  return mem_allocate_slow(allocation);
}

HeapWord* MemAllocator::mem_allocate_inside_tlab_fast() const {
  // ThreadLocalAllocBuffer& tlab() {
  //   return _tlab;
  // }
  // 尝试从TLAB中分配内存
  return _thread->tlab().allocate(_word_size);
}

HeapWord* MemAllocator::mem_allocate_slow(Allocation& allocation) const {
  // Allocation of an oop can always invoke a safepoint.
  debug_only(JavaThread::cast(_thread)->check_for_valid_safepoint_state());

  if (UseTLAB) {
    // Try refilling the TLAB and allocating the object in it.
    HeapWord* mem = mem_allocate_inside_tlab_slow(allocation);
    if (mem != nullptr) {
      return mem;
    }
  }

  return mem_allocate_outside_tlab(allocation);
}

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

  // Retain tlab and allocate object in shared space if
  // the amount free in the tlab is too large to discard.
  if (tlab.free() > tlab.refill_waste_limit()) {
    tlab.record_slow_allocation(_word_size);
    return nullptr;
  }

  // Discard tlab and allocate a new one.
  // To minimize fragmentation, the last TLAB may be smaller than the rest.
  size_t new_tlab_size = tlab.compute_size(_word_size);

  tlab.retire_before_allocation();

  if (new_tlab_size == 0) {
    return nullptr;
  }

  // Allocate a new TLAB requesting new_tlab_size. Any size
  // between minimal and new_tlab_size is accepted.
  size_t min_tlab_size = ThreadLocalAllocBuffer::compute_min_size(_word_size);
  mem = Universe::heap()->allocate_new_tlab(min_tlab_size, new_tlab_size, &allocation._allocated_tlab_size);
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

  if (ZeroTLAB) {
    // ..and clear it.
    Copy::zero_to_words(mem, allocation._allocated_tlab_size);
  } else {
    // ...and zap just allocated object.
#ifdef ASSERT
    // Skip mangling the space corresponding to the object header to
    // ensure that the returned space is not considered parsable by
    // any concurrent GC thread.
    size_t hdr_size = oopDesc::header_size();
    Copy::fill_to_words(mem + hdr_size, allocation._allocated_tlab_size - hdr_size, badHeapWordVal);
#endif // ASSERT
  }

  tlab.fill(mem, mem + _word_size, allocation._allocated_tlab_size);
  return mem;
}

HeapWord* MemAllocator::mem_allocate_outside_tlab(Allocation& allocation) const {
  allocation._allocated_outside_tlab = true;
  HeapWord* mem = Universe::heap()->mem_allocate(_word_size, &allocation._overhead_limit_exceeded);
  if (mem == nullptr) {
    return mem;
  }

  size_t size_in_bytes = _word_size * HeapWordSize;
  _thread->incr_allocated_bytes(size_in_bytes);

  return mem;
}
```
