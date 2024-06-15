# Handle

如果想要避免某些 oop 在垃圾回收期间被回收, 可以通过 hadle 来分配并使用这些 oop。hadle 被分配在线程本地的 handle area 中。

```cpp
// --- src/hotspot/share/runtime/handles.hpp --- //

class Handle {
 private:
  // Handle封装的oop
  oop* _handle;

 protected:
  oop     obj() const                            { return _handle == nullptr ? (oop)nullptr : *_handle; }
  oop     non_null_obj() const                   { assert(_handle != nullptr, "resolving null handle"); return *_handle; }

 public:
  // Constructors
  Handle() {
    _handle = nullptr;
  }
  inline Handle(Thread* thread, oop obj) {
    assert(thread == Thread::current(), "sanity check");
    if (obj == nullptr) {
      _handle = nullptr;
    } else {
      // hadle 被分配在线程本地的 handle area 中
      _handle = thread->handle_area()->allocate_handle(obj);
    }
  }

  // 通过运算符重载简化handle操作
  // 通过()直接获取handle中封装的oop: oop obj1 = h1();
  oop     operator () () const                   { return obj(); }
  // 通过->直接调用handle内部oop的方法: h1->print();
  oop     operator -> () const                   { return non_null_obj(); }

  bool operator == (oop o) const                 { return obj() == o; }
  bool operator != (oop o) const                 { return obj() != o; }
  bool operator == (const Handle& h) const       { return obj() == h.obj(); }
  bool operator != (const Handle& h) const       { return obj() != h.obj(); }

  // Null checks
  bool    is_null() const                        { return _handle == nullptr; }
  bool    not_null() const                       { return _handle != nullptr; }

  // Debugging
  void    print()                                { obj()->print(); }

  // Direct interface, use very sparingly.
  // Used by JavaCalls to quickly convert handles and to create handles static data structures.
  // Constructor takes a dummy argument to prevent unintentional type conversion in C++.
  Handle(oop *handle, bool dummy)                { _handle = handle; }

  // Raw handle access. Allows easy duplication of Handles. This can be very unsafe
  // since duplicates is only valid as long as original handle is alive.
  oop* raw_value() const                         { return _handle; }
  static oop raw_resolve(oop *handle)            { return handle == nullptr ? (oop)nullptr : *handle; }

  inline void replace(oop obj);
};
```

对于每种类型的 xxxOop, JVM 也定义了对应的 xxxHandle:

```cpp
// --- src/hotspot/share/runtime/handles.hpp --- //

#define DEF_HANDLE(type, is_a)                   \
  class type##Handle: public Handle {            \
   protected:                                    \
    type##Oop    obj() const                     { return (type##Oop)Handle::obj(); } \
    type##Oop    non_null_obj() const            { return (type##Oop)Handle::non_null_obj(); } \
                                                 \
   public:                                       \
    /* Constructors */                           \
    type##Handle ()                              : Handle() {} \
    inline type##Handle (Thread* thread, type##Oop obj); \
    type##Handle (oop *handle, bool dummy)       : Handle(handle, dummy) {} \
                                                 \
    /* Operators for ease of use */              \
    type##Oop    operator () () const            { return obj(); } \
    type##Oop    operator -> () const            { return non_null_obj(); } \
  };


DEF_HANDLE(instance         , is_instance_noinline         )
DEF_HANDLE(stackChunk       , is_stackChunk_noinline       )
DEF_HANDLE(array            , is_array_noinline            )
DEF_HANDLE(objArray         , is_objArray_noinline         )
DEF_HANDLE(typeArray        , is_typeArray_noinline        )
```
