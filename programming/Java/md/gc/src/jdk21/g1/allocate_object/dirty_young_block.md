# 把卡表中对应的卡片标记为dirty

G1 中有一个全局的卡表, 每一个卡片都对应堆中的 512 字节。

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.inline.hpp --- //

inline void
G1CollectedHeap::dirty_young_block(HeapWord *start, size_t word_size) {
    assert_heap_not_locked();

    DEBUG_ONLY(HeapRegion *containing_hr = heap_region_containing(start);)
    assert(word_size > 0, "pre-condition");
    assert(containing_hr->is_in(start), "it should contain start");
    assert(containing_hr->is_young(), "it should be young");
    assert(!containing_hr->is_humongous(), "it should not be humongous");
    // 标记 [start, end] 区间的卡表
    HeapWord *end = start + word_size;
    assert(containing_hr->is_in(end - 1), "it should also contain end - 1");

    MemRegion mr(start, end);
    // 标记为新生代
    card_table()->g1_mark_as_young(mr);
}

// --- src/hotspot/share/gc/g1/g1CardTable.cpp --- //

void G1CardTable::g1_mark_as_young(const MemRegion &mr) {
    CardValue *const first = byte_for(mr.start());
    CardValue *const last = byte_after(mr.last());

    memset_with_concurrent_readers(first, g1_young_gen, last - first);
}
```
