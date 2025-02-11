# 容器粗化并添加卡片索引

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

bool G1CardSet::coarsen_container(ContainerPtr volatile *container_addr,
                                  ContainerPtr cur_container,
                                  uint card_in_region,
                                  bool within_howl) {
    ContainerPtr new_container = nullptr;

    // 创建新容器
    switch (container_type(cur_container)) {
        case ContainerArrayOfCards: {
            // 非内部容器: 从 ContainerArrayOfCards 粗化成 ContainerHowl
            // howl的内部容器: 从 ContainerArrayOfCards 粗化成 ContainerBitMap
            new_container = create_coarsened_array_of_cards(card_in_region, within_howl);
            break;
        }
        case ContainerBitMap: {
            // ContainerBitMap只能是howl的内部容器类型
            // 从 ContainerBitMap 粗化成 Full
            new_container = FullCardSet;
            break;
        }
        case ContainerInlinePtr: {
            // 非内部容器: 从 ContainerInlinePtr 粗化成 ContainerArrayOfCards
            // howl的内部容器: 从 ContainerInlinePtr 粗化成 ContainerArrayOfCards
            uint const size = _config->max_cards_in_array();
            // 分配数组内存
            uint8_t *data = allocate_mem_object(ContainerArrayOfCards);
            // 使用 placement new 在已分配的内存 data 上构造 G1CardSetArray 对象
            // placement new 是 C++ 中的一种特殊的 new 表达式，它允许在已分配的内存块上构造对象，
            // 而不是像普通的 new 表达式那样先分配内存再构造对象
            new(data) G1CardSetArray(card_in_region, size);
            // 把容器类型拼到指针最低两位上
            new_container = make_container_ptr(data, ContainerArrayOfCards);
            break;
        }
        case ContainerHowl: {
            // 从 ContainerHowl 粗化成 Full
            new_container = FullCardSet;
            break;
        }
        default:
            ShouldNotReachHere();
    }

    // 用new_container替换cur_container
    ContainerPtr old_value = Atomic::cmpxchg(container_addr, cur_container, new_container);
    if (old_value == cur_container) {
        // 替换成功, 把旧容器中的卡片索引转移到新容器的工作由本函数的调用者来完成

        // 把cur_container的_ref_count减2
        // 由于调用者使用acquire_container()函数增加了_ref_count,
        // 本次减去不会使_ref_count等于1, 所以should_free一定是false
        bool should_free = release_container(cur_container);
        assert(!should_free, "must have had more than one reference");
        // 如果容器是ContainerHowl类型, 则释放
        if (container_type(cur_container) == ContainerHowl) {
            G1ReleaseCardsets rel(this);
            // 遍历_buckets, 释放_buckets中的容器
            container_ptr<G1CardSetHowl>(cur_container)->iterate(rel, _config->num_buckets_in_howl());
        }
        return true;
    } else {
        // 粗化被其他线程打断, 返回失败
        if (new_container != FullCardSet) {
            assert(new_container != nullptr, "must not be");
            // new_container用不到了, 清理掉
            release_and_must_free_container(new_container);
        }
        return false;
    }
}
```

## 数组容器粗化

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

// 粗化并添加卡片索引
G1CardSet::ContainerPtr G1CardSet::create_coarsened_array_of_cards(uint card_in_region, bool within_howl) {
    uint8_t *data = nullptr;
    ContainerPtr new_container;
    if (within_howl) { // 从 ContainerArrayOfCards 粗化成 ContainerBitMap
        uint const size_in_bits = _config->max_cards_in_howl_bitmap();
        // 要在位图中设置成1的位
        uint container_offset = _config->howl_bitmap_offset(card_in_region);
        data = allocate_mem_object(ContainerBitMap);
        new(data) G1CardSetBitMap(container_offset, size_in_bits);
        new_container = make_container_ptr(data, ContainerBitMap);
    } else { // 从 ContainerArrayOfCards 粗化成 ContainerHowl
        data = allocate_mem_object(ContainerHowl);
        // 创建howl容器
        new(data) G1CardSetHowl(card_in_region, _config);
        new_container = make_container_ptr(data, ContainerHowl);
    }
    return new_container;
}

inline G1CardSetHowl::G1CardSetHowl(EntryCountType card_in_region, G1CardSetConfiguration *config) :
        G1CardSetContainer(),
        _num_entries((config->max_cards_in_array() + 1)) {
    EntryCountType num_buckets = config->num_buckets_in_howl();
    EntryCountType bucket = config->howl_bucket_index(card_in_region);
    for (uint i = 0; i < num_buckets; ++i) {
        // _buckets中的每个容器都从ContainerInlinePtr类型开始
        _buckets[i] = G1CardSetInlinePtr();
        if (i == bucket) {
            // 把当前卡片索引添加到容器中
            G1CardSetInlinePtr value(&_buckets[i], _buckets[i]);
            value.add(card_in_region, config->inline_ptr_bits_per_card(), config->max_cards_in_inline_ptr());
        }
    }
}
```
