# ConstMethod

ConstMethod 用来存放或定位方法中的只读数据, 如字节码、方法引用、方法名、方法签名和异常表等。

// An ConstMethod represents portions of a Java method which are not written to after
// the classfile is parsed(\*see below). This part of the method can be shared across
// processes in a read-only section with Class Data Sharing (CDS). It's important
// that this class doesn't have virtual functions because the vptr cannot be shared
// with CDS.
//
// Note that most applications load thousands of methods, so keeping the size of this
// structure small has a big impact on footprint.

// The actual bytecodes are inlined after the end of the ConstMethod struct.
//
// The line number table is compressed and inlined following the byte codes. It is
// found as the first byte following the byte codes. Note that accessing the line
// number and local variable tables is not performance critical at all.
//
// The checked exceptions table and the local variable table are inlined after the
// line number table, and indexed from the end of the method. We do not compress the
// checked exceptions table since the average length is less than 2, and it is used
// by reflection so access should be fast. We do not bother to compress the local
// variable table either since it is mostly absent.
//
//
// ConstMethod 内置的字段(紧跟在类中声明的字段之后的内存位置)
// [EMBEDDED byte codes]
// [EMBEDDED compressed linenumber table]
// (see class CompressedLineNumberReadStream)
// (note that length is unknown until decompressed)
// (access flags bit tells whether table is present)
// (indexed from start of ConstMethod)
// (elements not necessarily sorted!)
// [EMBEDDED localvariable table elements + length (length last)]
// (length is u2, elements are 6-tuples of u2)
// (see class LocalVariableTableElement)
// (access flags bit tells whether table is present)
// (indexed from end of ConstMethod*)
// [EMBEDDED exception table + length (length last)]
// (length is u2, elements are 4-tuples of u2)
// (see class ExceptionTableElement)
// (access flags bit tells whether table is present)
// (indexed from end of ConstMethod*)
// [EMBEDDED checked exceptions elements + length (length last)]
// (length is u2, elements are u2)
// (see class CheckedExceptionElement)
// (access flags bit tells whether table is present)
// (indexed from end of ConstMethod*)
// [EMBEDDED method parameters elements + length (length last)]
// (length is u2, elements are u2, u4 structures)
// (see class MethodParametersElement)
// (access flags bit tells whether table is present)
// (indexed from end of ConstMethod*)
// [EMBEDDED generic signature index (u2)]
// (indexed from end of constMethodOop)
// [EMBEDDED annotations arrays - method, parameter, type, default]
// pointer to `Array<u1>` if annotation is present
//
// IMPORTANT: If anything gets added here, there need to be changes to
// ensure that ServicabilityAgent doesn't get broken as a result!

```cpp
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

  ConstantPool*     _constants;                  // Constant pool

  // Raw stackmap data for the method
  Array<u1>*        _stackmap_data;

  int               _constMethod_size;
  ConstMethodFlags  _flags;                       // for sizing
  u1                _result_type;                 // BasicType of result

  // 字节码的长度
  u2                _code_size;
  u2                _name_index;                 // Method name (index in constant pool)
  u2                _signature_index;            // Method signature (index in constant pool)
  u2                _method_idnum;               // unique identification number for the method within the class
                                                 // initially corresponds to the index into the methods array.
                                                 // but this may change with redefinition
  u2                _max_stack;                  // Maximum number of entries on the expression stack
  u2                _max_locals;                 // Number of local variables used by this method
  u2                _size_of_parameters;         // size of the parameter block (receiver + arguments) in words
  u2                _num_stack_arg_slots;        // Number of arguments passed on the stack even when compiled
  u2                _orig_method_idnum;          // Original unique identification number for the method
  // ...
};
```
