# 解析常量池

```cpp
// --- src/hotspot/share/classfile/classFileParser.cpp --- //

void ClassFileParser::parse_constant_pool(const ClassFileStream* const stream,
                                         ConstantPool* const cp,
                                         const int length,
                                         TRAPS) {
  assert(cp != nullptr, "invariant");
  assert(stream != nullptr, "invariant");

  // parsing constant pool entries
  parse_constant_pool_entries(stream, cp, length, CHECK);
  if (class_bad_constant_seen() != 0) {
    // a bad CP entry has been detected previously so stop parsing and just return.
    return;
  }

  int index = 1;  // declared outside of loops for portability
  int num_klasses = 0;

  // first verification pass - validate cross references
  // and fixup class and string constants
  for (index = 1; index < length; index++) {          // Index 0 is unused
    const jbyte tag = cp->tag_at(index).value();
    switch (tag) {
      case JVM_CONSTANT_Class: {
        ShouldNotReachHere();     // Only JVM_CONSTANT_ClassIndex should be present
        break;
      }
      case JVM_CONSTANT_Fieldref:
        // fall through
      case JVM_CONSTANT_Methodref:
        // fall through
      case JVM_CONSTANT_InterfaceMethodref: {
        if (!_need_verify) break;
        const int klass_ref_index = cp->uncached_klass_ref_index_at(index);
        const int name_and_type_ref_index = cp->uncached_name_and_type_ref_index_at(index);
        check_property(valid_klass_reference_at(klass_ref_index),
                       "Invalid constant pool index %u in class file %s",
                       klass_ref_index, CHECK);
        check_property(valid_cp_range(name_and_type_ref_index, length) &&
          cp->tag_at(name_and_type_ref_index).is_name_and_type(),
          "Invalid constant pool index %u in class file %s",
          name_and_type_ref_index, CHECK);
        break;
      }
      case JVM_CONSTANT_String: {
        ShouldNotReachHere();     // Only JVM_CONSTANT_StringIndex should be present
        break;
      }
      case JVM_CONSTANT_Integer:
        break;
      case JVM_CONSTANT_Float:
        break;
      case JVM_CONSTANT_Long:
      case JVM_CONSTANT_Double: {
        index++;
        check_property(
          (index < length && cp->tag_at(index).is_invalid()),
          "Improper constant pool long/double index %u in class file %s",
          index, CHECK);
        break;
      }
      case JVM_CONSTANT_NameAndType: {
        if (!_need_verify) break;
        const int name_ref_index = cp->name_ref_index_at(index);
        const int signature_ref_index = cp->signature_ref_index_at(index);
        check_property(valid_symbol_at(name_ref_index),
          "Invalid constant pool index %u in class file %s",
          name_ref_index, CHECK);
        check_property(valid_symbol_at(signature_ref_index),
          "Invalid constant pool index %u in class file %s",
          signature_ref_index, CHECK);
        break;
      }
      case JVM_CONSTANT_Utf8:
        break;
      case JVM_CONSTANT_UnresolvedClass:         // fall-through
      case JVM_CONSTANT_UnresolvedClassInError: {
        ShouldNotReachHere();     // Only JVM_CONSTANT_ClassIndex should be present
        break;
      }
      case JVM_CONSTANT_ClassIndex: {
        const int class_index = cp->klass_index_at(index);
        check_property(valid_symbol_at(class_index),
          "Invalid constant pool index %u in class file %s",
          class_index, CHECK);
        cp->unresolved_klass_at_put(index, class_index, num_klasses++);
        break;
      }
      case JVM_CONSTANT_StringIndex: {
        const int string_index = cp->string_index_at(index);
        check_property(valid_symbol_at(string_index),
          "Invalid constant pool index %u in class file %s",
          string_index, CHECK);
        Symbol* const sym = cp->symbol_at(string_index);
        cp->unresolved_string_at_put(index, sym);
        break;
      }
      case JVM_CONSTANT_MethodHandle: {
        const int ref_index = cp->method_handle_index_at(index);
        check_property(valid_cp_range(ref_index, length),
          "Invalid constant pool index %u in class file %s",
          ref_index, CHECK);
        const constantTag tag = cp->tag_at(ref_index);
        const int ref_kind = cp->method_handle_ref_kind_at(index);

        switch (ref_kind) {
          case JVM_REF_getField:
          case JVM_REF_getStatic:
          case JVM_REF_putField:
          case JVM_REF_putStatic: {
            check_property(
              tag.is_field(),
              "Invalid constant pool index %u in class file %s (not a field)",
              ref_index, CHECK);
            break;
          }
          case JVM_REF_invokeVirtual:
          case JVM_REF_newInvokeSpecial: {
            check_property(
              tag.is_method(),
              "Invalid constant pool index %u in class file %s (not a method)",
              ref_index, CHECK);
            break;
          }
          case JVM_REF_invokeStatic:
          case JVM_REF_invokeSpecial: {
            check_property(
              tag.is_method() ||
              ((_major_version >= JAVA_8_VERSION) && tag.is_interface_method()),
              "Invalid constant pool index %u in class file %s (not a method)",
              ref_index, CHECK);
            break;
          }
          case JVM_REF_invokeInterface: {
            check_property(
              tag.is_interface_method(),
              "Invalid constant pool index %u in class file %s (not an interface method)",
              ref_index, CHECK);
            break;
          }
          default: {
            classfile_parse_error(
              "Bad method handle kind at constant pool index %u in class file %s",
              index, THREAD);
            return;
          }
        } // switch(refkind)
        // Keep the ref_index unchanged.  It will be indirected at link-time.
        break;
      } // case MethodHandle
      case JVM_CONSTANT_MethodType: {
        const int ref_index = cp->method_type_index_at(index);
        check_property(valid_symbol_at(ref_index),
          "Invalid constant pool index %u in class file %s",
          ref_index, CHECK);
        break;
      }
      case JVM_CONSTANT_Dynamic: {
        const int name_and_type_ref_index =
          cp->bootstrap_name_and_type_ref_index_at(index);

        check_property(valid_cp_range(name_and_type_ref_index, length) &&
          cp->tag_at(name_and_type_ref_index).is_name_and_type(),
          "Invalid constant pool index %u in class file %s",
          name_and_type_ref_index, CHECK);
        // bootstrap specifier index must be checked later,
        // when BootstrapMethods attr is available

        // Mark the constant pool as having a CONSTANT_Dynamic_info structure
        cp->set_has_dynamic_constant();
        break;
      }
      case JVM_CONSTANT_InvokeDynamic: {
        const int name_and_type_ref_index =
          cp->bootstrap_name_and_type_ref_index_at(index);

        check_property(valid_cp_range(name_and_type_ref_index, length) &&
          cp->tag_at(name_and_type_ref_index).is_name_and_type(),
          "Invalid constant pool index %u in class file %s",
          name_and_type_ref_index, CHECK);
        // bootstrap specifier index must be checked later,
        // when BootstrapMethods attr is available
        break;
      }
      default: {
        fatal("bad constant pool tag value %u", cp->tag_at(index).value());
        ShouldNotReachHere();
        break;
      }
    } // switch(tag)
  } // end of for

  cp->allocate_resolved_klasses(_loader_data, num_klasses, CHECK);

  if (!_need_verify) {
    return;
  }

  // second verification pass - checks the strings are of the right format.
  // but not yet to the other entries
  for (index = 1; index < length; index++) {
    const jbyte tag = cp->tag_at(index).value();
    switch (tag) {
      case JVM_CONSTANT_UnresolvedClass: {
        const Symbol* const class_name = cp->klass_name_at(index);
        // check the name
        verify_legal_class_name(class_name, CHECK);
        break;
      }
      case JVM_CONSTANT_NameAndType: {
        if (_need_verify) {
          const int sig_index = cp->signature_ref_index_at(index);
          const int name_index = cp->name_ref_index_at(index);
          const Symbol* const name = cp->symbol_at(name_index);
          const Symbol* const sig = cp->symbol_at(sig_index);
          guarantee_property(sig->utf8_length() != 0,
            "Illegal zero length constant pool entry at %d in class %s",
            sig_index, CHECK);
          guarantee_property(name->utf8_length() != 0,
            "Illegal zero length constant pool entry at %d in class %s",
            name_index, CHECK);

          if (Signature::is_method(sig)) {
            // Format check method name and signature
            verify_legal_method_name(name, CHECK);
            verify_legal_method_signature(name, sig, CHECK);
          } else {
            // Format check field name and signature
            verify_legal_field_name(name, CHECK);
            verify_legal_field_signature(name, sig, CHECK);
          }
        }
        break;
      }
      case JVM_CONSTANT_Dynamic: {
        const int name_and_type_ref_index =
          cp->uncached_name_and_type_ref_index_at(index);
        // already verified to be utf8
        const int name_ref_index =
          cp->name_ref_index_at(name_and_type_ref_index);
        // already verified to be utf8
        const int signature_ref_index =
          cp->signature_ref_index_at(name_and_type_ref_index);
        const Symbol* const name = cp->symbol_at(name_ref_index);
        const Symbol* const signature = cp->symbol_at(signature_ref_index);
        if (_need_verify) {
          // CONSTANT_Dynamic's name and signature are verified above, when iterating NameAndType_info.
          // Need only to be sure signature is the right type.
          if (Signature::is_method(signature)) {
            throwIllegalSignature("CONSTANT_Dynamic", name, signature, CHECK);
          }
        }
        break;
      }
      case JVM_CONSTANT_InvokeDynamic:
      case JVM_CONSTANT_Fieldref:
      case JVM_CONSTANT_Methodref:
      case JVM_CONSTANT_InterfaceMethodref: {
        const int name_and_type_ref_index =
          cp->uncached_name_and_type_ref_index_at(index);
        // already verified to be utf8
        const int name_ref_index =
          cp->name_ref_index_at(name_and_type_ref_index);
        // already verified to be utf8
        const int signature_ref_index =
          cp->signature_ref_index_at(name_and_type_ref_index);
        const Symbol* const name = cp->symbol_at(name_ref_index);
        const Symbol* const signature = cp->symbol_at(signature_ref_index);
        if (tag == JVM_CONSTANT_Fieldref) {
          if (_need_verify) {
            // Field name and signature are verified above, when iterating NameAndType_info.
            // Need only to be sure signature is non-zero length and the right type.
            if (Signature::is_method(signature)) {
              throwIllegalSignature("Field", name, signature, CHECK);
            }
          }
        } else {
          if (_need_verify) {
            // Method name and signature are individually verified above, when iterating
            // NameAndType_info.  Need to check here that signature is non-zero length and
            // the right type.
            if (!Signature::is_method(signature)) {
              throwIllegalSignature("Method", name, signature, CHECK);
            }
          }
          // If a class method name begins with '<', it must be "<init>" and have void signature.
          const unsigned int name_len = name->utf8_length();
          if (tag == JVM_CONSTANT_Methodref && name_len != 0 &&
              name->char_at(0) == JVM_SIGNATURE_SPECIAL) {
            if (name != vmSymbols::object_initializer_name()) {
              classfile_parse_error(
                "Bad method name at constant pool index %u in class file %s",
                name_ref_index, THREAD);
              return;
            } else if (!Signature::is_void_method(signature)) { // must have void signature.
              throwIllegalSignature("Method", name, signature, CHECK);
            }
          }
        }
        break;
      }
      case JVM_CONSTANT_MethodHandle: {
        const int ref_index = cp->method_handle_index_at(index);
        const int ref_kind = cp->method_handle_ref_kind_at(index);
        switch (ref_kind) {
          case JVM_REF_invokeVirtual:
          case JVM_REF_invokeStatic:
          case JVM_REF_invokeSpecial:
          case JVM_REF_newInvokeSpecial: {
            const int name_and_type_ref_index =
              cp->uncached_name_and_type_ref_index_at(ref_index);
            const int name_ref_index =
              cp->name_ref_index_at(name_and_type_ref_index);
            const Symbol* const name = cp->symbol_at(name_ref_index);
            if (ref_kind == JVM_REF_newInvokeSpecial) {
              if (name != vmSymbols::object_initializer_name()) {
                classfile_parse_error(
                  "Bad constructor name at constant pool index %u in class file %s",
                    name_ref_index, THREAD);
                return;
              }
            } else {
              if (name == vmSymbols::object_initializer_name()) {
                classfile_parse_error(
                  "Bad method name at constant pool index %u in class file %s",
                  name_ref_index, THREAD);
                return;
              }
            }
            break;
          }
          // Other ref_kinds are already fully checked in previous pass.
        } // switch(ref_kind)
        break;
      }
      case JVM_CONSTANT_MethodType: {
        const Symbol* const no_name = vmSymbols::type_name(); // place holder
        const Symbol* const signature = cp->method_type_signature_at(index);
        verify_legal_method_signature(no_name, signature, CHECK);
        break;
      }
      case JVM_CONSTANT_Utf8: {
        assert(cp->symbol_at(index)->refcount() != 0, "count corrupted");
      }
    }  // switch(tag)
  }  // end of for
}
```
