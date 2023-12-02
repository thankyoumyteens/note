# 更新引用的地址

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\g1MarkSweep.cpp

```cpp
void G1MarkSweep::mark_sweep_phase3() {
  G1CollectedHeap* g1h = G1CollectedHeap::heap();

  ClassLoaderDataGraph::clear_claimed_marks();
  // 更新根对象的引用
  CodeBlobToOopClosure adjust_code_closure(&GenMarkSweep::adjust_pointer_closure, CodeBlobToOopClosure::FixRelocations);
  {
    G1RootProcessor root_processor(g1h);
    root_processor.process_all_roots(&GenMarkSweep::adjust_pointer_closure,
                                     &GenMarkSweep::adjust_cld_closure,
                                     &adjust_code_closure);
  }

  assert(GenMarkSweep::ref_processor() == g1h->ref_processor_stw(), "Sanity");
  g1h->ref_processor_stw()->weak_oops_do(&GenMarkSweep::adjust_pointer_closure);

  // 处理弱引用
  JNIHandles::weak_oops_do(&always_true, &GenMarkSweep::adjust_pointer_closure);

  if (G1StringDedup::is_enabled()) {
    G1StringDedup::oops_do(&GenMarkSweep::adjust_pointer_closure);
  }

  GenMarkSweep::adjust_marks();

  G1AdjustPointersClosure blk;
  g1h->heap_region_iterate(&blk);
}

class G1AdjustPointersClosure: public HeapRegionClosure {
public:
  bool doHeapRegion(HeapRegion* r) {
    if (r->isHumongous()) {
      if (r->startsHumongous()) {
        oop obj = oop(r->bottom());
        obj->adjust_pointers();
      }
    } else {
      r->adjust_pointers();
    }
    return false;
  }
};
```

> jdk8u60-master\hotspot\src\share\vm\memory\space.cpp

```cpp
void Space::adjust_pointers() {
  if (used() == 0) {
    return;
  }

  HeapWord* q = bottom();
  HeapWord* t = end();

  while (q < t) {
    if (oop(q)->is_gc_marked()) {
      size_t size = oop(q)->adjust_pointers();
      q += size;
    } else {
      q += block_size(q);
    }
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\oops\oop.inline.hpp

```cpp
inline int oopDesc::adjust_pointers() {
  int s = klass()->oop_adjust_pointers(this);
  return s;
}
```

> jdk8u60-master\hotspot\src\share\vm\oops\instanceKlass.cpp

```cpp
int InstanceKlass::oop_adjust_pointers(oop obj) {
  int size = size_helper();
  // 遍历对象的字段, 更新引用
  InstanceKlass_OOP_MAP_ITERATE( \
    obj, \
    MarkSweep::adjust_pointer(p), \
    assert_is_in)
  return size;
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\shared\markSweep.inline.hpp

```cpp
template <class T> inline void MarkSweep::adjust_pointer(T* p) {
  T heap_oop = oopDesc::load_heap_oop(p);
  if (!oopDesc::is_null(heap_oop)) {
    oop obj     = oopDesc::decode_heap_oop_not_null(heap_oop);
    oop new_obj = oop(obj->mark()->decode_pointer());
    if (new_obj != NULL) {
      // 更新指针位置
      oopDesc::encode_store_heap_oop_not_null(p, new_obj);
    }
  }
}
```
