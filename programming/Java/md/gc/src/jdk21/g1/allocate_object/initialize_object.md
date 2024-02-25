# 初始化对象

```cpp
//////////////////////////////////////////////////////////////////
// src/hotspot/share/gc/shared/memAllocator.cpp //
//////////////////////////////////////////////////////////////////

oop ObjAllocator::initialize(HeapWord* mem) const {
  mem_clear(mem);
  return finish(mem);
}

void MemAllocator::mem_clear(HeapWord* mem) const {
  assert(mem != nullptr, "cannot initialize null object");
  const size_t hs = oopDesc::header_size();
  assert(_word_size >= hs, "unexpected object size");
  // 设置GC分代年龄
  oopDesc::set_klass_gap(mem, 0);
  // 把对象的内存空间用0填充
  Copy::fill_to_aligned_words(mem + hs, _word_size - hs);
}

oop MemAllocator::finish(HeapWord* mem) const {
  assert(mem != nullptr, "null object pointer");
  // 初始化 mark word
  oopDesc::set_mark(mem, markWord::prototype());
  // 设置元数据指针
  oopDesc::release_set_klass(mem, _klass);
  return cast_to_oop(mem);
}
```
