# 把旧容器的数据转移到新容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

class G1TransferCard : public StackObj {
    G1CardSet *_card_set;
    uint _region_idx;
public:
    G1TransferCard(G1CardSet *card_set, uint region_idx) : _card_set(card_set), _region_idx(region_idx) {}

    void operator()(uint card_idx) {
        // 把旧容器中的卡片索引重新添加到card set中
        _card_set->add_card(_region_idx, card_idx, false);
    }
};

template<class CardVisitor>
void G1CardSet::iterate_cards_during_transfer(ContainerPtr const container, CardVisitor &cl) {
    uint type = container_type(container);
    assert(type == ContainerInlinePtr || type == ContainerArrayOfCards,
           "invalid card set type %d to transfer from",
           container_type(container));

    switch (type) {
        case ContainerInlinePtr: {
            G1CardSetInlinePtr ptr(container);
            ptr.iterate(cl, _config->inline_ptr_bits_per_card());
            return;
        }
        case ContainerArrayOfCards: {
            container_ptr<G1CardSetArray>(container)->iterate(cl);
            return;
        }
        default:
            ShouldNotReachHere();
    }
}

// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

template<class CardVisitor>
inline void G1CardSetInlinePtr::iterate(CardVisitor &found, uint bits_per_card) {
    uint const num_cards = num_cards_in(_value);
    uintptr_t const card_mask = (1 << bits_per_card) - 1;

    // 把指针中的每一项重新添加到card set中
    uintptr_t value = ((uintptr_t) _value) >> card_pos_for(0, bits_per_card);
    for (uint cur_idx = 0; cur_idx < num_cards; cur_idx++) {
        found(value & card_mask);
        value >>= bits_per_card;
    }
}

template<class CardVisitor>
void G1CardSetArray::iterate(CardVisitor &found) {
    EntryCountType num_entries = Atomic::load_acquire(&_num_entries) & EntryMask;
    // 把数组的每一项重新添加到card set中
    for (EntryCountType idx = 0; idx < num_entries; idx++) {
        found(_data[idx]);
    }
}
```

## 非 howl 子容器转移

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

// source_container 旧容器
void G1CardSet::transfer_cards(G1CardSetHashTableValue *table_entry, ContainerPtr source_container, uint card_region) {
    assert(source_container != FullCardSet, "Should not need to transfer from FullCardSet");
    if (container_type(source_container) != ContainerHowl) {
        // 把旧的source_container中的卡片索引重新添加到card set中
        G1TransferCard iter(this, card_region);
        iterate_cards_during_transfer(source_container, iter);
    } else {
        // howl容器在transfer_cards_in_howl函数中转移
        assert(container_type(source_container) == ContainerHowl, "must be");
        Atomic::add(&_num_occupied, _config->max_cards_in_region() - table_entry->_num_occupied, memory_order_relaxed);
    }
}
```
