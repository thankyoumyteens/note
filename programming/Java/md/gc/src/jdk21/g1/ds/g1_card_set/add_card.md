# 添加卡片

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1AddCardResult G1CardSet::add_card(uintptr_t card) {
    uint card_region;
    uint card_within_region;
    // 把card拆分成card_region和card_within_region两部分
    split_card(card, card_region, card_within_region);

    return add_card(card_region, card_within_region, true /* increment_total */);
}

void G1CardSet::split_card(uintptr_t card, uint &card_region, uint &card_within_region) const {
    // 通过逻辑右移 _split_card_shift 位将 card 的高 _split_card_shift 位提取出来
    card_region = (uint) (card >> _split_card_shift);
    // 通过与 _split_card_mask(低 _split_card_mask 位全为 1) 进行与操作，将低 _split_card_mask 位提取出来
    card_within_region = (uint) (card & _split_card_mask);
    assert(card_within_region < _config->max_cards_in_region(), "must be");
}
```

## 获取容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1CardSetHashTableValue *G1CardSet::get_or_add_container(uint card_region, bool *should_grow_table) {
    return _table->get_or_add(card_region, should_grow_table);
}

class G1CardSetHashTable : public CHeapObj<mtGCCardSet> {
    G1CardSetHashTableValue *get_or_add(uint region_idx, bool *should_grow) {
        G1CardSetHashTableLookUp lookup(region_idx);
        G1CardSetHashTableFound found;

        if (_table.get(Thread::current(), lookup, found)) {
            return found.value();
        }

        // value把分区id和容器指针关联起来
        G1CardSetHashTableValue value(region_idx, G1CardSetInlinePtr());
        bool inserted = _table.insert_get(Thread::current(), lookup, value, found, should_grow);

        if (!_inserted_card && inserted) {
            Atomic::store(&_inserted_card, true);
        }

        return found.value();
    }
};
```
