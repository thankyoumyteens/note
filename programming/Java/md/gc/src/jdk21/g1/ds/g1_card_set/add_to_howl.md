# 把卡片索引添加到 howl 容器中

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

    // 计算卡片索引应该存到bucket数组的第几个元素中
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

## 计算卡片索引应该存到 bucket 数组的第几个元素中

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.hpp --- //

class G1CardSetConfiguration {
    uint howl_bucket_index(uint card_idx) {
        // _log2_max_cards_in_howl_bitmap: 一个bucket能存储2的_log2_max_cards_in_howl_bitmap次方个卡片索引
        // 假设_log2_max_cards_in_howl_bitmap = 6, 即一个bucket能存储64个卡片索引
        // 如果card_idx = 10, 则该函数返回 0
        // 如果card_idx = 101, 则该函数返回 = 1
        return card_idx >> _log2_max_cards_in_howl_bitmap;
    }
}
```

## 添加到位图容器

位图容器是 howl 的子容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1AddCardResult G1CardSet::add_to_bitmap(ContainerPtr container, uint card_in_region) {
    // 添加到howl容器时, 会根据卡片索引计算要添加到哪个bucket(在外层的add_to_howl函数中计算)
    // 假设_log2_max_cards_in_howl_bitmap = 6, 即一个bucket能存储64个卡片索引
    // 如果card_in_region = 101,
    // 则该卡片索引会添加到下标为 (int) (101 / 2^6) = 1 的bucket中,
    // 并会把位图的第 101 - 1 * 2^6 = 37 位设为1
    G1CardSetBitMap *bitmap = container_ptr<G1CardSetBitMap>(container);
    // 获取卡片索引在位图中的第几位
    // 如果card_in_region = 101, 那么card_offset = 37
    uint card_offset = _config->howl_bitmap_offset(card_in_region);
    return bitmap->add(
            card_offset,
            _config->cards_in_howl_bitmap_threshold(),
            _config->max_cards_in_howl_bitmap()
    );
}
```

## 获取卡片索引在位图中的索引

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.hpp --- //

class G1CardSetConfiguration {
    uint howl_bitmap_offset(uint card_idx) const {
        // 和howl_bucket_index函数一起使用
        // _bitmap_hash_mask 的值是 ~(~(0) << _log2_max_cards_in_howl_bitmap)
        // 假设_log2_max_cards_in_howl_bitmap = 6, 即一个bucket能存储64个卡片索引
        // 那么_bitmap_hash_mask = ~(~(0) << 6) = 00...00111111
        // 如果card_idx = 10, 则该函数返回 10 (0 * 64 + 10 = 10)
        // 如果card_idx = 101, 则该函数返回 37 (1 * 64 + 37 = 101)
        return card_idx & _bitmap_hash_mask;
    }
}
```
