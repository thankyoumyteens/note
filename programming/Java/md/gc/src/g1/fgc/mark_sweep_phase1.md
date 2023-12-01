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

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1RootProcessor.cpp

```cpp
void G1RootProcessor::process_strong_roots(OopClosure* oops,
                                           CLDClosure* clds,
                                           CodeBlobClosure* blobs) {
  // 处理java根
  process_java_roots(oops, clds, clds, NULL, blobs, NULL, 0);
  // 处理vm根
  process_vm_roots(oops, NULL, NULL, 0);
  // 通知标记完成
  _process_strong_tasks->all_tasks_completed();
}

void G1RootProcessor::process_java_roots(OopClosure* strong_roots,
                                         CLDClosure* thread_stack_clds,
                                         CLDClosure* strong_clds,
                                         CLDClosure* weak_clds,
                                         CodeBlobClosure* strong_code,
                                         G1GCPhaseTimes* phase_times,
                                         uint worker_i) {
  assert(thread_stack_clds == NULL || weak_clds == NULL, "There is overlap between those, only one may be set");

  {
    // 处理类加载器
    // 每个类加载器都会对应一个ClassLoaderData,
    // 里面会存具体的类加载器对象, 加载的klass, 管理内存的metaspace等,
    // 它是一个链式结构
    G1GCParPhaseTimesTracker x(phase_times, G1GCPhaseTimes::CLDGRoots, worker_i);
    if (!_process_strong_tasks->is_task_claimed(G1RP_PS_ClassLoaderDataGraph_oops_do)) {
      // 通过ClassLoaderDataGraph来遍历这些ClassLoaderData,
      // ClassLoaderDataGraph的第一个节点是BootstrapClassLoader
      ClassLoaderDataGraph::roots_cld_do(strong_clds, weak_clds);
    }
  }

  {
    // 处理对象
    G1GCParPhaseTimesTracker x(phase_times, G1GCPhaseTimes::ThreadRoots, worker_i);
    Threads::possibly_parallel_oops_do(strong_roots, thread_stack_clds, strong_code);
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\runtime\thread.cpp

```cpp
void Threads::possibly_parallel_oops_do(OopClosure* f, CLDClosure* cld_f, CodeBlobClosure* cf) {
  SharedHeap* sh = SharedHeap::heap();
  bool is_par = sh->n_par_threads() > 0;
  int cp = SharedHeap::heap()->strong_roots_parity();
  ALL_JAVA_THREADS(p) {
    if (p->claim_oops_do(is_par, cp)) {
      p->oops_do(f, cld_f, cf);
    }
  }
  VMThread* vmt = VMThread::vm_thread();
  if (vmt->claim_oops_do(is_par, cp)) {
    vmt->oops_do(f, cld_f, cf);
  }
}

void Thread::oops_do(OopClosure* f, CLDClosure* cld_f, CodeBlobClosure* cf) {
  active_handles()->oops_do(f);
  f->do_oop((oop*)&_pending_exception);
  handle_area()->oops_do(f);
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\shared\markSweep.cpp

```cpp
void MarkSweep::FollowRootClosure::do_oop(oop* p) {
  follow_root(p);
}
void MarkSweep::FollowRootClosure::do_oop(narrowOop* p) {
  follow_root(p);
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\shared\markSweep.inline.hpp

```cpp
template <class T> inline void MarkSweep::follow_root(T* p) {
  assert(!Universe::heap()->is_in_reserved(p),
         "roots shouldn't be things within the heap");
  T heap_oop = oopDesc::load_heap_oop(p);
  if (!oopDesc::is_null(heap_oop)) {
    oop obj = oopDesc::decode_heap_oop_not_null(heap_oop);
    if (!obj->mark()->is_marked()) {
      // 标记对象
      mark_object(obj);
      // 遍历对象的每一个字段
      // 标记它们指向的对象, 并把这些对象放入标记栈
      obj->follow_contents();
    }
  }
  // 处理标记栈中的对象
  follow_stack();
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\shared\markSweep.cpp

```cpp
void MarkSweep::follow_stack() {
  do {
    // 标记对象
    while (!_marking_stack.is_empty()) {
      oop obj = _marking_stack.pop();
      // 遍历对象的每一个字段
      // 标记它们指向的对象, 并把这些对象放入标记栈
      obj->follow_contents();
    }
    // 标记对象数组
    if (!_objarray_stack.is_empty()) {
      ObjArrayTask task = _objarray_stack.pop();
      ObjArrayKlass* k = (ObjArrayKlass*)task.obj()->klass();
      // 遍历数组的每一个元素
      // 标记它们, 并把这些对象放入标记栈
      k->oop_follow_contents(task.obj(), task.index());
    }
  } while (!_marking_stack.is_empty() || !_objarray_stack.is_empty());
}
```
