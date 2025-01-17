# 添加卡片

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1AddCardResult G1CardSet::add_card(uintptr_t card) {
    uint card_region;
    uint card_within_region;
    split_card(card, card_region, card_within_region);

    return add_card(card_region, card_within_region, true /* increment_total */);
}
```
