# 把卡片索引添加到容器中

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1AddCardResult G1CardSet::add_to_container(ContainerPtr volatile *container_addr,
                                            ContainerPtr container,
                                            uint card_region,
                                            uint card_in_region,
                                            bool increment_total) {
    assert(container_addr != nullptr, "must be");

    G1AddCardResult add_result;

    switch (container_type(container)) {
        case ContainerInlinePtr: { // 内联指针卡片模式
            add_result = add_to_inline_ptr(container_addr, container, card_in_region);
            break;
        }
        case ContainerArrayOfCards: { // 卡片数组模式
            add_result = add_to_array(container, card_in_region);
            break;
        }
        case ContainerBitMap: { // 位图模式
            add_result = add_to_bitmap(container, card_in_region);
            break;
        }
        case ContainerHowl: { // Howl 模式
            assert(ContainerHowl == container_type(FullCardSet), "must be");
            if (container == FullCardSet) {
                return Found;
            }
            add_result = add_to_howl(container, card_region, card_in_region, increment_total);
            break;
        }
        default:
            ShouldNotReachHere();
    }
    return add_result;
}
```

## 添加到内联指针卡片容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1AddCardResult
G1CardSet::add_to_inline_ptr(ContainerPtr volatile *container_addr, ContainerPtr container, uint card_in_region) {
    G1CardSetInlinePtr value(container_addr, container);
    return value.add(card_in_region, _config->inline_ptr_bits_per_card(), _config->max_cards_in_inline_ptr());
}
```

## 添加到卡片数组容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1AddCardResult G1CardSet::add_to_array(ContainerPtr container, uint card_in_region) {
    G1CardSetArray *array = container_ptr<G1CardSetArray>(container);
    return array->add(card_in_region);
}
```

## 添加到位图容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1AddCardResult G1CardSet::add_to_bitmap(ContainerPtr container, uint card_in_region) {
    G1CardSetBitMap *bitmap = container_ptr<G1CardSetBitMap>(container);
    uint card_offset = _config->howl_bitmap_offset(card_in_region);
    return bitmap->add(card_offset, _config->cards_in_howl_bitmap_threshold(), _config->max_cards_in_howl_bitmap());
}
```

## 添加到 Howl 容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1AddCardResult G1CardSet::add_to_howl(ContainerPtr parent_container,
                                       uint card_region,
                                       uint card_in_region,
                                       bool increment_total) {
    G1CardSetHowl *howl = container_ptr<G1CardSetHowl>(parent_container);

    G1AddCardResult add_result;
    ContainerPtr to_transfer = nullptr;
    ContainerPtr container;

    // 保证卡片索引不超出bucket数组的长度
    uint bucket = _config->howl_bucket_index(card_in_region);
    // return &_buckets[index]
    ContainerPtr volatile *bucket_entry = howl->get_container_addr(bucket);

    while (true) {
        if (Atomic::load(&howl->_num_entries) >= _config->cards_in_howl_threshold()) {
            // 容器中的卡片索引数量达到阈值
            return Overflow;
        }

        // 获取bucket_entry指向的容器
        container = acquire_container(bucket_entry);
        // 把卡片索引添加到bucket_entry指向的容器中
        add_result = add_to_container(bucket_entry, container, card_region, card_in_region);

        if (add_result != Overflow) {
            break;
        }
        // Card set container has overflown. Coarsen or retry.
        // 粗化并重试
        // Howl内部的容器粗化按照以下顺序进行: Free -> ContainerInlinePtr -> ContainerArrayOfCards -> ContainerBitMap -> Full
        bool coarsened = coarsen_container(bucket_entry, container, card_in_region, true /* within_howl */);
        _coarsen_stats.record_coarsening(container_type(container) + G1CardSetCoarsenStats::CoarsenHowlOffset,
                                         !coarsened);
        if (coarsened) {
            // We successful coarsened this card set container (and in the process added the card).
            // 成功
            add_result = Added;
            to_transfer = container;
            break;
        }
        // Somebody else beat us to coarsening. Retry.
        // 失败, 由于acquire_container会增加_ref_count,
        // 所以在这里调用release_and_maybe_free_container减少_ref_count
        release_and_maybe_free_container(container);
    }

    if (increment_total && add_result == Added) {
        // 增加卡片索引计数
        Atomic::inc(&howl->_num_entries, memory_order_relaxed);
    }

    if (to_transfer != nullptr) {
        // 把旧容器的数据转移到新容器
        transfer_cards_in_howl(parent_container, to_transfer, card_region);
    }

    release_and_maybe_free_container(container);
    return add_result;
}
```
