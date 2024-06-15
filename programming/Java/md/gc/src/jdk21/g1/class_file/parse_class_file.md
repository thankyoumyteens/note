# 解析字节码文件

```cpp
// --- src/hotspot/share/classfile/klassFactory.cpp --- //

InstanceKlass* KlassFactory::create_from_stream(ClassFileStream* stream,
                                                Symbol* name,
                                                ClassLoaderData* loader_data,
                                                const ClassLoadInfo& cl_info,
                                                TRAPS) {

  assert(stream != nullptr, "invariant");
  assert(loader_data != nullptr, "invariant");

  ResourceMark rm(THREAD);
  HandleMark hm(THREAD);

  JvmtiCachedClassFileData* cached_class_file = nullptr;

  ClassFileStream* old_stream = stream;

  // 统计已经加载了多少Java类
  THREAD->statistical_info().incr_define_class_count();

  // Skip this processing for VM hidden classes
  if (!cl_info.is_hidden()) {
    stream = check_class_file_load_hook(stream,
                                        name,
                                        loader_data,
                                        cl_info.protection_domain(),
                                        &cached_class_file,
                                        CHECK_NULL);
  }

  ClassFileParser parser(stream,
                         name,
                         loader_data,
                         &cl_info,
                         ClassFileParser::BROADCAST, // publicity level
                         CHECK_NULL);

  const ClassInstanceInfo* cl_inst_info = cl_info.class_hidden_info_ptr();
  InstanceKlass* result = parser.create_instance_klass(old_stream != stream, *cl_inst_info, CHECK_NULL);
  assert(result != nullptr, "result cannot be null with no pending exception");

  if (cached_class_file != nullptr) {
    // JVMTI: we have an InstanceKlass now, tell it about the cached bytes
    result->set_cached_class_file(cached_class_file);
  }

  JFR_ONLY(ON_KLASS_CREATION(result, parser, THREAD);)

#if INCLUDE_CDS
  if (Arguments::is_dumping_archive()) {
    ClassLoader::record_result(THREAD, result, stream, old_stream != stream);
  }
#endif // INCLUDE_CDS

  return result;
}

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

void ClassFileParser::parse_stream(const ClassFileStream* const stream,
                                   TRAPS) {

  assert(stream != nullptr, "invariant");
  assert(_class_name != nullptr, "invariant");

  // BEGIN STREAM PARSING
  // 确保文件至少包含8个字节
  stream->guarantee_more(8, CHECK);  // magic, major, minor
  // Magic value
  const u4 magic = stream->get_u4_fast();
  guarantee_property(magic == JAVA_CLASSFILE_MAGIC,
                     "Incompatible magic value %u in class file %s",
                     magic, CHECK);

  // Version numbers
  _minor_version = stream->get_u2_fast();
  _major_version = stream->get_u2_fast();

  // Check version numbers - we check this even with verifier off
  verify_class_version(_major_version, _minor_version, _class_name, CHECK);

  stream->guarantee_more(3, CHECK); // length, first cp tag
  u2 cp_size = stream->get_u2_fast();

  guarantee_property(
    cp_size >= 1, "Illegal constant pool size %u in class file %s",
    cp_size, CHECK);

  _orig_cp_size = cp_size;
  if (is_hidden()) { // Add a slot for hidden class name.
    cp_size++;
  }

  _cp = ConstantPool::allocate(_loader_data,
                               cp_size,
                               CHECK);

  ConstantPool* const cp = _cp;

  parse_constant_pool(stream, cp, _orig_cp_size, CHECK);

  assert(cp_size == (const u2)cp->length(), "invariant");

  // ACCESS FLAGS
  stream->guarantee_more(8, CHECK);  // flags, this_class, super_class, infs_len

  // Access flags
  jint flags;
  // JVM_ACC_MODULE is defined in JDK-9 and later.
  if (_major_version >= JAVA_9_VERSION) {
    flags = stream->get_u2_fast() & (JVM_RECOGNIZED_CLASS_MODIFIERS | JVM_ACC_MODULE);
  } else {
    flags = stream->get_u2_fast() & JVM_RECOGNIZED_CLASS_MODIFIERS;
  }

  if ((flags & JVM_ACC_INTERFACE) && _major_version < JAVA_6_VERSION) {
    // Set abstract bit for old class files for backward compatibility
    flags |= JVM_ACC_ABSTRACT;
  }

  verify_legal_class_modifiers(flags, CHECK);

  short bad_constant = class_bad_constant_seen();
  if (bad_constant != 0) {
    // Do not throw CFE until after the access_flags are checked because if
    // ACC_MODULE is set in the access flags, then NCDFE must be thrown, not CFE.
    classfile_parse_error("Unknown constant tag %u in class file %s", bad_constant, THREAD);
    return;
  }

  _access_flags.set_flags(flags);

  // This class and superclass
  _this_class_index = stream->get_u2_fast();
  check_property(
    valid_cp_range(_this_class_index, cp_size) &&
      cp->tag_at(_this_class_index).is_unresolved_klass(),
    "Invalid this class index %u in constant pool in class file %s",
    _this_class_index, CHECK);

  Symbol* const class_name_in_cp = cp->klass_name_at(_this_class_index);
  assert(class_name_in_cp != nullptr, "class_name can't be null");

  // Don't need to check whether this class name is legal or not.
  // It has been checked when constant pool is parsed.
  // However, make sure it is not an array type.
  if (_need_verify) {
    guarantee_property(class_name_in_cp->char_at(0) != JVM_SIGNATURE_ARRAY,
                       "Bad class name in class file %s",
                       CHECK);
  }

#ifdef ASSERT
  // Basic sanity checks
  if (_is_hidden) {
    assert(_class_name != vmSymbols::unknown_class_name(), "hidden classes should have a special name");
  }
#endif

  // Update the _class_name as needed depending on whether this is a named, un-named, or hidden class.

  if (_is_hidden) {
    assert(_class_name != nullptr, "Unexpected null _class_name");
#ifdef ASSERT
    if (_need_verify) {
      verify_legal_class_name(_class_name, CHECK);
    }
#endif

  } else {
    // Check if name in class file matches given name
    if (_class_name != class_name_in_cp) {
      if (_class_name != vmSymbols::unknown_class_name()) {
        ResourceMark rm(THREAD);
        Exceptions::fthrow(THREAD_AND_LOCATION,
                           vmSymbols::java_lang_NoClassDefFoundError(),
                           "%s (wrong name: %s)",
                           _class_name->as_C_string(),
                           class_name_in_cp->as_C_string()
                           );
        return;
      } else {
        // The class name was not known by the caller so we set it from
        // the value in the CP.
        update_class_name(class_name_in_cp);
      }
      // else nothing to do: the expected class name matches what is in the CP
    }
  }

  // Verification prevents us from creating names with dots in them, this
  // asserts that that's the case.
  assert(is_internal_format(_class_name), "external class name format used internally");

  if (!is_internal()) {
    LogTarget(Debug, class, preorder) lt;
    if (lt.is_enabled()){
      ResourceMark rm(THREAD);
      LogStream ls(lt);
      ls.print("%s", _class_name->as_klass_external_name());
      if (stream->source() != nullptr) {
        ls.print(" source: %s", stream->source());
      }
      ls.cr();
    }
  }

  // SUPERKLASS
  _super_class_index = stream->get_u2_fast();
  _super_klass = parse_super_class(cp,
                                   _super_class_index,
                                   _need_verify,
                                   CHECK);

  // Interfaces
  _itfs_len = stream->get_u2_fast();
  parse_interfaces(stream,
                   _itfs_len,
                   cp,
                   &_has_nonstatic_concrete_methods,
                   CHECK);

  assert(_local_interfaces != nullptr, "invariant");

  // Fields (offsets are filled in later)
  _fac = new FieldAllocationCount();
  parse_fields(stream,
               _access_flags.is_interface(),
               _fac,
               cp,
               cp_size,
               &_java_fields_count,
               CHECK);

  assert(_temp_field_info != nullptr, "invariant");

  // Methods
  parse_methods(stream,
                _access_flags.is_interface(),
                &_has_localvariable_table,
                &_has_final_method,
                &_declares_nonstatic_concrete_methods,
                CHECK);

  assert(_methods != nullptr, "invariant");

  if (_declares_nonstatic_concrete_methods) {
    _has_nonstatic_concrete_methods = true;
  }

  // Additional attributes/annotations
  _parsed_annotations = new ClassAnnotationCollector();
  parse_classfile_attributes(stream, cp, _parsed_annotations, CHECK);

  assert(_inner_classes != nullptr, "invariant");

  // Finalize the Annotations metadata object,
  // now that all annotation arrays have been created.
  create_combined_annotations(CHECK);

  // Make sure this is the end of class file stream
  guarantee_property(stream->at_eos(),
                     "Extra bytes at the end of class file %s",
                     CHECK);

  // all bytes in stream read and parsed
}
```
