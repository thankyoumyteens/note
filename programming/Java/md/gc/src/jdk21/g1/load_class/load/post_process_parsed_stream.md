# 后续处理

```cpp
// --- src/hotspot/share/classfile/classFileParser.cpp --- //

void ClassFileParser::post_process_parsed_stream(const ClassFileStream* const stream,
                                                 ConstantPool* cp,
                                                 TRAPS) {
  assert(stream != nullptr, "invariant");
  assert(stream->at_eos(), "invariant");
  assert(cp != nullptr, "invariant");
  assert(_loader_data != nullptr, "invariant");

  if (_class_name == vmSymbols::java_lang_Object()) {
    check_property(_local_interfaces == Universe::the_empty_instance_klass_array(),
                   "java.lang.Object cannot implement an interface in class file %s",
                   CHECK);
  }
  // We check super class after class file is parsed and format is checked
  if (_super_class_index > 0 && nullptr == _super_klass) {
    Symbol* const super_class_name = cp->klass_name_at(_super_class_index);
    if (_access_flags.is_interface()) {
      // Before attempting to resolve the superclass, check for class format
      // errors not checked yet.
      guarantee_property(super_class_name == vmSymbols::java_lang_Object(),
        "Interfaces must have java.lang.Object as superclass in class file %s",
        CHECK);
    }
    Handle loader(THREAD, _loader_data->class_loader());
    if (loader.is_null() && super_class_name == vmSymbols::java_lang_Object()) {
      _super_klass = vmClasses::Object_klass();
    } else {
      _super_klass = (const InstanceKlass*)
                       SystemDictionary::resolve_super_or_fail(_class_name,
                                                               super_class_name,
                                                               loader,
                                                               _protection_domain,
                                                               true,
                                                               CHECK);
    }
  }

  if (_super_klass != nullptr) {
    if (_super_klass->has_nonstatic_concrete_methods()) {
      _has_nonstatic_concrete_methods = true;
    }

    if (_super_klass->is_interface()) {
      classfile_icce_error("class %s has interface %s as super class", _super_klass, THREAD);
      return;
    }
  }

  // Compute the transitive list of all unique interfaces implemented by this class
  _transitive_interfaces =
    compute_transitive_interfaces(_super_klass,
                                  _local_interfaces,
                                  _loader_data,
                                  CHECK);

  assert(_transitive_interfaces != nullptr, "invariant");

  // sort methods
  _method_ordering = sort_methods(_methods);

  _all_mirandas = new GrowableArray<Method*>(20);

  Handle loader(THREAD, _loader_data->class_loader());

  // 通过klassVtable、klassltable 模块提供的算法, 
  // 根据已解析的父类、方法、接口等信息计算得到Java vtable 和itable 大小
  klassVtable::compute_vtable_size_and_num_mirandas(&_vtable_size,
                                                    &_num_miranda_methods,
                                                    _all_mirandas,
                                                    _super_klass,
                                                    _methods,
                                                    _access_flags,
                                                    _major_version,
                                                    loader,
                                                    _class_name,
                                                    _local_interfaces);
  // Size of Java itable (in words)
  _itable_size = _access_flags.is_interface() ? 0 :
    klassItable::compute_itable_size(_transitive_interfaces);

  assert(_fac != nullptr, "invariant");
  assert(_parsed_annotations != nullptr, "invariant");

  _field_info = new FieldLayoutInfo();
  FieldLayoutBuilder lb(class_name(), super_klass(), _cp, /*_fields*/ _temp_field_info,
                        _parsed_annotations->is_contended(), _field_info);
  lb.build_layout();

  int injected_fields_count = _temp_field_info->length() - _java_fields_count;
  _fieldinfo_stream =
    FieldInfoStream::create_FieldInfoStream(_temp_field_info, _java_fields_count,
                                            injected_fields_count, loader_data(), CHECK);
  _fields_status =
    MetadataFactory::new_array<FieldStatus>(_loader_data, _temp_field_info->length(),
                                            FieldStatus(0), CHECK);
}
```
