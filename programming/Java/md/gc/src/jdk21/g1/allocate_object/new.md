# new 字节码指令

hotspot 有两个解释器, 基于 C++ 的解释器和基于汇编的模板解释器, hotspot 默认使用比较快的模板解释器。

基于 C++ 的解释器更加清晰直观, 便于理解。

## 模板解释器

```cpp
///////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/cpu/x86/templateTable_x86.cpp //
///////////////////////////////////////////////////////////////

void TemplateTable::_new() {
  // 以__开头的是汇编代码
  transition(vtos, atos);
  __ get_unsigned_2_byte_index_at_bcp(rdx, 1);
  Label slow_case;
  Label slow_case_no_pop;
  Label done;
  Label initialize_header;

  __ get_cpool_and_tags(rcx, rax);

  // Make sure the class we're about to instantiate has been resolved.
  // This is done before loading InstanceKlass to be consistent with the order
  // how Constant Pool is updated (see ConstantPool::klass_at_put)
  const int tags_offset = Array<u1>::base_offset_in_bytes();
  __ cmpb(Address(rax, rdx, Address::times_1, tags_offset), JVM_CONSTANT_Class);
  __ jcc(Assembler::notEqual, slow_case_no_pop);

  // get InstanceKlass
  __ load_resolved_klass_at_index(rcx, rcx, rdx);
  __ push(rcx);  // save the contexts of klass for initializing the header

  // make sure klass is initialized & doesn't have finalizer
  // make sure klass is fully initialized
  __ cmpb(Address(rcx, InstanceKlass::init_state_offset()), InstanceKlass::fully_initialized);
  __ jcc(Assembler::notEqual, slow_case);

  // get instance_size in InstanceKlass (scaled to a count of bytes)
  __ movl(rdx, Address(rcx, Klass::layout_helper_offset()));
  // test to see if it has a finalizer or is malformed in some way
  __ testl(rdx, Klass::_lh_instance_slow_path_bit);
  __ jcc(Assembler::notZero, slow_case);

  // Allocate the instance:
  //  If TLAB is enabled:
  //    Try to allocate in the TLAB.
  //    If fails, go to the slow path.
  //    Initialize the allocation.
  //    Exit.
  //
  //  Go to slow path.

  const Register thread = LP64_ONLY(r15_thread) NOT_LP64(rcx);

  if (UseTLAB) {
    NOT_LP64(__ get_thread(thread);)
    __ tlab_allocate(thread, rax, rdx, 0, rcx, rbx, slow_case);
    if (ZeroTLAB) {
      // the fields have been already cleared
      __ jmp(initialize_header);
    }

    // The object is initialized before the header.  If the object size is
    // zero, go directly to the header initialization.
    __ decrement(rdx, sizeof(oopDesc));
    __ jcc(Assembler::zero, initialize_header);

    // Initialize topmost object field, divide rdx by 8, check if odd and
    // test if zero.
    __ xorl(rcx, rcx);    // use zero reg to clear memory (shorter code)
    __ shrl(rdx, LogBytesPerLong); // divide by 2*oopSize and set carry flag if odd

    // rdx must have been multiple of 8
#ifdef ASSERT
    // make sure rdx was multiple of 8
    Label L;
    // Ignore partial flag stall after shrl() since it is debug VM
    __ jcc(Assembler::carryClear, L);
    __ stop("object size is not multiple of 2 - adjust this code");
    __ bind(L);
    // rdx must be > 0, no extra check needed here
#endif

    // initialize remaining object fields: rdx was a multiple of 8
    { Label loop;
    __ bind(loop);
    __ movptr(Address(rax, rdx, Address::times_8, sizeof(oopDesc) - 1*oopSize), rcx);
    NOT_LP64(__ movptr(Address(rax, rdx, Address::times_8, sizeof(oopDesc) - 2*oopSize), rcx));
    __ decrement(rdx);
    __ jcc(Assembler::notZero, loop);
    }

    // initialize object header only.
    __ bind(initialize_header);
    __ movptr(Address(rax, oopDesc::mark_offset_in_bytes()),
              (intptr_t)markWord::prototype().value()); // header
    __ pop(rcx);   // get saved klass back in the register.
#ifdef _LP64
    __ xorl(rsi, rsi); // use zero reg to clear memory (shorter code)
    __ store_klass_gap(rax, rsi);  // zero klass gap for compressed oops
#endif
    __ store_klass(rax, rcx, rscratch1);  // klass

    {
      SkipIfEqual skip_if(_masm, &DTraceAllocProbes, 0, rscratch1);
      // Trigger dtrace event for fastpath
      __ push(atos);
      __ call_VM_leaf(
           CAST_FROM_FN_PTR(address, static_cast<int (*)(oopDesc*)>(SharedRuntime::dtrace_object_alloc)), rax);
      __ pop(atos);
    }

    __ jmp(done);
  }

  // slow case
  __ bind(slow_case);
  __ pop(rcx);   // restore stack pointer to what it was when we came in.
  __ bind(slow_case_no_pop);

  Register rarg1 = LP64_ONLY(c_rarg1) NOT_LP64(rax);
  Register rarg2 = LP64_ONLY(c_rarg2) NOT_LP64(rdx);

  __ get_constant_pool(rarg1);
  __ get_unsigned_2_byte_index_at_bcp(rarg2, 1);
  // 调用InterpreterRuntime::_new给对象分配内存空间
  call_VM(rax, CAST_FROM_FN_PTR(address, InterpreterRuntime::_new), rarg1, rarg2);
   __ verify_oop(rax);

  // continue
  __ bind(done);
}
```

## C++ 解释器

```cpp
////////////////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/interpreter/zero/bytecodeInterpreter.cpp //
////////////////////////////////////////////////////////////////////////////////

CASE(_new): {
  u2 index = Bytes::get_Java_u2(pc+1);

  // 首先尝试从TLAB中分配内存空间
  //
  // 前提条件:
  //   - klass已经被初始化过
  //   - klass需要支持快速分配内存空间
  //   - 允许在TLAB上分配内存空间
  ConstantPool* constants = istate->method()->constants();
  // 判断是否允许在TLAB上分配内存空间,
  // 并且常量池中index索引上的是一个可以解析的klass对象
  if (UseTLAB && !constants->tag_at(index).is_unresolved_klass()) {
    // 从常量池中取出klass对象
    Klass* entry = constants->resolved_klass_at(index);
    InstanceKlass* ik = InstanceKlass::cast(entry);
    // 判断klass是否已经被初始化过,
    // 并且klass支持快速分配内存空间
    if (ik->is_initialized() && ik->can_be_fastpath_allocated()) {
      // 获取对象的大小
      // 一个类的对象有多大在编译时就已经确定
      size_t obj_size = ik->size_helper();
      // 尝试从TLAB中分配对象的内存空间
      HeapWord* result = THREAD->tlab().allocate(obj_size);
      if (result != nullptr) {
        // 把对象的内存空间用0填充:
        //   - 如果TLAB在创建时已经把自己的内存格式化成0, 这步就可以跳过
        //   - 在debug模式下, 这块内存空间会受ThreadLocalAllocBuffer::allocate影响,
        //     所以不管TLAB有没有格式化, 都要重新填充一遍
        if (DEBUG_ONLY(true ||) !ZeroTLAB) {
          size_t hdr_size = oopDesc::header_size();
          Copy::fill_to_words(result + hdr_size, obj_size - hdr_size, 0);
        }

        // 初始化 mark word
        oopDesc::set_mark(result, markWord::prototype());
        // 设置GC分代年龄
        oopDesc::set_klass_gap(result, 0);
        // 设置元数据指针
        oopDesc::release_set_klass(result, ik);

        oop obj = cast_to_oop(result);

        // 使用StoreStore屏障禁止重排序,
        // 防止把还没初始化完成的对象入栈
        OrderAccess::storestore();
        // 把这个对象放到操作数栈的栈顶
        SET_STACK_OBJECT(obj, 0);
        // 更新程序计数器, 此条new指令执行完毕, new指令总共3个字节, PC加3
        UPDATE_PC_AND_TOS_AND_CONTINUE(3, 1);
      }
    }
  }
  // 从TLAB中分配内存空间失败, 开始慢速分配
  CALL_VM(InterpreterRuntime::_new(THREAD, METHOD->constants(), index),
          handle_exception);
  // 使用StoreStore屏障禁止重排序,
  // 防止把还没初始化完成的对象入栈
  OrderAccess::storestore();
  // InterpreterRuntime::_new中分配的对象会保存在vm_result中,
  // 将对象取出, 并放到操作数栈的顶部
  SET_STACK_OBJECT(THREAD->vm_result(), 0);
  // 清空vm_result
  THREAD->set_vm_result(nullptr);
  // 更新程序计数器
  UPDATE_PC_AND_TOS_AND_CONTINUE(3, 1);
}

// jdk21-jdk-21-ga/src/hotspot/share/oops/instanceKlass.hpp
class InstanceKlass: public Klass {
  // 判断klass是否支持快速分配内存空间
  // _layout_helper在classFileParser.cpp中初始化
  // 它在下面几种情况时为false:
  //  - 这个类是抽象类或者接口
  //  - 这个类有不为空的finalize()方法
  //  - 这个类的大小超过了FastAllocateSizeLimit
  //  - 这个类是java.lang.Class, java.lang.Class不能直接分配内存空间
  bool can_be_fastpath_allocated() const {
    return !layout_helper_needs_slow_path(layout_helper());
  }
}
```
