# Full GC

对象在堆中慢速分配时, 如果还分配失败, 会进行 Full GC。在 Full GC 之前需要做一些预处理，主要有停止并发标记、停止增量回收等动作。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1CollectedHeap.cpp

```cpp
bool G1CollectedHeap::do_collection(bool explicit_gc,
                                    bool clear_all_soft_refs,
                                    size_t word_size) {
  // ...
  G1MarkSweep::invoke_at_safepoint(ref_processor_stw(), do_clear_all_soft_refs);
  // ...
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1MarkSweep.cpp

```cpp
/**
 * 串行Full GC, 使用标记清理算法
 * clear_all_softrefs: 是否清理软引用
 */
void G1MarkSweep::invoke_at_safepoint(ReferenceProcessor* rp,
                                      bool clear_all_softrefs) {
  assert(SafepointSynchronize::is_at_safepoint(), "must be at a safepoint");

  SharedHeap* sh = SharedHeap::heap();

  assert(GenMarkSweep::ref_processor() == NULL, "no stomping");
  assert(rp != NULL, "should be non-NULL");
  assert(rp == G1CollectedHeap::heap()->ref_processor_stw(), "Precondition");

  GenMarkSweep::_ref_processor = rp;
  rp->setup_policy(clear_all_softrefs);

  CodeCache::gc_prologue();
  Threads::gc_prologue();

  bool marked_for_unloading = false;

  allocate_stacks();

  BiasedLocking::preserve_marks();
  // 标记存活对象
  mark_sweep_phase1(marked_for_unloading, clear_all_softrefs);
  // 计算对象的新地址
  mark_sweep_phase2();

  COMPILER2_PRESENT(DerivedPointerTable::set_active(false));

  mark_sweep_phase3();

  mark_sweep_phase4();

  GenMarkSweep::restore_marks();
  BiasedLocking::restore_marks();
  GenMarkSweep::deallocate_stacks();

  Threads::gc_epilogue();
  CodeCache::gc_epilogue();
  JvmtiExport::gc_epilogue();

  GenMarkSweep::_ref_processor = NULL;
}
```
