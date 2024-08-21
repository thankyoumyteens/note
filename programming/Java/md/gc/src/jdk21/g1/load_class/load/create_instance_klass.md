# 创建 instanceKlass

```cpp
// --- src/hotspot/share/classfile/classFileParser.cpp --- //

InstanceKlass* ClassFileParser::create_instance_klass(bool changed_by_loadhook,
                                                      const ClassInstanceInfo& cl_inst_info,
                                                      TRAPS) {
  if (_klass != nullptr) {
    return _klass;
  }

  InstanceKlass* const ik =
    InstanceKlass::allocate_instance_klass(*this, CHECK_NULL);

  if (is_hidden()) {
    mangle_hidden_class_name(ik);
  }

  fill_instance_klass(ik, changed_by_loadhook, cl_inst_info, CHECK_NULL);

  assert(_klass == ik, "invariant");

  return ik;
}

void ClassFileParser::fill_instance_klass(InstanceKlass* ik,
                                          bool changed_by_loadhook,
                                          const ClassInstanceInfo& cl_inst_info,
                                          TRAPS) {
  assert(ik != nullptr, "invariant");

  // Set name and CLD before adding to CLD
  ik->set_class_loader_data(_loader_data);
  ik->set_name(_class_name);

  // Add all classes to our internal class loader list here,
  // including classes in the bootstrap (null) class loader.
  const bool publicize = !is_internal();

  _loader_data->add_class(ik, publicize);

  set_klass_to_deallocate(ik);

  assert(_field_info != nullptr, "invariant");
  assert(ik->static_field_size() == _field_info->_static_field_size, "sanity");
  assert(ik->nonstatic_oop_map_count() == _field_info->oop_map_blocks->_nonstatic_oop_map_count,
         "sanity");

  assert(ik->is_instance_klass(), "sanity");
  assert(ik->size_helper() == _field_info->_instance_size, "sanity");

  // Fill in information already parsed
  ik->set_should_verify_class(_need_verify);

  // Not yet: supers are done below to support the new subtype-checking fields
  ik->set_nonstatic_field_size(_field_info->_nonstatic_field_size);
  ik->set_has_nonstatic_fields(_field_info->_has_nonstatic_fields);
  assert(_fac != nullptr, "invariant");
  ik->set_static_oop_field_count(_fac->count[STATIC_OOP]);

  // this transfers ownership of a lot of arrays from
  // the parser onto the InstanceKlass*
  apply_parsed_class_metadata(ik, _java_fields_count);

  // can only set dynamic nest-host after static nest information is set
  if (cl_inst_info.dynamic_nest_host() != nullptr) {
    ik->set_nest_host(cl_inst_info.dynamic_nest_host());
  }

  // note that is not safe to use the fields in the parser from this point on
  assert(nullptr == _cp, "invariant");
  assert(nullptr == _fieldinfo_stream, "invariant");
  assert(nullptr == _fields_status, "invariant");
  assert(nullptr == _methods, "invariant");
  assert(nullptr == _inner_classes, "invariant");
  assert(nullptr == _nest_members, "invariant");
  assert(nullptr == _combined_annotations, "invariant");
  assert(nullptr == _record_components, "invariant");
  assert(nullptr == _permitted_subclasses, "invariant");

  if (_has_localvariable_table) {
    ik->set_has_localvariable_table(true);
  }

  if (_has_final_method) {
    ik->set_has_final_method();
  }

  ik->copy_method_ordering(_method_ordering, CHECK);
  // The InstanceKlass::_methods_jmethod_ids cache
  // is managed on the assumption that the initial cache
  // size is equal to the number of methods in the class. If
  // that changes, then InstanceKlass::idnum_can_increment()
  // has to be changed accordingly.
  ik->set_initial_method_idnum(ik->methods()->length());

  ik->set_this_class_index(_this_class_index);

  if (_is_hidden) {
    // _this_class_index is a CONSTANT_Class entry that refers to this
    // hidden class itself. If this class needs to refer to its own methods
    // or fields, it would use a CONSTANT_MethodRef, etc, which would reference
    // _this_class_index. However, because this class is hidden (it's
    // not stored in SystemDictionary), _this_class_index cannot be resolved
    // with ConstantPool::klass_at_impl, which does a SystemDictionary lookup.
    // Therefore, we must eagerly resolve _this_class_index now.
    ik->constants()->klass_at_put(_this_class_index, ik);
  }

  ik->set_minor_version(_minor_version);
  ik->set_major_version(_major_version);
  ik->set_has_nonstatic_concrete_methods(_has_nonstatic_concrete_methods);
  ik->set_declares_nonstatic_concrete_methods(_declares_nonstatic_concrete_methods);

  if (_is_hidden) {
    ik->set_is_hidden();
  }

  // Set PackageEntry for this_klass
  oop cl = ik->class_loader();
  Handle clh = Handle(THREAD, java_lang_ClassLoader::non_reflection_class_loader(cl));
  ClassLoaderData* cld = ClassLoaderData::class_loader_data_or_null(clh());
  ik->set_package(cld, nullptr, CHECK);

  const Array<Method*>* const methods = ik->methods();
  assert(methods != nullptr, "invariant");
  const int methods_len = methods->length();

  check_methods_for_intrinsics(ik, methods);

  // Fill in field values obtained by parse_classfile_attributes
  if (_parsed_annotations->has_any_annotations()) {
    _parsed_annotations->apply_to(ik);
  }

  apply_parsed_class_attributes(ik);

  // Miranda methods
  if ((_num_miranda_methods > 0) ||
      // if this class introduced new miranda methods or
      (_super_klass != nullptr && _super_klass->has_miranda_methods())
        // super class exists and this class inherited miranda methods
     ) {
       ik->set_has_miranda_methods(); // then set a flag
  }

  // Fill in information needed to compute superclasses.
  ik->initialize_supers(const_cast<InstanceKlass*>(_super_klass), _transitive_interfaces, CHECK);
  ik->set_transitive_interfaces(_transitive_interfaces);
  ik->set_local_interfaces(_local_interfaces);
  _transitive_interfaces = nullptr;
  _local_interfaces = nullptr;

  // Initialize itable offset tables
  klassItable::setup_itable_offset_table(ik);

  // Compute transitive closure of interfaces this class implements
  // Do final class setup
  OopMapBlocksBuilder* oop_map_blocks = _field_info->oop_map_blocks;
  if (oop_map_blocks->_nonstatic_oop_map_count > 0) {
    oop_map_blocks->copy(ik->start_of_nonstatic_oop_maps());
  }

  if (_has_contended_fields || _parsed_annotations->is_contended() ||
      ( _super_klass != nullptr && _super_klass->has_contended_annotations())) {
    ik->set_has_contended_annotations(true);
  }

  // Fill in has_finalizer, has_vanilla_constructor, and layout_helper
  set_precomputed_flags(ik);

  // check if this class can access its super class
  check_super_class_access(ik, CHECK);

  // check if this class can access its superinterfaces
  check_super_interface_access(ik, CHECK);

  // check if this class overrides any final method
  check_final_method_override(ik, CHECK);

  // reject static interface methods prior to Java 8
  if (ik->is_interface() && _major_version < JAVA_8_VERSION) {
    check_illegal_static_method(ik, CHECK);
  }

  // Obtain this_klass' module entry
  ModuleEntry* module_entry = ik->module();
  assert(module_entry != nullptr, "module_entry should always be set");

  // Obtain java.lang.Module
  Handle module_handle(THREAD, module_entry->module());

  // Allocate mirror and initialize static fields
  // The create_mirror() call will also call compute_modifiers()
  // 创建Java镜像类并初始化静态字段
  java_lang_Class::create_mirror(ik,
                                 Handle(THREAD, _loader_data->class_loader()),
                                 module_handle,
                                 _protection_domain,
                                 cl_inst_info.class_data(),
                                 CHECK);

  assert(_all_mirandas != nullptr, "invariant");

  // Generate any default methods - default methods are public interface methods
  // that have a default implementation.  This is new with Java 8.
  if (_has_nonstatic_concrete_methods) {
    DefaultMethods::generate_default_methods(ik,
                                             _all_mirandas,
                                             CHECK);
  }

  // Add read edges to the unnamed modules of the bootstrap and app class loaders.
  if (changed_by_loadhook && !module_handle.is_null() && module_entry->is_named() &&
      !module_entry->has_default_read_edges()) {
    if (!module_entry->set_has_default_read_edges()) {
      // We won a potential race
      JvmtiExport::add_default_read_edges(module_handle, THREAD);
    }
  }
  // 通知类已加载, 更新 Perf Data 计数器
  ClassLoadingService::notify_class_loaded(ik, false /* not shared class */);

  if (!is_internal()) {
    ik->print_class_load_logging(_loader_data, module_entry, _stream);

    if (ik->minor_version() == JAVA_PREVIEW_MINOR_VERSION &&
        ik->major_version() == JVM_CLASSFILE_MAJOR_VERSION &&
        log_is_enabled(Info, class, preview)) {
      ResourceMark rm;
      log_info(class, preview)("Loading class %s that depends on preview features (class file version %d.65535)",
                               ik->external_name(), JVM_CLASSFILE_MAJOR_VERSION);
    }

    if (log_is_enabled(Debug, class, resolve))  {
      ResourceMark rm;
      // print out the superclass.
      const char * from = ik->external_name();
      if (ik->java_super() != nullptr) {
        log_debug(class, resolve)("%s %s (super)",
                   from,
                   ik->java_super()->external_name());
      }
      // print out each of the interface classes referred to by this class.
      const Array<InstanceKlass*>* const local_interfaces = ik->local_interfaces();
      if (local_interfaces != nullptr) {
        const int length = local_interfaces->length();
        for (int i = 0; i < length; i++) {
          const InstanceKlass* const k = local_interfaces->at(i);
          const char * to = k->external_name();
          log_debug(class, resolve)("%s %s (interface)", from, to);
        }
      }
    }
  }

  JFR_ONLY(INIT_ID(ik);)

  // If we reach here, all is well.
  // Now remove the InstanceKlass* from the _klass_to_deallocate field
  // in order for it to not be destroyed in the ClassFileParser destructor.
  set_klass_to_deallocate(nullptr);

  // it's official
  set_klass(ik);

  debug_only(ik->verify();)
}
```
