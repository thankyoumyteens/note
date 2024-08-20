# 解析 class 文件

```cpp
// --- src/hotspot/share/classfile/classFileParser.cpp --- //

ClassFileParser::ClassFileParser(ClassFileStream* stream,
                                 Symbol* name,
                                 ClassLoaderData* loader_data,
                                 const ClassLoadInfo* cl_info,
                                 Publicity pub_level,
                                 TRAPS) :
  _stream(stream),
  _class_name(nullptr),
  _loader_data(loader_data),
  _is_hidden(cl_info->is_hidden()),
  _can_access_vm_annotations(cl_info->can_access_vm_annotations()),
  _orig_cp_size(0),
  _super_klass(),
  _cp(nullptr),
  _fieldinfo_stream(nullptr),
  _fields_status(nullptr),
  _methods(nullptr),
  _inner_classes(nullptr),
  _nest_members(nullptr),
  _nest_host(0),
  _permitted_subclasses(nullptr),
  _record_components(nullptr),
  _local_interfaces(nullptr),
  _transitive_interfaces(nullptr),
  _combined_annotations(nullptr),
  _class_annotations(nullptr),
  _class_type_annotations(nullptr),
  _fields_annotations(nullptr),
  _fields_type_annotations(nullptr),
  _klass(nullptr),
  _klass_to_deallocate(nullptr),
  _parsed_annotations(nullptr),
  _fac(nullptr),
  _field_info(nullptr),
  _temp_field_info(nullptr),
  _method_ordering(nullptr),
  _all_mirandas(nullptr),
  _vtable_size(0),
  _itable_size(0),
  _num_miranda_methods(0),
  _protection_domain(cl_info->protection_domain()),
  _access_flags(),
  _pub_level(pub_level),
  _bad_constant_seen(0),
  _synthetic_flag(false),
  _sde_length(false),
  _sde_buffer(nullptr),
  _sourcefile_index(0),
  _generic_signature_index(0),
  _major_version(0),
  _minor_version(0),
  _this_class_index(0),
  _super_class_index(0),
  _itfs_len(0),
  _java_fields_count(0),
  _need_verify(false),
  _relax_verify(false),
  _has_nonstatic_concrete_methods(false),
  _declares_nonstatic_concrete_methods(false),
  _has_localvariable_table(false),
  _has_final_method(false),
  _has_contended_fields(false),
  _has_finalizer(false),
  _has_empty_finalizer(false),
  _has_vanilla_constructor(false),
  _max_bootstrap_specifier_index(-1) {

  _class_name = name != nullptr ? name : vmSymbols::unknown_class_name();
  _class_name->increment_refcount();

  assert(_loader_data != nullptr, "invariant");
  assert(stream != nullptr, "invariant");
  assert(_stream != nullptr, "invariant");
  assert(_stream->buffer() == _stream->current(), "invariant");
  assert(_class_name != nullptr, "invariant");
  assert(0 == _access_flags.as_int(), "invariant");

  // Figure out whether we can skip format checking (matching classic VM behavior)
  if (DumpSharedSpaces) {
    // verify == true means it's a 'remote' class (i.e., non-boot class)
    // Verification decision is based on BytecodeVerificationRemote flag
    // for those classes.
    _need_verify = (stream->need_verify()) ? BytecodeVerificationRemote :
                                              BytecodeVerificationLocal;
  }
  else {
    _need_verify = Verifier::should_verify_for(_loader_data->class_loader(),
                                               stream->need_verify());
  }

  // synch back verification state to stream
  stream->set_verify(_need_verify);

  // Check if verification needs to be relaxed for this class file
  // Do not restrict it to jdk1.0 or jdk1.1 to maintain backward compatibility (4982376)
  _relax_verify = relax_format_check_for(_loader_data);

  parse_stream(stream, CHECK);

  post_process_parsed_stream(stream, _cp, CHECK);
}
```
