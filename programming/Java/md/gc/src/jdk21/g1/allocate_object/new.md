# 对象的分配

创建一个对象通常是 new, dup, invokespecial 三条指令一起出现:

1. new 指令会分配一块内存空间给新的对象使用, new 指令执行完成后会把新对象的引用放入操作数栈的栈顶给后续的 dup 指令使用
2. dup 指令会把栈顶的对象引用复制一份给后面的 invokespecial 指令使用
3. invokespecial 指令会调用 `<init>` 方法初始化对象的字段

new 指令的执行过程:

![](../../../img/op_new.png)

## C++ 解释器

hotspot 有两个解释器, 基于 C++ 的解释器和基于汇编的模板解释器, hotspot 默认使用比较快的模板解释器。

基于 C++ 的解释器更加清晰直观, 便于理解。

```cpp
// --- src/hotspot/share/interpreter/zero/bytecodeInterpreter.cpp --- //

void BytecodeInterpreter::run(interpreterState istate) {
    {
        switch (opcode)
        {
            CASE(_new):
            {
                u2 index = Bytes::get_Java_u2(pc + 1);

                // 首先尝试从TLAB中分配内存空间
                //
                // 前提条件:
                //   - klass已经被初始化过
                //   - klass需要支持快速分配内存空间
                //   - 允许在TLAB上分配内存空间

                // 运行时常量池
                ConstantPool *constants = istate->method()->constants();
                // 判断是否允许在TLAB上分配内存空间,
                // 并且常量池中index索引上的是一个可以解析的klass对象
                if (UseTLAB && !constants->tag_at(index).is_unresolved_klass()) {
                    // 从常量池中取出klass对象
                    Klass *entry = constants->resolved_klass_at(index);
                    InstanceKlass *ik = InstanceKlass::cast(entry);
                    // 确保klass已经被初始化过,
                    // 并且klass支持快速分配内存空间
                    if (ik->is_initialized() && ik->can_be_fastpath_allocated()) {
                        // 获取对象的大小
                        // 一个类的对象有多大在编译时就已经确定
                        size_t obj_size = ik->size_helper();
                        // 尝试从TLAB中分配对象的内存空间,
                        // result指向新对象内存的首地址
                        HeapWord *result = THREAD->tlab().allocate(obj_size);
                        if (result != nullptr) {
                            // 把对象的内存空间用0填充:
                            //   - 如果TLAB在创建时已经把自己的内存格式化成0, 这步就可以跳过
                            //   - 在debug模式下, 这块内存空间会被ThreadLocalAllocBuffer::allocate修改,
                            //     所以不管TLAB有没有格式化, 都要重新填充一遍
                            // 这步操作保证了对象的实例字段在Java代码中可以不赋初始值就直接使用，
                            // 程序能访问到这些字段的数据类型所对应的零值
                            if (DEBUG_ONLY(true || ) !ZeroTLAB) {
                                size_t hdr_size = oopDesc::header_size();
                                Copy::fill_to_words(result + hdr_size, obj_size - hdr_size, 0);
                            }

                            // 设置对象头
                            // 初始化 mark word
                            oopDesc::set_mark(result, markWord::prototype());
                            // 设置GC分代年龄
                            oopDesc::set_klass_gap(result, 0);
                            // 设置元数据指针
                            oopDesc::release_set_klass(result, ik);

                            // 转换成对象指针
                            oop obj = cast_to_oop(result);

                            // 使用StoreStore屏障禁止指令重排序,
                            // 防止把对象头还没初始化完成的对象入栈
                            OrderAccess::storestore();
                            // 把这个对象的指针放到操作数栈的栈顶给后续的dup指令使用
                            SET_STACK_OBJECT(obj, 0);
                            // 更新程序计数器, new指令执行完毕, new指令总共3个字节(操作码+操作数), PC加3
                            UPDATE_PC_AND_TOS_AND_CONTINUE(3, 1);
                        }
                    }
                }
                // 从TLAB中分配内存空间失败, 开始慢速分配
                CALL_VM(InterpreterRuntime::_new(THREAD, METHOD->constants(), index),
                        handle_exception);
                // 使用StoreStore屏障禁止重排序,
                // 防止把对象头还没初始化完成的对象入栈
                OrderAccess::storestore();
                // InterpreterRuntime::_new中分配的对象会保存在vm_result中,
                // 将对象的指针取出, 并放到操作数栈的栈顶给后续的dup指令使用
                SET_STACK_OBJECT(THREAD->vm_result(), 0);
                // 清空vm_result
                THREAD->set_vm_result(nullptr);
                // 更新程序计数器
                UPDATE_PC_AND_TOS_AND_CONTINUE(3, 1);
            }
        }
    }
}

// --- src/hotspot/share/oops/instanceKlass.hpp --- //

class InstanceKlass: public Klass {
    // 判断klass是否支持快速分配内存空间
    // _layout_helper在classFileParser.cpp中初始化
    // 它在下面几种情况时为false:
    //  - 这个类是抽象类或者接口
    //  - 这个类有不为空的finalize()方法
    //  - 这个类的大小超过了FastAllocateSizeLimit
    //  - 这个类是java.lang.Class, java.lang.Class不能直接分配内存空间
    bool can_be_fastpath_allocated() const {
        // klass的_layout_helper变量中保存了是否支持快速分配的标志
        // layout_helper_needs_slow_path 在
        // (_layout_helper & 0x01) != 0 时 返回 true
        return !layout_helper_needs_slow_path(layout_helper());
    }
}
```

## 模板解释器

```cpp
// --- src/hotspot/cpu/aarch64/templateTable_aarch64.cpp --- //

void TemplateTable::_new() {
    transition(vtos, atos);

    __ get_unsigned_2_byte_index_at_bcp(r3, 1);
    Label slow_case;
    Label done;
    Label initialize_header;

    __ get_cpool_and_tags(r4, r0);
    // Make sure the class we're about to instantiate has been resolved.
    // This is done before loading InstanceKlass to be consistent with the order
    // how Constant Pool is updated (see ConstantPool::klass_at_put)
    const int tags_offset = Array<u1>::base_offset_in_bytes();
    __ lea(rscratch1, Address(r0, r3, Address::lsl(0)));
    __ lea(rscratch1, Address(rscratch1, tags_offset));
    __ ldarb(rscratch1, rscratch1);
    __ cmp(rscratch1, (u1) JVM_CONSTANT_Class);
    __ br(Assembler::NE, slow_case);

    // get InstanceKlass
    __ load_resolved_klass_at_offset(r4, r3, r4, rscratch1);

    // make sure klass is initialized & doesn't have finalizer
    // make sure klass is fully initialized
    __ ldrb(rscratch1, Address(r4, InstanceKlass::init_state_offset()));
    __ cmp(rscratch1, (u1) InstanceKlass::fully_initialized);
    __ br(Assembler::NE, slow_case);

    // get instance_size in InstanceKlass (scaled to a count of bytes)
    __ ldrw(r3,
            Address(r4,
                    Klass::layout_helper_offset()));
    // test to see if it has a finalizer or is malformed in some way
    __ tbnz(r3, exact_log2(Klass::_lh_instance_slow_path_bit), slow_case);

    // Allocate the instance:
    //  If TLAB is enabled:
    //    Try to allocate in the TLAB.
    //    If fails, go to the slow path.
    //    Initialize the allocation.
    //    Exit.
    //
    //  Go to slow path.

    if (UseTLAB) {
        __ tlab_allocate(r0, r3, 0, noreg, r1, slow_case);

        if (ZeroTLAB) {
            // the fields have been already cleared
            __ b(initialize_header);
        }

        // The object is initialized before the header.  If the object size is
        // zero, go directly to the header initialization.
        __ sub(r3, r3, sizeof(oopDesc));
        __ cbz(r3, initialize_header);

        // Initialize object fields
        {
            __ add(r2, r0, sizeof(oopDesc));
            Label loop;
            __ bind(loop);
            __ str(zr, Address(__ post(r2, BytesPerLong)));
            __ sub(r3, r3, BytesPerLong);
            __ cbnz(r3, loop);
        }

        // initialize object header only.
        __ bind(initialize_header);
        __ mov(rscratch1, (intptr_t) markWord::prototype().value());
        __ str(rscratch1, Address(r0, oopDesc::mark_offset_in_bytes()));
        __ store_klass_gap(r0, zr);  // zero klass gap for compressed oops
        __ store_klass(r0, r4);      // store klass last

        {
            SkipIfEqual skip(_masm, &DTraceAllocProbes, false);
            // Trigger dtrace event for fastpath
            __ push(atos); // save the return value
            __ call_VM_leaf(
                    CAST_FROM_FN_PTR(address, static_cast<int (*)(oopDesc *)>(SharedRuntime::dtrace_object_alloc)), r0);
            __ pop(atos); // restore the return value

        }
        __ b(done);
    }

    // slow case
    __ bind(slow_case);
    __ get_constant_pool(c_rarg1);
    __ get_unsigned_2_byte_index_at_bcp(c_rarg2, 1);
    call_VM(r0, CAST_FROM_FN_PTR(address, InterpreterRuntime::_new), c_rarg1, c_rarg2);
    __ verify_oop(r0);

    // continue
    __ bind(done);
    // Must prevent reordering of stores for object initialization with stores that publish the new object.
    __ membar(Assembler::StoreStore);
}
```
