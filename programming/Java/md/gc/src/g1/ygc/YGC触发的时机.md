# YGC 触发的时机

在创建对象时若申请不到内存，则会触发一次 Young GC：

> jdk8u60-master\hotspot\src\share\vm\interpreter\bytecodeInterpreter.cpp

```cpp
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
        // 设置压缩指针
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

  // 确保没有实例化一个抽象类
  klass->check_valid_for_instantiation(true, CHECK);

  // 确保Kalss对象已经初始化
  klass->initialize(CHECK);

  // 创建对象
  oop obj = klass->allocate_instance(CHECK);
  // 将结果放到当前线程的_vm_result字段中，
  // 用来传递给解释器
  thread->set_vm_result(obj);
IRT_END
```
