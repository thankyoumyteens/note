# 系统字典

系统字典(System Dictionary)记录了系统加载的所有的类, 它持有了系统已加载类, 类加载器, 公共类 klass 等重要信息, 正如一个字典一样。

```cpp
// --- src/hotspot/share/classfile/systemDictionary.hpp --- //

class SystemDictionary : AllStatic {
 public:

  // Returns a class with a given class name and class loader.  Loads the
  // class if needed. If not found a NoClassDefFoundError or a
  // ClassNotFoundException is thrown, depending on the value on the
  // throw_error flag.  For most uses the throw_error argument should be set
  // to true.

  static Klass* resolve_or_fail(Symbol* class_name, Handle class_loader, Handle protection_domain, bool throw_error, TRAPS);
  // Convenient call for null loader and protection domain.
  static Klass* resolve_or_fail(Symbol* class_name, bool throw_error, TRAPS) {
    return resolve_or_fail(class_name, Handle(), Handle(), throw_error, THREAD);
  }

  // Returns a class with a given class name and class loader.
  // Loads the class if needed. If not found null is returned.
  static Klass* resolve_or_null(Symbol* class_name, Handle class_loader, Handle protection_domain, TRAPS);
  // Version with null loader and protection domain
  static Klass* resolve_or_null(Symbol* class_name, TRAPS) {
    return resolve_or_null(class_name, Handle(), Handle(), THREAD);
  }

  // Resolve a superclass or superinterface. Called from ClassFileParser,
  // parse_interfaces, resolve_instance_class_or_null, load_shared_class
  // "class_name" is the class whose super class or interface is being resolved.
  static InstanceKlass* resolve_super_or_fail(Symbol* class_name,
                                              Symbol* super_name,
                                              Handle class_loader,
                                              Handle protection_domain,
                                              bool is_superclass,
                                              TRAPS);
 private:
  // Parse the stream to create a hidden class.
  // Used by jvm_lookup_define_class.
  static InstanceKlass* resolve_hidden_class_from_stream(ClassFileStream* st,
                                                         Symbol* class_name,
                                                         Handle class_loader,
                                                         const ClassLoadInfo& cl_info,
                                                         TRAPS);

  // Resolve a class from stream (called by jni_DefineClass and JVM_DefineClass)
  // This class is added to the SystemDictionary.
  static InstanceKlass* resolve_class_from_stream(ClassFileStream* st,
                                                  Symbol* class_name,
                                                  Handle class_loader,
                                                  const ClassLoadInfo& cl_info,
                                                  TRAPS);

  static oop get_system_class_loader_impl(TRAPS);
  static oop get_platform_class_loader_impl(TRAPS);

 public:
  // Resolve either a hidden or normal class from a stream of bytes, based on ClassLoadInfo
  static InstanceKlass* resolve_from_stream(ClassFileStream* st,
                                            Symbol* class_name,
                                            Handle class_loader,
                                            const ClassLoadInfo& cl_info,
                                            TRAPS);

  // Lookup an already loaded class. If not found null is returned.
  static InstanceKlass* find_instance_klass(Thread* current, Symbol* class_name,
                                            Handle class_loader, Handle protection_domain);

  // Lookup an already loaded instance or array class.
  // Do not make any queries to class loaders; consult only the cache.
  // If not found null is returned.
  static Klass* find_instance_or_array_klass(Thread* current, Symbol* class_name,
                                             Handle class_loader,
                                             Handle protection_domain);

  // Lookup an instance or array class that has already been loaded
  // either into the given class loader, or else into another class
  // loader that is constrained (via loader constraints) to produce
  // a consistent class.  Do not take protection domains into account.
  // Do not make any queries to class loaders; consult only the cache.
  // Return null if the class is not found.
  //
  // This function is a strict superset of find_instance_or_array_klass.
  // This function (the unchecked version) makes a conservative prediction
  // of the result of the checked version, assuming successful lookup.
  // If both functions return non-null, they must return the same value.
  // Also, the unchecked version may sometimes be non-null where the
  // checked version is null.  This can occur in several ways:
  //   1. No query has yet been made to the class loader.
  //   2. The class loader was queried, but chose not to delegate.
  //   3. ClassLoader.checkPackageAccess rejected a proposed protection domain.
  //   4. Loading was attempted, but there was a linkage error of some sort.
  // In all of these cases, the loader constraints on this type are
  // satisfied, and it is safe for classes in the given class loader
  // to manipulate strongly-typed values of the found class, subject
  // to local linkage and access checks.
  static Klass* find_constrained_instance_or_array_klass(Thread* current,
                                                         Symbol* class_name,
                                                         Handle class_loader);

  static void classes_do(MetaspaceClosure* it);
  // Iterate over all methods in all klasses

  static void methods_do(void f(Method*));

  // Garbage collection support

  // Unload (that is, break root links to) all unmarked classes and
  // loaders.  Returns "true" iff something was unloaded.
  static bool do_unloading(GCTimer* gc_timer);

  // Printing
  static void print();
  static void print_on(outputStream* st);
  static void dump(outputStream* st, bool verbose);

  // Verification
  static void verify();

  // Initialization
  static void initialize(TRAPS);

public:
  // Returns java system loader
  static oop java_system_loader();

  // Returns java platform loader
  static oop java_platform_loader();

  // Compute the java system and platform loaders
  static void compute_java_loaders(TRAPS);

  // Register a new class loader
  static ClassLoaderData* register_loader(Handle class_loader, bool create_mirror_cld = false);

  static void set_system_loader(ClassLoaderData *cld);
  static void set_platform_loader(ClassLoaderData *cld);

  static Symbol* check_signature_loaders(Symbol* signature, Klass* klass_being_linked,
                                         Handle loader1, Handle loader2, bool is_method);

  // JSR 292
  // find a java.lang.invoke.MethodHandle.invoke* method for a given signature
  // (asks Java to compute it if necessary, except in a compiler thread)
  static Method* find_method_handle_invoker(Klass* klass,
                                            Symbol* name,
                                            Symbol* signature,
                                            Klass* accessing_klass,
                                            Handle *appendix_result,
                                            TRAPS);
  // for a given signature, find the internal MethodHandle method (linkTo* or invokeBasic)
  // (does not ask Java, since this is a low-level intrinsic defined by the JVM)
  static Method* find_method_handle_intrinsic(vmIntrinsicID iid,
                                              Symbol* signature,
                                              TRAPS);

  // compute java_mirror (java.lang.Class instance) for a type ("I", "[[B", "LFoo;", etc.)
  // Either the accessing_klass or the CL/PD can be non-null, but not both.
  static Handle    find_java_mirror_for_type(Symbol* signature,
                                             Klass* accessing_klass,
                                             Handle class_loader,
                                             Handle protection_domain,
                                             SignatureStream::FailureMode failure_mode,
                                             TRAPS);
  static Handle    find_java_mirror_for_type(Symbol* signature,
                                             Klass* accessing_klass,
                                             SignatureStream::FailureMode failure_mode,
                                             TRAPS) {
    // callee will fill in CL/PD from AK, if they are needed
    return find_java_mirror_for_type(signature, accessing_klass, Handle(), Handle(),
                                     failure_mode, THREAD);
  }

  // find a java.lang.invoke.MethodType object for a given signature
  // (asks Java to compute it if necessary, except in a compiler thread)
  static Handle    find_method_handle_type(Symbol* signature,
                                           Klass* accessing_klass,
                                           TRAPS);

  // find a java.lang.Class object for a given signature
  static Handle    find_field_handle_type(Symbol* signature,
                                          Klass* accessing_klass,
                                          TRAPS);

  // ask Java to compute a java.lang.invoke.MethodHandle object for a given CP entry
  static Handle    link_method_handle_constant(Klass* caller,
                                               int ref_kind, //e.g., JVM_REF_invokeVirtual
                                               Klass* callee,
                                               Symbol* name,
                                               Symbol* signature,
                                               TRAPS);

  // ask Java to compute a constant by invoking a BSM given a Dynamic_info CP entry
  static void      invoke_bootstrap_method(BootstrapInfo& bootstrap_specifier, TRAPS);

  // Record the error when the first attempt to resolve a reference from a constant
  // pool entry to a class fails.
  static void add_resolution_error(const constantPoolHandle& pool, int which, Symbol* error,
                                   Symbol* message, Symbol* cause = nullptr, Symbol* cause_msg = nullptr);
  static void delete_resolution_error(ConstantPool* pool);
  static Symbol* find_resolution_error(const constantPoolHandle& pool, int which,
                                       Symbol** message, Symbol** cause, Symbol** cause_msg);


  // Record a nest host resolution/validation error
  static void add_nest_host_error(const constantPoolHandle& pool, int which,
                                  const char* message);
  static const char* find_nest_host_error(const constantPoolHandle& pool, int which);

protected:
  static InstanceKlass* _well_known_klasses[];

private:
  // table of box klasses (int_klass, etc.)
  static InstanceKlass* _box_klasses[T_VOID+1];

  static OopHandle  _java_system_loader;
  static OopHandle  _java_platform_loader;

private:
  // Basic loading operations
  static InstanceKlass* resolve_instance_class_or_null(Symbol* class_name,
                                                       Handle class_loader,
                                                       Handle protection_domain, TRAPS);
  static Klass* resolve_array_class_or_null(Symbol* class_name,
                                            Handle class_loader,
                                            Handle protection_domain, TRAPS);
  static void define_instance_class(InstanceKlass* k, Handle class_loader, TRAPS);
  static InstanceKlass* find_or_define_helper(Symbol* class_name,
                                              Handle class_loader,
                                              InstanceKlass* k, TRAPS);
  static InstanceKlass* load_instance_class_impl(Symbol* class_name, Handle class_loader, TRAPS);
  static InstanceKlass* load_instance_class(Symbol* class_name,
                                            Handle class_loader, TRAPS);

  // Class loader constraints
  static void check_constraints(InstanceKlass* k, ClassLoaderData* loader,
                                bool defining, TRAPS);
  static void update_dictionary(JavaThread* current, InstanceKlass* k, ClassLoaderData* loader_data);

  static bool is_shared_class_visible(Symbol* class_name, InstanceKlass* ik,
                                      PackageEntry* pkg_entry,
                                      Handle class_loader);
  static bool is_shared_class_visible_impl(Symbol* class_name,
                                           InstanceKlass* ik,
                                           PackageEntry* pkg_entry,
                                           Handle class_loader);
  static bool check_shared_class_super_type(InstanceKlass* klass, InstanceKlass* super,
                                            Handle class_loader,  Handle protection_domain,
                                            bool is_superclass, TRAPS);
  static bool check_shared_class_super_types(InstanceKlass* ik, Handle class_loader,
                                               Handle protection_domain, TRAPS);
  // Second part of load_shared_class
  static void load_shared_class_misc(InstanceKlass* ik, ClassLoaderData* loader_data) NOT_CDS_RETURN;

protected:
  // Used by SystemDictionaryShared

  static bool add_loader_constraint(Symbol* name, Klass* klass_being_linked,  Handle loader1,
                                    Handle loader2);
  static void post_class_load_event(EventClassLoad* event, const InstanceKlass* k, const ClassLoaderData* init_cld);
  static InstanceKlass* load_shared_lambda_proxy_class(InstanceKlass* ik,
                                                       Handle class_loader,
                                                       Handle protection_domain,
                                                       PackageEntry* pkg_entry,
                                                       TRAPS);
  static InstanceKlass* load_shared_class(InstanceKlass* ik,
                                          Handle class_loader,
                                          Handle protection_domain,
                                          const ClassFileStream *cfs,
                                          PackageEntry* pkg_entry,
                                          TRAPS);
  static Handle get_loader_lock_or_null(Handle class_loader);
  static InstanceKlass* find_or_define_instance_class(Symbol* class_name,
                                                      Handle class_loader,
                                                      InstanceKlass* k, TRAPS);
public:
  static bool is_system_class_loader(oop class_loader);
  static bool is_platform_class_loader(oop class_loader);
  static bool is_boot_class_loader(oop class_loader) { return class_loader == nullptr; }
  static bool is_builtin_class_loader(oop class_loader) {
    return is_boot_class_loader(class_loader)      ||
           is_platform_class_loader(class_loader)  ||
           is_system_class_loader(class_loader);
  }
  // Returns TRUE if the method is a non-public member of class java.lang.Object.
  static bool is_nonpublic_Object_method(Method* m);

  // Return Symbol or throw exception if name given is can not be a valid Symbol.
  static Symbol* class_name_symbol(const char* name, Symbol* exception, TRAPS);
};
```
