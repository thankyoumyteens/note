# 遍历 howl 容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

template<class CardOrRangeVisitor>
inline void G1CardSetHowl::iterate(CardOrRangeVisitor &found, G1CardSetConfiguration *config) {
    // _buckets中的每个元素都是一个容器
    for (uint i = 0; i < config->num_buckets_in_howl(); ++i) {
        // 遍历每个bucket内的卡片索引
        iterate_cardset(_buckets[i], i, found, config);
    }
}

template<class CardOrRangeVisitor>
inline void G1CardSetHowl::iterate_cardset(ContainerPtr const container, uint index, CardOrRangeVisitor &found,
                                           G1CardSetConfiguration *config) {
    switch (G1CardSet::container_type(container)) {
        case G1CardSet::ContainerInlinePtr: {
            if (found.start_iterate(G1GCPhaseTimes::MergeRSHowlInline)) {
                G1CardSetInlinePtr ptr(container);
                ptr.iterate(found, config->inline_ptr_bits_per_card());
            }
            return;
        }
        case G1CardSet::ContainerArrayOfCards: {
            if (found.start_iterate(G1GCPhaseTimes::MergeRSHowlArrayOfCards)) {
                G1CardSet::container_ptr<G1CardSetArray>(container)->iterate(found);
            }
            return;
        }
        case G1CardSet::ContainerBitMap: {
            // 遍历位图容器
            if (found.start_iterate(G1GCPhaseTimes::MergeRSHowlBitmap)) {
                // 添加到howl容器时, 会根据卡片索引计算要添加到哪个bucket
                // 假设_log2_max_cards_in_howl_bitmap = 6, 即一个bucket能存储64个卡片索引
                // 如果card_idx = 101,
                // 则该卡片索引会添加到下标为 (int) (101 / 2^6) = 1 的bucket中,
                // 并会把位图的第 101 - 1 * 2^6 = 37 位设为1

                // 在遍历时, found函数接收的事卡片索引的真实值, 所以需要还原
                // index是bucket数组的索引
                // 如果index为1, 则offset = 1 * 2^6 = 64
                // 那么在遍历到位图的第37位时, 会把它还原为 37 + 64 = 101
                uint offset = index << config->log2_max_cards_in_howl_bitmap();
                G1CardSet::container_ptr<G1CardSetBitMap>(container)->iterate(
                        found,
                        config->max_cards_in_howl_bitmap(),
                        offset
                );
            }
            return;
        }
        case G1CardSet::ContainerHowl: { // actually FullCardSet
            assert(container == G1CardSet::FullCardSet, "Must be");
            if (found.start_iterate(G1GCPhaseTimes::MergeRSHowlFull)) {
                uint offset = index << config->log2_max_cards_in_howl_bitmap();
                found(offset, config->max_cards_in_howl_bitmap());
            }
            return;
        }
    }
}

template<class CardVisitor>
inline void G1CardSetBitMap::iterate(CardVisitor &found, size_t size_in_bits, uint offset) {
    BitMapView bm(_bits, size_in_bits);
    bm.iterate([&](BitMap::idx_t idx) { found(offset | (uint) idx); });
}

class BitMap {
    template<typename BitMapClosureType>
    bool iterate(BitMapClosureType *cl) const {
        return iterate(cl, 0, size());
    }
};
```
