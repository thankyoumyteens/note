# 链接解析器

在虚拟机中，通过链接解析器(LinkResolver)对方法进行解析和查找，链接解析器能够对不同类型的方法执行解析任务

## 参数

```cpp
// --- src/hotspot/share/interpreter/linkResolver.hpp --- //

class LinkInfo : public StackObj {
  // 方法名
  Symbol*     _name;            // extracted from JVM_CONSTANT_NameAndType
  // 方法签名
  Symbol*     _signature;
  // 待解析方法所在的类
  // 在执行方法解析的时候，所在类应当是已解析的，故称为resolved_klass
  Klass*      _resolved_klass;  // class that the constant pool entry points to
  // 常量池所在的类
  Klass*      _current_klass;   // class that owns the constant pool
  methodHandle _current_method;  // sending method
  // 是否执行可访问性检查
  bool        _check_access;
  bool        _check_loader_constraints;
  constantTag _tag;
};
```

## 解析类方法

1. 首先检查 resolved_klass 类型是否正确。如果 resolved_klass 是接口类型, 则抛出 java.lang.IncompatibleClassChangeError
2. 在 resolved_klass 以及它的超类中査找方法。若未找到，则转向步骤 3。instanceKlass 中封装了这个查找算法，instanceKlass 中的成员 `_methods` 表该类拥有的方法表，它是已排序的，这样在做方法查找时，就可以应用高效的二分查找算法。找到目标方法后把 `Method*` 包装成 methodHandle 句柄
3. 在 resolved_klass 实现的所有接口中査找，若已找到，则进入步骤 5, 进行一些必要的检查。如果仍然没有找到，则进入步骤 4
4. 抛出 java.lang.NoSuchMethodError
5. 检查方法是否是具体的，若该方法所在类是非抽象的但该方法是抽象的，则抛出 java.lang.AbstractMethodError
6. 接下来是访问权限检查，包括检查调用类是否具有对该方法的访问权限，以及通过调用 SystemDictionary::check_signature_loaders，检查当前类和已解析类的加载器以及该方法的签名等信息，以检验是否违反类加载器约束，若违反约束，则抛出 java.lang.LinkageError

```cpp
// --- src/hotspot/share/interpreter/linkResolver.cpp --- //

Method* LinkResolver::resolve_method(const LinkInfo& link_info,
                                     Bytecodes::Code code, TRAPS) {

  Handle nested_exception;
  Klass* resolved_klass = link_info.resolved_klass();

  // 1. For invokevirtual, cannot call an interface method
  if (code == Bytecodes::_invokevirtual && resolved_klass->is_interface()) {
    ResourceMark rm(THREAD);
    char buf[200];
    jio_snprintf(buf, sizeof(buf), "Found interface %s, but class was expected",
        resolved_klass->external_name());
    THROW_MSG_NULL(vmSymbols::java_lang_IncompatibleClassChangeError(), buf);
  }

  // 2. check constant pool tag for called method - must be JVM_CONSTANT_Methodref
  if (!link_info.tag().is_invalid() && !link_info.tag().is_method()) {
    ResourceMark rm(THREAD);
    stringStream ss;
    ss.print("Method '");
    Method::print_external_name(&ss, link_info.resolved_klass(), link_info.name(), link_info.signature());
    ss.print("' must be Methodref constant");
    THROW_MSG_NULL(vmSymbols::java_lang_IncompatibleClassChangeError(), ss.as_string());
  }

  // 3. lookup method in resolved klass and its super klasses
  // 待解析的方法，是一个methodHandle类型引用
  // 若解析成功，则赋予正确的方法句柄
  methodHandle resolved_method(THREAD, lookup_method_in_klasses(link_info, true, false));

  // 4. lookup method in all the interfaces implemented by the resolved klass
  if (resolved_method.is_null() && !resolved_klass->is_array_klass()) { // not found in the class hierarchy
    resolved_method = methodHandle(THREAD, lookup_method_in_interfaces(link_info));

    if (resolved_method.is_null()) {
      // JSR 292:  see if this is an implicitly generated method MethodHandle.linkToVirtual(*...), etc
      Method* method = lookup_polymorphic_method(link_info, (Handle*)nullptr, THREAD);
      resolved_method = methodHandle(THREAD, method);
      if (HAS_PENDING_EXCEPTION) {
        nested_exception = Handle(THREAD, PENDING_EXCEPTION);
        CLEAR_PENDING_EXCEPTION;
      }
    }
  }

  // 5. method lookup failed
  if (resolved_method.is_null()) {
    ResourceMark rm(THREAD);
    stringStream ss;
    ss.print("'");
    Method::print_external_name(&ss, resolved_klass, link_info.name(), link_info.signature());
    ss.print("'");
    THROW_MSG_CAUSE_(vmSymbols::java_lang_NoSuchMethodError(),
                     ss.as_string(), nested_exception, nullptr);
  }

  // 6. access checks, access checking may be turned off when calling from within the VM.
  Klass* current_klass = link_info.current_klass();
  if (link_info.check_access()) {
    assert(current_klass != nullptr , "current_klass should not be null");

    // check if method can be accessed by the referring class
    check_method_accessability(current_klass,
                               resolved_klass,
                               resolved_method->method_holder(),
                               resolved_method,
                               CHECK_NULL);
  }
  if (link_info.check_loader_constraints()) {
    // check loader constraints
    check_method_loader_constraints(link_info, resolved_method, "method", CHECK_NULL);
  }
  // Handle使用运算符重载实现, 通过()直接获取handle中封装的oop
  return resolved_method();
}
```

## 解析接口方法

```cpp
// --- src/hotspot/share/interpreter/linkResolver.cpp --- //

// Do linktime resolution of a method in the interface within the context of the specified bytecode.
Method* LinkResolver::resolve_interface_method(const LinkInfo& link_info, Bytecodes::Code code, TRAPS) {

  Klass* resolved_klass = link_info.resolved_klass();

  // check if klass is interface
  if (!resolved_klass->is_interface()) {
    ResourceMark rm(THREAD);
    char buf[200];
    jio_snprintf(buf, sizeof(buf), "Found class %s, but interface was expected", resolved_klass->external_name());
    THROW_MSG_NULL(vmSymbols::java_lang_IncompatibleClassChangeError(), buf);
  }

  // check constant pool tag for called method - must be JVM_CONSTANT_InterfaceMethodref
  if (!link_info.tag().is_invalid() && !link_info.tag().is_interface_method()) {
    ResourceMark rm(THREAD);
    stringStream ss;
    ss.print("Method '");
    Method::print_external_name(&ss, link_info.resolved_klass(), link_info.name(), link_info.signature());
    ss.print("' must be InterfaceMethodref constant");
    THROW_MSG_NULL(vmSymbols::java_lang_IncompatibleClassChangeError(), ss.as_string());
  }

  // lookup method in this interface or its super, java.lang.Object
  // JDK8: also look for static methods
  methodHandle resolved_method(THREAD, lookup_method_in_klasses(link_info, false, true));

  if (resolved_method.is_null() && !resolved_klass->is_array_klass()) {
    // lookup method in all the super-interfaces
    resolved_method = methodHandle(THREAD, lookup_method_in_interfaces(link_info));
  }

  if (resolved_method.is_null()) {
    // no method found
    ResourceMark rm(THREAD);
    stringStream ss;
    ss.print("'");
    Method::print_external_name(&ss, resolved_klass, link_info.name(), link_info.signature());
    ss.print("'");
    THROW_MSG_NULL(vmSymbols::java_lang_NoSuchMethodError(), ss.as_string());
  }

  if (link_info.check_access()) {
    // JDK8 adds non-public interface methods, and accessability check requirement
    Klass* current_klass = link_info.current_klass();

    assert(current_klass != nullptr , "current_klass should not be null");

    // check if method can be accessed by the referring class
    check_method_accessability(current_klass,
                               resolved_klass,
                               resolved_method->method_holder(),
                               resolved_method,
                               CHECK_NULL);
  }
  if (link_info.check_loader_constraints()) {
    check_method_loader_constraints(link_info, resolved_method, "interface method", CHECK_NULL);
  }

  if (code != Bytecodes::_invokestatic && resolved_method->is_static()) {
    ResourceMark rm(THREAD);
    stringStream ss;
    ss.print("Expected instance not static method '");
    Method::print_external_name(&ss, resolved_klass,
                                resolved_method->name(), resolved_method->signature());
    ss.print("'");
    THROW_MSG_NULL(vmSymbols::java_lang_IncompatibleClassChangeError(), ss.as_string());
  }

  if (log_develop_is_enabled(Trace, itables)) {
    char buf[200];
    jio_snprintf(buf, sizeof(buf), "%s resolved interface method: caller-class:",
                 Bytecodes::name(code));
    trace_method_resolution(buf, link_info.current_klass(), resolved_klass, resolved_method(), true);
  }

  return resolved_method();
}
```
