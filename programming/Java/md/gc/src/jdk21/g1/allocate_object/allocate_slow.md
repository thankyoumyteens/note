# 慢速分配对象

如果从 TLAB 中分配内存空间失败, 就会开始慢速分配。

```cpp
//////////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/interpreter/interpreterRuntime.cpp //
//////////////////////////////////////////////////////////////////////////

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

//////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/oops/instanceKlass.cpp //
//////////////////////////////////////////////////////////////

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

///////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/memory/universe.hpp //
///////////////////////////////////////////////////////////

static CollectedHeap* heap() {
  // 返回当前使用的垃圾回收器管理的堆,
  // 使用G1返回的是G1CollectedHeap
  return _collectedHeap;
}

//////////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/collectedHeap.inline.hpp //
//////////////////////////////////////////////////////////////////////////

inline oop CollectedHeap::obj_allocate(Klass* klass, size_t size, TRAPS) {
  ObjAllocator allocator(klass, size, THREAD);
  // 给对象分配内存空间
  return allocator.allocate();
}

//////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/memAllocator.cpp //
//////////////////////////////////////////////////////////////////

/**
 * 给对象分配内存空间
 */
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

//////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/memAllocator.cpp //
//////////////////////////////////////////////////////////////////

/**
 * 给对象分配内存空间
 */
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

/**
 * 在TLAB中分配失败, 开始慢速分配
 */
HeapWord* MemAllocator::mem_allocate_slow(Allocation& allocation) const {
  // Allocation of an oop can always invoke a safepoint.
  debug_only(JavaThread::cast(_thread)->check_for_valid_safepoint_state());

  if (UseTLAB) {
    // 申请一个新的TLAB, 并在新的TLAB中分配对象内存
    HeapWord* mem = mem_allocate_inside_tlab_slow(allocation);
    if (mem != nullptr) {
      return mem;
    }
  }
  // 还是失败, 直接在堆中分配对象内存
  return mem_allocate_outside_tlab(allocation);
}
```
