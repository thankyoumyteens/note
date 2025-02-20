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
        CardOrRanges<Closure> cl(
                _cl,
                // 算出card region属于哪个分区
                card_region_idx >> _log_card_regions_per_region,
                // card_region_idx & _card_regions_per_region_mask: 确保card region索引不越界
                // 换算出这个card region中卡片索引的偏移量
                // 比如card region索引为2, 每个card region有4个卡片索引(_log_card_region_size = 2)
                // 那么值为3的卡片索引在整个分区中的实际值应该是: (2 << 2) + 3 = 11
                (card_region_idx & _card_regions_per_region_mask) << _log_card_region_size
        );
        // 遍历容器内的所有卡片索引
        // 1. 先调用start_iterate
        // 2. 再通过()运算符调用do_card或do_card_range
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
