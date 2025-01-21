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

G1AddCardResult G1CardSet::add_card(uint card_region, uint card_in_region, bool increment_total) {
    G1AddCardResult add_result;
    ContainerPtr to_transfer = nullptr;
    ContainerPtr container;

    bool should_grow_table = false;
    // 获取分区(card_region)对应的容器, 如果不存在则新建一个
    G1CardSetHashTableValue *table_entry = get_or_add_container(card_region, &should_grow_table);
    while (true) {
        // 获取容器, 并增加引用计数
        container = acquire_container(&table_entry->_container);
        // 把卡片索引(card_in_region)添加到container中
        add_result = add_to_container(&table_entry->_container, container, card_region, card_in_region,
                                      increment_total);

        if (add_result != Overflow) {
            // 添加成功
            break;
        }
        // container满了, 需要粗化并重试
        bool coarsened = coarsen_container(&table_entry->_container, container, card_in_region);
        _coarsen_stats.record_coarsening(container_type(container), !coarsened);
        if (coarsened) {
            // 成功
            add_result = Added;
            to_transfer = container;
            break;
        }
        // 其它线程已经做过粗化了, 下一轮循环重试
        release_and_maybe_free_container(container);
    }

    if (increment_total && add_result == Added) {
        // 增加卡片计数
        Atomic::inc(&table_entry->_num_occupied, memory_order_relaxed);
        Atomic::inc(&_num_occupied, memory_order_relaxed);
    }
    if (should_grow_table) {
        // 扩容
        _table->grow();
    }
    if (to_transfer != nullptr) {
        // 把旧容器的数据转移到新容器
        transfer_cards(table_entry, to_transfer, card_region);
    }

    // 可能会释放旧容器
    release_and_maybe_free_container(container);

    return add_result;
}
```

## 获取或新建容器

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
