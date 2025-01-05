# 方法

JVM 内部是通过 Method 描述一个方法的。

Method 内置的字段(紧跟在类中声明的字段之后的内存位置)

- native_function 当前 Method 是 native 方法时存在
- signature_handler 当前 Method 是 native 方法时存在

```cpp
// --- src/hotspot/share/oops/method.hpp --- //

class Method : public Metadata {
 private:
  // If you add a new field that points to any metaspace object, you
  // must add this field to Method::metaspace_pointers_do().
  // 用来存放或定位方法中的只读数据, 如字节码、方法引用、方法名、方法签名和异常表等
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
```
