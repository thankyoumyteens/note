# new 关键字

Hotspot 有两个解释器，基于 C++的解释器和基于汇编的模板解释器，hotspot 默认使用比较快的模板解释器。

基于 C++的解释器更加清晰直观，便于理解：

> jdk8u60-master\hotspot\src\share\vm\interpreter\bytecodeInterpreter.cpp

```cpp
// 基于C++的解释器
// Java使用new关键字时会调用到这里
CASE(_new): {
  // 获取操作数栈中的要创建对象的类的符号引用在常量池的索引
  u2 index = Bytes::get_Java_u2(pc+1);
  // 获取当前执行的方法所在类的常量池，
  // istate是当前字节码解释器BytecodeInterpreter实例的指针
  ConstantPool* constants = istate->method()->constants();
  // 如果目标类已经解析
  if (!constants->tag_at(index).is_unresolved_klass()) {
    // 从常量池获取Klass
    Klass* entry = constants->slot_at(index).get_klass();
    // 校验从常量池获取的Klass是否是InstanceKlass类型
    assert(entry->is_klass(), "Should be resolved klass");
    Klass* k_entry = (Klass*) entry;
    assert(k_entry->oop_is_instance(), "Should be InstanceKlass");
    // 转成InstanceKlass
    InstanceKlass* ik = (InstanceKlass*) k_entry;
    // 如果Klass已经完成初始化，并且可以使用快速分配的方式创建对象
    if ( ik->is_initialized() && ik->can_be_fastpath_allocated() ) {
      // 获取要创建的对象的大小
      size_t obj_size = ik->size_helper();
      oop result = NULL;
      // 判断TLAB中的内存是否已经初始化为0值，
      // need_zero表示是否需要把对象的内存初始化为0值
      bool need_zero = !ZeroTLAB;
      if (UseTLAB) {
        // 在TLAB中快速分配对象
        result = (oop) THREAD->tlab().allocate(obj_size);
      }
#ifndef CC_INTERP_PROFILE
      if (result == NULL) {
        need_zero = true;
        // 尝试在共享的eden区分配
      retry:
        // 获取当前未分配内存空间的起始地址
        // HeapWord 是 JVM 管理的堆内存的地址抽象。
        // 堆中的内存地址都需要通过 HeapWord* 指针进行表示，
        // 例如申请内存起始地址的函数一般返回的都是HeapWord*， 大小也是 HeapWordSize 的整数倍，
        // 因为 Java 堆是按照一定内存大小对齐的
        HeapWord* compare_to = *Universe::heap()->top_addr();
        // 起始地址加上要创建的对象的大小
        HeapWord* new_top = compare_to + obj_size;
        // 判断是否超出了eden区
        if (new_top <= *Universe::heap()->end_addr()) {
          // 如果没有超过则通过CAS的方式尝试分配
          // cmpxchg_ptr函数是比较top_addr的地址和compare_to的地址是否一样，
          // 如果一样则将new_top的地址写入top_addr中并返回compare_to
          // 如果不相等，说明此时eden区分配了新对象，
          // 则返回top_addr新的地址，即返回结果不等于compare_to，分配失败
          if (Atomic::cmpxchg_ptr(new_top, Universe::heap()->top_addr(), compare_to) != compare_to) {
            // 分配失败就跳回retry，一直尝试直到不能分配为止
            goto retry;
          }
          result = (oop) compare_to;
        }
      }
#endif
      // 判断快速分配是否成功
      if (result != NULL) {
        if (need_zero ) {
          // 把对象的内存初始化为0值
          HeapWord* to_zero = (HeapWord*) result + sizeof(oopDesc) / oopSize;
          obj_size -= sizeof(oopDesc) / oopSize;
          if (obj_size > 0 ) {
            memset(to_zero, 0, obj_size * HeapWordSize);
          }
        }
        // 设置对象头
        if (UseBiasedLocking) {
          // 使用偏向锁
          result->set_mark(ik->prototype_header());
        } else {
          result->set_mark(markOopDesc::prototype());
        }
        // 设置GC分代年龄
        result->set_klass_gap(0);
        // 设置类型指针
        result->set_klass(k_entry);
        // 使用StoreStore屏障把写入操作强制刷新回主内存
        OrderAccess::storestore();
        // 把这个对象放到操作数栈的顶部
        SET_STACK_OBJECT(result, 0);
        // 更新程序计数器，此条new指令执行完毕，new指令总共3个字节，计数器加3
        UPDATE_PC_AND_TOS_AND_CONTINUE(3, 1);
      }
    }
  }
  // 快速分配失败了，执行慢速分配
  CALL_VM(InterpreterRuntime::_new(THREAD, METHOD->constants(), index),
          handle_exception);
  // StoreStore屏障
  OrderAccess::storestore();
  // 慢速分配的对象会保存在vm_result中，
  // 将对象取出，并放到操作数栈的顶部
  SET_STACK_OBJECT(THREAD->vm_result(), 0);
  // 清空vm_result
  THREAD->set_vm_result(NULL);
  // 更新程序计数器
  UPDATE_PC_AND_TOS_AND_CONTINUE(3, 1);
}
```

慢速分配时对象分配和初始化的逻辑和快速分配基本一致，最大的区别在于慢速分配会执行类的初始化，执行类的 finalize()方法的注册，正是因为目标类的初始化比较耗时所以才称为慢速分配。

执行 new，getstatic,putstatic,invokestatic 指令时会触发类的初始化，即某个类第一次 new 时执行的是慢速分配，然后该类完成初始化，下次 new 时基本就可以通过快速分配的方式创建对象了。

> jdk8u60-master\hotspot\src\share\vm\interpreter\interpreterRuntime.cpp

```cpp
/**
 * 对象的慢速分配
 */
IRT_ENTRY(void, InterpreterRuntime::_new(JavaThread* thread, ConstantPool* pool, int index))
  // 先去运行时常量池中查找Klass
  Klass* k_oop = pool->klass_at(index, CHECK);
  // 把Klass包装成instanceKlassHandle
  instanceKlassHandle klass (THREAD, k_oop);

  // 校验Klass是否是抽象类，接口或者java.lang.Class,如果是则抛出异常
  klass->check_valid_for_instantiation(true, CHECK);

  // 检查Klass是否已经完成初始化，如果未完成则执行初始化
  klass->initialize(CHECK);

  // 创建对象
  oop obj = klass->allocate_instance(CHECK);
  // 将结果放到当前线程的_vm_result字段中，
  // 用来传递给解释器
  thread->set_vm_result(obj);
IRT_END
```

> jdk8u60-master\hotspot\src\share\vm\oops\instanceKlass.cpp

```cpp
/**
 * 创建对象
 *
 * instanceOop是instanceOopDesc的别名：
 * typedef class instanceOopDesc* instanceOop;
 */
instanceOop InstanceKlass::allocate_instance(TRAPS) {
  // 判断是否定义了finalize()方法
  bool has_finalizer_flag = has_finalizer();
  // 获取对象的大小
  int size = size_helper();
  // 对象所属的Klass
  KlassHandle h_k(THREAD, this);

  instanceOop i;
  // 创建对象
  i = (instanceOop)CollectedHeap::obj_allocate(h_k, size, CHECK_NULL);
  // 如果重写了finalize()方法
  // 并且RegisterFinalizersAtInit为false，
  // 即不在JVM启动时完成finalize()方法的注册
  if (has_finalizer_flag && !RegisterFinalizersAtInit) {
    // 注册finalize()方法
    i = register_finalizer(i, CHECK_NULL);
  }
  return i;
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_interface\collectedHeap.inline.hpp

```cpp
/**
 * 创建对象
 */
oop CollectedHeap::obj_allocate(KlassHandle klass, int size, TRAPS) {
  // 检查Java堆是否正在gc
  assert(!Universe::heap()->is_gc_active(), "Allocation during gc not allowed");
  assert(size >= 0, "int won't convert to size_t");
  // 申请内存并初始化对象
  HeapWord* obj = common_mem_allocate_init(klass, size, CHECK_NULL);
  // 设置对象头和klass指针
  post_allocation_setup_obj(klass, obj, size);
  // 检查分配的内存是否正常，生产环境不执行
  NOT_PRODUCT(Universe::heap()->check_for_bad_heap_word_value(obj, size));
  return (oop)obj;
}

/**
 * 申请内存并初始化对象
 */
HeapWord* CollectedHeap::common_mem_allocate_init(KlassHandle klass, size_t size, TRAPS) {
  // 申请内存
  HeapWord* obj = common_mem_allocate_noinit(klass, size, CHECK_NULL);
  // 初始化对象
  init_obj(obj, size);
  return obj;
}

/**
 * 申请内存
 */
HeapWord* CollectedHeap::common_mem_allocate_noinit(KlassHandle klass, size_t size, TRAPS) {

  // 清理当前线程TLAB中未使用的opp
  CHECK_UNHANDLED_OOPS_ONLY(THREAD->clear_unhandled_oops();)
  // 判断是否发生异常
  if (HAS_PENDING_EXCEPTION) {
    NOT_PRODUCT(guarantee(false, "Should not allocate with exception pending"));
    return NULL;
  }

  HeapWord* result = NULL;
  // 判断是否使用TLAB
  if (UseTLAB) {
    // 从TLAB分配内存
    result = allocate_from_tlab(klass, THREAD, size);
    if (result != NULL) {
      assert(!HAS_PENDING_EXCEPTION,
             "Unexpected exception, will result in uninitialized storage");
      return result;
    }
  }
  // 没有开启TLAB或者TLAB分配失败，
  // 从Java堆中分配内存
  bool gc_overhead_limit_was_exceeded = false;
  // Universe::heap ()方法返回的是当前JVM使用的堆类，
  // 因为使用的是G1垃圾回收器，所以返回的是G1CollectedHeap
  result = Universe::heap()->mem_allocate(size,
                                          &gc_overhead_limit_was_exceeded);
  // 判断是否分配成功
  if (result != NULL) {
    // 分配成功
    NOT_PRODUCT(Universe::heap()->
      check_for_non_bad_heap_word_value(result, size));
    assert(!HAS_PENDING_EXCEPTION,
           "Unexpected exception, will result in uninitialized storage");
    // 增加当前线程中记录已分配的内存大小的字段
    THREAD->incr_allocated_bytes(size * HeapWordSize);
    // 发送堆内存对象分配事件
    AllocTracer::send_allocation_outside_tlab_event(klass, size * HeapWordSize);

    return result;
  }

  // 分配失败，抛出异常
  if (!gc_overhead_limit_was_exceeded) {
    // 当前堆内存严重不足
    // 用于实现-XX:+HeapDumpOnOutOfMemoryError 和 -XX:OnOutOfMemoryError参数
    report_java_out_of_memory("Java heap space");
    // 通知JVMTI
    if (JvmtiExport::should_post_resource_exhausted()) {
      JvmtiExport::post_resource_exhausted(
        JVMTI_RESOURCE_EXHAUSTED_OOM_ERROR | JVMTI_RESOURCE_EXHAUSTED_JAVA_HEAP,
        "Java heap space");
    }
    // 抛出异常
    THROW_OOP_0(Universe::out_of_memory_error_java_heap());
  } else {
    // 执行GC后仍不能有效回收内存导致内存不足
    // 用于实现-XX:+HeapDumpOnOutOfMemoryError 和 -XX:OnOutOfMemoryError参数
    report_java_out_of_memory("GC overhead limit exceeded");
    // 通知JVMTI
    if (JvmtiExport::should_post_resource_exhausted()) {
      JvmtiExport::post_resource_exhausted(
        JVMTI_RESOURCE_EXHAUSTED_OOM_ERROR | JVMTI_RESOURCE_EXHAUSTED_JAVA_HEAP,
        "GC overhead limit exceeded");
    }
    // 抛出异常
    THROW_OOP_0(Universe::out_of_memory_error_gc_overhead_limit());
  }
}

/**
 * 初始化对象
 */
void CollectedHeap::init_obj(HeapWord* obj, size_t size) {
  assert(obj != NULL, "cannot initialize NULL object");
  const size_t hs = oopDesc::header_size();
  assert(size >= hs, "unexpected object size");
  // 设置GC分代年龄
  ((oop)obj)->set_klass_gap(0);
  // 将分配的对象内存全部初始化为0值
  Copy::fill_to_aligned_words(obj + hs, size - hs);
}

/**
 * 设置对象头和klass指针
 */
void CollectedHeap::post_allocation_setup_obj(KlassHandle klass,
                                              HeapWord* obj,
                                              int size) {
  post_allocation_setup_common(klass, obj);
  assert(Universe::is_bootstrapping() ||
         !((oop)obj)->is_array(), "must not be an array");
  // 通知jvmti对象已创建，如果DTraceAllocProbes为true则打印日志
  post_allocation_notify(klass, (oop)obj, size);
}

void CollectedHeap::post_allocation_setup_common(KlassHandle klass,
                                                 HeapWord* obj) {
  post_allocation_setup_no_klass_install(klass, obj);
  post_allocation_install_obj_klass(klass, oop(obj));
}

void CollectedHeap::post_allocation_setup_no_klass_install(KlassHandle klass,
                                                           HeapWord* objPtr) {
  oop obj = (oop)objPtr;

  assert(obj != NULL, "NULL object pointer");
  // 设置对象头
  if (UseBiasedLocking && (klass() != NULL)) {
    // 使用偏向锁
    obj->set_mark(klass->prototype_header());
  } else {
    obj->set_mark(markOopDesc::prototype());
  }
}

void CollectedHeap::post_allocation_install_obj_klass(KlassHandle klass,
                                                   oop obj) {
  assert(klass() != NULL || !Universe::is_fully_initialized(), "NULL klass");
  assert(klass() == NULL || klass()->is_klass(), "not a klass");
  assert(obj != NULL, "NULL object pointer");
  // 设置对象的klass指针
  obj->set_klass(klass());
  assert(!Universe::is_fully_initialized() || obj->klass() != NULL,
         "missing klass");
}
```
