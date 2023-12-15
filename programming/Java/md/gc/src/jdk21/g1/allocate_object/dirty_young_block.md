# 在全局卡表中标记

```cpp
////////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.inline.hpp //
////////////////////////////////////////////////////////////////////////

// It dirties the cards that cover the block so that the post
// write barrier never queues anything when updating objects on this
// block. It is assumed (and in fact we assert) that the block
// belongs to a young region.
// 在全局卡表中标记这个对象属于新生代region
inline void
G1CollectedHeap::dirty_young_block(HeapWord* start, size_t word_size) {
  assert_heap_not_locked();

  DEBUG_ONLY(HeapRegion* containing_hr = heap_region_containing(start);)
  assert(word_size > 0, "pre-condition");
  assert(containing_hr->is_in(start), "it should contain start");
  assert(containing_hr->is_young(), "it should be young");
  assert(!containing_hr->is_humongous(), "it should not be humongous");
  // end指针指向对象内存范围的末尾
  HeapWord* end = start + word_size;
  assert(containing_hr->is_in(end - 1), "it should also contain end - 1");

  MemRegion mr(start, end);
  // G1堆中的全局卡表: G1CardTable* _card_table
  card_table()->g1_mark_as_young(mr);
}

/////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CardTable.cpp //
/////////////////////////////////////////////////////////////

void G1CardTable::g1_mark_as_young(const MemRegion& mr) {
  // 找到这个新分配的对象所属的卡片范围
  CardValue *const first = byte_for(mr.start());
  CardValue *const last = byte_after(mr.last());
  // 把全局卡表中从first到last的卡片都设置成g1_young_gen
  // g1_young_gen的值是2
  memset_with_concurrent_readers(first, g1_young_gen, last - first);
}
```
