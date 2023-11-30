# 标记存活对象

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1MarkSweep.cpp

```cpp
/**
 * 标记存活对象
 */
void G1MarkSweep::mark_sweep_phase1(bool& marked_for_unloading,
                                    bool clear_all_softrefs) {

  G1CollectedHeap* g1h = G1CollectedHeap::heap();

  MarkingCodeBlobClosure follow_code_closure(&GenMarkSweep::follow_root_closure, !CodeBlobToOopClosure::FixRelocations);
  // 处理强引用
  {
    G1RootProcessor root_processor(g1h);
    // 从根集合开始标记
    root_processor.process_strong_roots(&GenMarkSweep::follow_root_closure,
                                        &GenMarkSweep::follow_cld_closure,
                                        &follow_code_closure);
  }

  ReferenceProcessor* rp = GenMarkSweep::ref_processor();
  assert(rp == g1h->ref_processor_stw(), "Sanity");
  // 处理其它类型的引用
  rp->setup_policy(clear_all_softrefs);
  const ReferenceProcessorStats& stats =
    rp->process_discovered_references(&GenMarkSweep::is_alive,
                                      &GenMarkSweep::keep_alive,
                                      &GenMarkSweep::follow_stack_closure,
                                      NULL,
                                      gc_timer(),
                                      gc_tracer()->gc_id());

  assert(GenMarkSweep::_marking_stack.is_empty(), "Marking should have completed");

  // 卸载类, 清理SystemDictionary
  // SystemDictionary用来记录所有已加载的 (类型名, 类加载器) -> 类型 的映射关系
  bool purged_class = SystemDictionary::do_unloading(&GenMarkSweep::is_alive);

  // 卸载nmethods
  CodeCache::do_unloading(&GenMarkSweep::is_alive, purged_class);

  // Prune dead klasses from subklass/sibling/implementor lists.
  Klass::clean_weak_klass_links(&GenMarkSweep::is_alive);

  // 清理字符串和符号表
  G1CollectedHeap::heap()->unlink_string_and_symbol_table(&GenMarkSweep::is_alive);
}
```
