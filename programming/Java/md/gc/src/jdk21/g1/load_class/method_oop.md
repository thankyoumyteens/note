# 方法

JVM 内部是通过 Method 描述一个方法的。

// A Method represents a Java method.
//
// Note that most applications load thousands of methods, so keeping the size of this
// class small has a big impact on footprint.
//
// Note that native_function and signature_handler have to be at fixed offsets
// (required by the interpreter)
//
//  Method embedded field layout (after declared fields):
//   [EMBEDDED native_function       (present only if native) ]
//   [EMBEDDED signature_handler     (present only if native) ]

```cpp
// --- src/hotspot/share/oops/method.hpp --- //

class Method : public Metadata {
 private:
  // If you add a new field that points to any metaspace object, you
  // must add this field to Method::metaspace_pointers_do().
  // 用来存放或定位方法中的只读数据，如字节码、方法引用、方法名、方法签名和异常表等
  ConstMethod*      _constMethod;
  MethodData*       _method_data;
  MethodCounters*   _method_counters;
  AdapterHandlerEntry* _adapter;
  // 访问标识
  AccessFlags       _access_flags;
  // 表示该方法在vtable表中的索引位置。vtable表用于函数分发机制
  int               _vtable_index;
  MethodFlags       _flags;

  u2                _intrinsic_id;               // vmSymbols::intrinsic_id (0 == _none)

  JFR_ONLY(DEFINE_TRACE_FLAG;)

#ifndef PRODUCT
  int64_t _compiled_invocation_count;

  Symbol* _name;
#endif
  // Entry point for calling both from and to the interpreter.
  // 解释器调用入口地址
  address _i2i_entry;           // All-args-on-stack calling convention
  // Entry point for calling from compiled code, to compiled code if it exists
  // or else the interpreter.
  // 编译代码入口
  volatile address _from_compiled_entry;        // Cache of: _code ? _code->entry_point() : _adapter->c2i_entry()
  // The entry point for calling both from and to compiled code is
  // "_code->entry_point()".  Because of tiered compilation and de-opt, this
  // field can come and go.  It can transition from null to not-null at any
  // time (whenever a compile completes).  It can transition from not-null to
  // null only at safepoints (because of a de-opt).
  CompiledMethod* volatile _code;                       // Points to the corresponding piece of native code
  volatile address           _from_interpreted_entry; // Cache of _code ? _adapter->i2c_entry() : _i2i_entry
  // ...
};

// --- src/hotspot/share/oops/constMethod.hpp --- //

class ConstMethod : public MetaspaceObj {
private:

  // Bit vector of signature
  // Callers interpret 0=not initialized yet and
  // -1=too many args to fix, must parse the slow way.
  // The real initial value is special to account for nonatomicity of 64 bit
  // loads and stores.  This value may updated and read without a lock by
  // multiple threads, so is volatile.
  volatile uint64_t _fingerprint;

  // If you add a new field that points to any metaspace object, you
  // must add this field to ConstMethod::metaspace_pointers_do().
  // 常量池
  ConstantPool*     _constants;

  // Raw stackmap data for the method
  Array<u1>*        _stackmap_data;

  int               _constMethod_size;
  ConstMethodFlags  _flags;                       // for sizing
  u1                _result_type;                 // BasicType of result

  // Size of Java bytecodes allocated immediately after Method*.
  u2                _code_size;
  u2                _name_index;                 // Method name (index in constant pool)
  u2                _signature_index;            // Method signature (index in constant pool)
  u2                _method_idnum;               // unique identification number for the method within the class
                                                 // initially corresponds to the index into the methods array.
                                                 // but this may change with redefinition
  // 操作数栈最大元素个数
  u2                _max_stack;
  // 局部变量表最大元素个数
  u2                _max_locals;
  u2                _size_of_parameters;         // size of the parameter block (receiver + arguments) in words
  u2                _num_stack_arg_slots;        // Number of arguments passed on the stack even when compiled
  u2                _orig_method_idnum;          // Original unique identification number for the method
  // ...
};
```
