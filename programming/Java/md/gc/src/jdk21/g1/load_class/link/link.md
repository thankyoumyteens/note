# 链接

不同的 class 文件之间通过符号引用建立了联系。在程序运行初期，类加载器将用到的各个类或接口加载进来，然后通过动态链接将它们联接在一起。这样，当程序运行时，便可以实现类型的相互引用和方法调用。

符号引用是以字符串的形式存在的。在每个 class 文件中，都有一个常量池，用来存放该类中用到的符号引用。当完成加载以后，来自于 class 文件的常量池会在 JVM 内部关联上一个位于运行时内存中的常量池数据结构，即运行时常量池。

如果仅仅是符号，那么引用将失去实际意义。只有当符号引用被转换成直接引用，才能帮助运行时准确定位内存实体。符号引用转换成直接引用的过程，称为解析。因为符号引用来自于常量池，所以这个过程也被称为常量池解析。

解析是链接的核心环节。

JVM 规范并没有强制规定解析过程发生的时间点。HotSpot 会在符号引用首次被访问时才去解析(晚解析)。虽然是晚解析，但 HotSpot 对延迟也有一个最低容忍限度。至少类型在初始化前，应确保已链接。若此时尚未链接，则需要进行链接。

```cpp
// --- src/hotspot/share/oops/instanceKlass.cpp --- //

bool InstanceKlass::link_class_impl(TRAPS) {
  if (DumpSharedSpaces && SystemDictionaryShared::has_class_failed_verification(this)) {
    // This is for CDS dumping phase only -- we use the in_error_state to indicate that
    // the class has failed verification. Throwing the NoClassDefFoundError here is just
    // a convenient way to stop repeat attempts to verify the same (bad) class.
    //
    // Note that the NoClassDefFoundError is not part of the JLS, and should not be thrown
    // if we are executing Java code. This is not a problem for CDS dumping phase since
    // it doesn't execute any Java code.
    ResourceMark rm(THREAD);
    Exceptions::fthrow(THREAD_AND_LOCATION,
                       vmSymbols::java_lang_NoClassDefFoundError(),
                       "Class %s, or one of its supertypes, failed class initialization",
                       external_name());
    return false;
  }
  // return if already verified
  if (is_linked()) {
    return true;
  }

  // Timing
  // timer handles recursion
  JavaThread* jt = THREAD;

  // link super class before linking this class
  Klass* super_klass = super();
  if (super_klass != nullptr) {
    if (super_klass->is_interface()) {  // check if super class is an interface
      ResourceMark rm(THREAD);
      Exceptions::fthrow(
        THREAD_AND_LOCATION,
        vmSymbols::java_lang_IncompatibleClassChangeError(),
        "class %s has interface %s as super class",
        external_name(),
        super_klass->external_name()
      );
      return false;
    }

    InstanceKlass* ik_super = InstanceKlass::cast(super_klass);
    ik_super->link_class_impl(CHECK_false);
  }

  // link all interfaces implemented by this class before linking this class
  Array<InstanceKlass*>* interfaces = local_interfaces();
  int num_interfaces = interfaces->length();
  for (int index = 0; index < num_interfaces; index++) {
    InstanceKlass* interk = interfaces->at(index);
    interk->link_class_impl(CHECK_false);
  }

  // in case the class is linked in the process of linking its superclasses
  if (is_linked()) {
    return true;
  }

  // trace only the link time for this klass that includes
  // the verification time
  PerfClassTraceTime vmtimer(ClassLoader::perf_class_link_time(),
                             ClassLoader::perf_class_link_selftime(),
                             ClassLoader::perf_classes_linked(),
                             jt->get_thread_stat()->perf_recursion_counts_addr(),
                             jt->get_thread_stat()->perf_timers_addr(),
                             PerfClassTraceTime::CLASS_LINK);

  // verification & rewriting
  {
    LockLinkState init_lock(this, jt);

    // rewritten will have been set if loader constraint error found
    // on an earlier link attempt
    // don't verify or rewrite if already rewritten
    //

    if (!is_linked()) {
      if (!is_rewritten()) {
        if (is_shared()) {
          assert(!verified_at_dump_time(), "must be");
        }
        {
          bool verify_ok = verify_code(THREAD);
          if (!verify_ok) {
            return false;
          }
        }

        // Just in case a side-effect of verify linked this class already
        // (which can sometimes happen since the verifier loads classes
        // using custom class loaders, which are free to initialize things)
        if (is_linked()) {
          return true;
        }

        // also sets rewritten
        rewrite_class(CHECK_false);
      } else if (is_shared()) {
        SystemDictionaryShared::check_verification_constraints(this, CHECK_false);
      }

      // relocate jsrs and link methods after they are all rewritten
      link_methods(CHECK_false);

      // Initialize the vtable and interface table after
      // methods have been rewritten since rewrite may
      // fabricate new Method*s.
      // also does loader constraint checking
      //
      // initialize_vtable and initialize_itable need to be rerun
      // for a shared class if
      // 1) the class is loaded by custom class loader or
      // 2) the class is loaded by built-in class loader but failed to add archived loader constraints or
      // 3) the class was not verified during dump time
      bool need_init_table = true;
      if (is_shared() && verified_at_dump_time() &&
          SystemDictionaryShared::check_linking_constraints(THREAD, this)) {
        need_init_table = false;
      }
      if (need_init_table) {
        vtable().initialize_vtable_and_check_constraints(CHECK_false);
        itable().initialize_itable_and_check_constraints(CHECK_false);
      }
#ifdef ASSERT
      vtable().verify(tty, true);
      // In case itable verification is ever added.
      // itable().verify(tty, true);
#endif
      set_initialization_state_and_notify(linked, THREAD);
      if (JvmtiExport::should_post_class_prepare()) {
        JvmtiExport::post_class_prepare(THREAD, this);
      }
    }
  }
  return true;
}
```
