# InstanceKlass

```cpp
// --- src/hotspot/share/oops/instanceKlass.hpp --- //

class InstanceKlass: public Klass {
 public:
  static const KlassKind Kind = InstanceKlassKind;

 public:
  // See "The Java Virtual Machine Specification" section 2.16.2-5 for a detailed description
  // of the class loading & initialization procedure, and the use of the states.
  enum ClassState : u1 {
    allocated,                          // allocated (but not yet linked)
    loaded,                             // loaded and inserted in class hierarchy (but not linked yet)
    being_linked,                       // currently running verifier and rewriter
    linked,                             // successfully linked/verified (but not initialized yet)
    being_initialized,                  // currently running class initializer
    fully_initialized,                  // initialized (successful final state)
    initialization_error                // error happened during initialization
  };

 protected:
  // If you add a new field that points to any metaspace object, you
  // must add this field to InstanceKlass::metaspace_pointers_do().

  // Annotations for this class
  Annotations*    _annotations;
  // Package this class is defined in
  PackageEntry*   _package_entry;
  // Array classes holding elements of this class.
  ObjArrayKlass* volatile _array_klasses;
  // Constant pool for this class.
  ConstantPool* _constants;
  // The InnerClasses attribute and EnclosingMethod attribute. The
  // _inner_classes is an array of shorts. If the class has InnerClasses
  // attribute, then the _inner_classes array begins with 4-tuples of shorts
  // [inner_class_info_index, outer_class_info_index,
  // inner_name_index, inner_class_access_flags] for the InnerClasses
  // attribute. If the EnclosingMethod attribute exists, it occupies the
  // last two shorts [class_index, method_index] of the array. If only
  // the InnerClasses attribute exists, the _inner_classes array length is
  // number_of_inner_classes * 4. If the class has both InnerClasses
  // and EnclosingMethod attributes the _inner_classes array length is
  // number_of_inner_classes * 4 + enclosing_method_attribute_size.
  Array<jushort>* _inner_classes;

  // The NestMembers attribute. An array of shorts, where each is a
  // class info index for the class that is a nest member. This data
  // has not been validated.
  Array<jushort>* _nest_members;

  // Resolved nest-host klass: either true nest-host or self if we are not
  // nested, or an error occurred resolving or validating the nominated
  // nest-host. Can also be set directly by JDK API's that establish nest
  // relationships.
  // By always being set it makes nest-member access checks simpler.
  InstanceKlass* _nest_host;

  // The PermittedSubclasses attribute. An array of shorts, where each is a
  // class info index for the class that is a permitted subclass.
  Array<jushort>* _permitted_subclasses;

  // The contents of the Record attribute.
  Array<RecordComponent*>* _record_components;

  // the source debug extension for this klass, null if not specified.
  // Specified as UTF-8 string without terminating zero byte in the classfile,
  // it is stored in the instanceklass as a null-terminated UTF-8 string
  const char*     _source_debug_extension;

  // Number of heapOopSize words used by non-static fields in this klass
  // (including inherited fields but after header_size()).
  int             _nonstatic_field_size;
  int             _static_field_size;       // number words used by static fields (oop and non-oop) in this klass
  int             _nonstatic_oop_map_size;  // size in words of nonstatic oop map blocks
  int             _itable_len;              // length of Java itable (in words)

  // The NestHost attribute. The class info index for the class
  // that is the nest-host of this class. This data has not been validated.
  u2              _nest_host_index;
  u2              _this_class_index;        // constant pool entry
  u2              _static_oop_field_count;  // number of static oop fields in this klass

  volatile u2     _idnum_allocated_count;   // JNI/JVMTI: increments with the addition of methods, old ids don't change

  volatile ClassState _init_state;          // state of class

  u1              _reference_type;          // reference type

  // State is set either at parse time or while executing, atomically to not disturb other state
  InstanceKlassFlags _misc_flags;

  Monitor*             _init_monitor;       // mutual exclusion to _init_state and _init_thread.
  JavaThread* volatile _init_thread;        // Pointer to current thread doing initialization (to handle recursive initialization)

  OopMapCache*    volatile _oop_map_cache;   // OopMapCache for all methods in the klass (allocated lazily)
  JNIid*          _jni_ids;              // First JNI identifier for static fields in this class
  jmethodID*      volatile _methods_jmethod_ids;  // jmethodIDs corresponding to method_idnum, or null if none
  nmethodBucket*  volatile _dep_context;          // packed DependencyContext structure
  uint64_t        volatile _dep_context_last_cleaned;
  nmethod*        _osr_nmethods_head;    // Head of list of on-stack replacement nmethods for this class
#if INCLUDE_JVMTI
  BreakpointInfo* _breakpoints;          // bpt lists, managed by Method*
  // Linked instanceKlasses of previous versions
  InstanceKlass* _previous_versions;
  // JVMTI fields can be moved to their own structure - see 6315920
  // JVMTI: cached class file, before retransformable agent modified it in CFLH
  JvmtiCachedClassFileData* _cached_class_file;
#endif

#if INCLUDE_JVMTI
  JvmtiCachedClassFieldMap* _jvmti_cached_class_field_map;  // JVMTI: used during heap iteration
#endif

  NOT_PRODUCT(int _verify_count;)  // to avoid redundant verifies
  NOT_PRODUCT(volatile int _shared_class_load_count;) // ensure a shared class is loaded only once

  // 类拥有的方法列表
  Array<Method*>* _methods;
  // Default Method Array, concrete methods inherited from interfaces
  Array<Method*>* _default_methods;
  // 实现的接口
  Array<InstanceKlass*>* _local_interfaces;
  // 继承来的接口
  Array<InstanceKlass*>* _transitive_interfaces;
  // Int array containing the original order of method in the class file (for JVMTI).
  Array<int>*     _method_ordering;
  // Int array containing the vtable_indices for default_methods
  // offset matches _default_methods offset
  Array<int>*     _default_vtable_indices;

  // Fields information is stored in an UNSIGNED5 encoded stream (see fieldInfo.hpp)
  Array<u1>*          _fieldinfo_stream;
  Array<FieldStatus>* _fields_status;

  // embedded Java vtable follows here
  // embedded Java itables follows here
  // embedded static fields follows here
  // embedded nonstatic oop-map blocks follows here
  // embedded implementor of this interface follows here
  //   The embedded implementor only exists if the current klass is an
  //   interface. The possible values of the implementor fall into following
  //   three cases:
  //     null: no implementor.
  //     A Klass* that's not itself: one implementor.
  //     Itself: more than one implementors.
  //

  friend class SystemDictionary;

  static bool _disable_method_binary_search;

  // Controls finalizer registration
  static bool _finalization_enabled;
};
```
