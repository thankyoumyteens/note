# 合并到卡表

```cpp
// --- src/hotspot/share/gc/g1/heapRegionRemSet.inline.hpp --- //

template<class CardOrRangeVisitor>
inline void HeapRegionRemSet::iterate_for_merge(CardOrRangeVisitor &cl) {
    G1HeapRegionRemSetMergeCardClosure<CardOrRangeVisitor, G1ContainerCardsOrRanges> cl2(
            &_card_set,
            cl,
            // 每个分区有多少个card_region(2的log2_card_regions_per_heap_region次方个)
            _card_set.config()->log2_card_regions_per_heap_region(),
            // 每个card_region有多少个卡片索引(2的log2_cards_per_card_region次方个)
            _card_set.config()->log2_cards_per_card_region()
    );
    // 遍历card set中的容器
    // 并把容器作为参数传入cl2的do_containerptr函数中
    _card_set.iterate_containers(&cl2, true /* at_safepoint */);
}

template<typename Closure, template<typename> class CardOrRanges>
class G1HeapRegionRemSetMergeCardClosure : public G1CardSet::ContainerPtrClosure {
    void do_containerptr(uint card_region_idx, size_t num_occupied, G1CardSet::ContainerPtr container) override {
        // cl是G1ContainerCardsOrRanges类型
        CardOrRanges<Closure> cl(
                // cl在这里是G1MergeCardSetClosure
                _cl,
                // 算出card region属于哪个分区
                card_region_idx >> _log_card_regions_per_region,
                // card_region_idx & _card_regions_per_region_mask: 确保card region索引不越界
                // 换算出这个card region中卡片索引的偏移量
                // 比如card region索引为2, 每个card region有4个卡片索引(_log_card_region_size = 2)
                // 那么值为3的卡片索引在整个分区中的实际值应该是: (2 * 2^2) + 3 = 11
                (card_region_idx & _card_regions_per_region_mask) << _log_card_region_size
        );
        // 遍历容器内的所有卡片索引:
        // 1. 先调用cl的start_iterate函数
        // 2. 再通过cl的重载()运算符调用do_card或do_card_range函数
        _card_set->iterate_cards_or_ranges_in_container(container, cl);
    }
};
```

## G1ContainerCardsOrRanges

```cpp
// --- src/hotspot/share/gc/g1/heapRegionRemSet.inline.hpp --- //

template<typename Closure>
class G1ContainerCardsOrRanges {
    Closure &_cl;
    uint _region_idx;
    uint _offset;

public:
    G1ContainerCardsOrRanges(Closure &cl, uint region_idx, uint offset) : _cl(cl), _region_idx(region_idx),
                                                                          _offset(offset) {}

    bool start_iterate(uint tag) {
        // 确定该分区在卡表上的起始索引
        return _cl.start_iterate(tag, _region_idx);
    }

    void operator()(uint card_idx) {
        // 处理一个卡片索引
        _cl.do_card(card_idx + _offset);
    }

    void operator()(uint card_idx, uint length) {
        // 处理一组卡片索引
        _cl.do_card_range(card_idx + _offset, length);
    }
};
```

## start_iterate

```cpp
// --- src/hotspot/share/gc/g1/g1RemSet.cpp --- //

class G1MergeCardSetClosure : public HeapRegionClosure {
    // 返回给定分区是否需要遍历
    bool start_iterate(uint const tag, uint const region_idx) {
        assert(tag < G1GCPhaseTimes::MergeRSCards, "invalid tag %u", tag);
        if (remember_if_interesting(region_idx)) {
            // region_idx: 分区索引
            // _region_base_idx: 该分区在卡表上的起始索引
            // HeapRegion::LogCardsPerRegion: 每个分区需要用几张卡片表示(2的HeapRegion::LogCardsPerRegion次方张)
            _region_base_idx = (size_t) region_idx << HeapRegion::LogCardsPerRegion;
            _stats.inc_card_set_merged(tag);
            return true;
        }
        // 该分区无需遍历
        return false;
    }

    // 返回给定分区是否包含需要扫描的卡片
    bool remember_if_interesting(uint const region_idx) {
        // 判断给定分区是否包含需要扫描的卡片
        if (!_scan_state->contains_cards_to_process(region_idx)) {
            // 不包含, 该分区无需遍历
            return false;
        }
        // 标记该分区在疏散阶段需要扫描的是否有脏卡片
        _scan_state->add_dirty_region(region_idx);
        // 该分区需要遍历
        return true;
    }
};

class G1RemSetScanState : public CHeapObj<mtGC> {
    bool contains_cards_to_process(uint const region_idx) const {
        HeapRegion *hr = G1CollectedHeap::heap()->region_at_or_null(region_idx);
        // 需要扫描的分区:
        // - 不在回收集中
        // - 老年代或大对象分区
        return (hr != nullptr && !hr->in_collection_set() && hr->is_old_or_humongous());
    }
};
```

## do_card

```cpp
// --- src/hotspot/share/gc/g1/g1RemSet.cpp --- //

class G1MergeCardSetClosure : public HeapRegionClosure {
    void do_card(uint const card_idx) {
        // 根据卡片索引拿到卡表上的卡片
        G1CardTable::CardValue *to_prefetch = _ct->byte_for_index(_region_base_idx + card_idx);
        // 把to_prefetch添加到数组末尾, 并把添加前的最后一个元素赋值给to_process
        G1CardTable::CardValue *to_process = _merge_card_set_cache.push(to_prefetch);

        mark_card(to_process);
    }

    void mark_card(G1CardTable::CardValue *value) {
        // _ct: 卡表
        // mark_clean_as_dirty: 把卡片标记成脏卡片
        if (_ct->mark_clean_as_dirty(value)) {
            // index_for_cardvalue: 获取卡片在卡表中的索引
            // set_chunk_dirty: 一个分区被分成多个块(chunk), 把这个卡片所在的块标记为脏
            _scan_state->set_chunk_dirty(_ct->index_for_cardvalue(value));
        }
        _stats.inc_remset_cards();
    }
};

template<class T>
class G1MergeHeapRootsPrefetchCache {
    T *push(T *elem) {
        // 遍历数组时，提前把后续元素放到L1缓存中, 提高性能
        Prefetch::write(elem, 0);
        T *result = _cache[_cur_cache_idx];
        _cache[_cur_cache_idx++] = elem;
        _cur_cache_idx &= (CacheSize - 1);

        return result;
    }
};
```

## do_card_range

```cpp
// --- src/hotspot/share/gc/g1/g1RemSet.cpp --- //

class G1MergeCardSetClosure : public HeapRegionClosure {
    void do_card_range(uint const start_card_idx, uint const length) {
        // 把这些卡片标记为脏
        _ct->mark_range_dirty(_region_base_idx + start_card_idx, length);
        _stats.inc_remset_cards(length);
        // 把这些卡片所在的块都标记为脏
        _scan_state->set_chunk_range_dirty(_region_base_idx + start_card_idx, length);
    }
};

class G1RemSetScanState : public CHeapObj<mtGC> {
    void set_chunk_range_dirty(size_t const region_card_idx, size_t const card_length) {
        size_t chunk_idx = region_card_idx >> _scan_chunks_shift;
        size_t const end_chunk = (region_card_idx + card_length - 1) >> _scan_chunks_shift;
        for (; chunk_idx <= end_chunk; chunk_idx++) {
            _region_scan_chunks[chunk_idx] = true;
        }
    }
};

// --- src/hotspot/share/gc/g1/g1CardTable.inline.hpp --- //

inline void G1CardTable::mark_range_dirty(size_t start_card_index, size_t num_cards) {
    assert(is_aligned(start_card_index, sizeof(size_t)), "Start card index must be aligned.");
    assert(is_aligned(num_cards, sizeof(size_t)), "Number of cards to change must be evenly divisible.");

    // 为了提高效率按块遍历, 如果这个块内的卡片都是脏卡片则直接跳过这个块
    // 如果这个块内都是干净的卡片则可以一次性把整个块标记为脏
    // 只有当这个块内的卡片既有脏卡片又有干净的卡片时, 才需要逐个处理块内的每个卡片
    // 在这里, 一个块的大小是size_t
    size_t const num_chunks = num_cards / sizeof(size_t);

    // 取出起始的块
    size_t *cur_word = (size_t *) &_byte_map[start_card_index];
    // 遍历到哪个块
    size_t *const end_word_map = cur_word + num_chunks;
    while (cur_word < end_word_map) {
        size_t value = *cur_word;
        if (value == WordAllClean) { // WordAllClean: size_t位二进制全是0
            *cur_word = WordAllDirty; // WordAllDirty: size_t位二进制全是1
        } else if (value == WordAllDirty) {
            // do nothing.
        } else {
            // 块内既有脏卡片也有干净的卡片
            // 逐个处理块内的每个卡片
            CardValue *cur = (CardValue *) cur_word;
            for (size_t i = 0; i < sizeof(size_t); i++) {
                CardValue value = *cur;
                // 把干净的卡片标为脏
                if (value == clean_card_val()) {
                    *cur = dirty_card_val();
                }
                cur++;
            }
        }
        cur_word++;
    }
}
```
