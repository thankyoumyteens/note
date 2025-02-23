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
