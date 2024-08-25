# 重写

为优化解释器性能，虚拟机向运行时常量池添加了额外的缓存项(即 constantPoolCache)，因此，原本字节码中表示常量池项索引位置的字节也需要相应地跟着调整。这个调整过程需要对 Class 定义的所有方法的字节码进行重写。

```cpp
// --- src/hotspot/share/oops/instanceKlass.cpp --- //

// Rewrite the byte codes of all of the methods of a class.
// The rewriter must be called exactly once. Rewriting must happen after
// verification but before the first method of the class is executed.
void InstanceKlass::rewrite_class(TRAPS) {
  assert(is_loaded(), "must be loaded");
  if (is_rewritten()) {
    assert(is_shared(), "rewriting an unshared class?");
    return;
  }
  Rewriter::rewrite(this, CHECK);
  set_rewritten();
}

// --- src/hotspot/share/interpreter/rewriter.cpp --- //

void Rewriter::rewrite(InstanceKlass* klass, TRAPS) {
#if INCLUDE_CDS
  if (klass->is_shared()) {
    assert(!klass->is_rewritten(), "rewritten shared classes cannot be rewritten again");
  }
#endif // INCLUDE_CDS
  ResourceMark rm(THREAD);
  constantPoolHandle cpool(THREAD, klass->constants());
  Rewriter     rw(klass, cpool, klass->methods(), CHECK);
  // (That's all, folks.)
}

Rewriter::Rewriter(InstanceKlass* klass, const constantPoolHandle& cpool, Array<Method*>* methods, TRAPS)
  : _klass(klass),
    _pool(cpool),
    _methods(methods),
    _cp_map(cpool->length()),
    _cp_cache_map(cpool->length() / 2),
    _reference_map(cpool->length()),
    _resolved_references_map(cpool->length() / 2),
    _invokedynamic_references_map(cpool->length() / 2),
    _method_handle_invokers(cpool->length()),
    _invokedynamic_index(0)
{

  // Rewrite bytecodes - exception here exits.
  rewrite_bytecodes(CHECK);

  // Stress restoring bytecodes
  if (StressRewriter) {
    restore_bytecodes(THREAD);
    rewrite_bytecodes(CHECK);
  }

  // allocate constant pool cache, now that we've seen all the bytecodes
  make_constant_pool_cache(THREAD);

  // Restore bytecodes to their unrewritten state if there are exceptions
  // rewriting bytecodes or allocating the cpCache
  if (HAS_PENDING_EXCEPTION) {
    restore_bytecodes(THREAD);
    return;
  }

  // Relocate after everything, but still do this under the is_rewritten flag,
  // so methods with jsrs in custom class lists in aren't attempted to be
  // rewritten in the RO section of the shared archive.
  // Relocated bytecodes don't have to be restored, only the cp cache entries
  int len = _methods->length();
  for (int i = len-1; i >= 0; i--) {
    methodHandle m(THREAD, _methods->at(i));

    if (m->has_jsrs()) {
      m = rewrite_jsrs(m, THREAD);
      // Restore bytecodes to their unrewritten state if there are exceptions
      // relocating bytecodes.  If some are relocated, that is ok because that
      // doesn't affect constant pool to cpCache rewriting.
      if (HAS_PENDING_EXCEPTION) {
        restore_bytecodes(THREAD);
        return;
      }
      // Method might have gotten rewritten.
      methods->at_put(i, m());
    }
  }
}
```
