# 遍历容器里的卡片索引

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.inline.hpp --- //

template<class CardOrRangeVisitor>
inline void G1CardSet::iterate_cards_or_ranges_in_container(ContainerPtr const container, CardOrRangeVisitor &cl) {
    switch (container_type(container)) {
        case ContainerInlinePtr: {
            // 先调用start_iterate确定该分区在卡表上的起始索引
            if (cl.start_iterate(G1GCPhaseTimes::MergeRSMergedInline)) {
                G1CardSetInlinePtr ptr(container);
                // 遍历指针上的卡片索引
                ptr.iterate(cl, _config->inline_ptr_bits_per_card());
            }
            return;
        }
        case ContainerArrayOfCards: {
            if (cl.start_iterate(G1GCPhaseTimes::MergeRSMergedArrayOfCards)) {
                // 遍历数组里的卡片索引
                container_ptr<G1CardSetArray>(container)->iterate(cl);
            }
            return;
        }
        case ContainerBitMap: {
            ShouldNotReachHere();
            return;
        }
        case ContainerHowl: {
            assert(container_type(FullCardSet) == ContainerHowl, "Must be");
            if (container == FullCardSet) {
                if (cl.start_iterate(G1GCPhaseTimes::MergeRSMergedFull)) {
                    // 容器满了, 直接从头遍历到尾
                    cl(0, _config->max_cards_in_region());
                }
                return;
            }
            if (cl.start_iterate(G1GCPhaseTimes::MergeRSMergedHowl)) {
                // 遍历howl容器里的卡片索引
                container_ptr<G1CardSetHowl>(container)->iterate(cl, _config);
            }
            return;
        }
    }
    log_error(gc)("Unknown card set container type %u", container_type(container));
    ShouldNotReachHere();
}
```
