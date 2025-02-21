# 遍历内联指针容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

template<class CardVisitor>
inline void G1CardSetInlinePtr::iterate(CardVisitor &found, uint bits_per_card) {
    // 获取指针中卡片索引的个数
    uint const num_cards = num_cards_in(_value);

    // 卡片索引掩码
    // 例如每个卡片索引的长度为14比特, 则card_mask的值如下:
    // 0000000000000000000000000000000000000000000000000011111111111111
    uintptr_t const card_mask = (1 << bits_per_card) - 1;

    // 找到第一个卡片索引的位置, 并把指针中低于它的比特移除
    // 比如_value是:
    // ...|card_index2|card_index1|card_index0|11100
    // 处理后的value是:
    // ...|card_index2|card_index1|card_index0
    uintptr_t value = ((uintptr_t) _value) >> card_pos_for(0, bits_per_card);
    for (uint cur_idx = 0; cur_idx < num_cards; cur_idx++) {
        // 把value中的卡片索引取出来, 交给found函数处理
        found(value & card_mask);
        // 移动到下一个卡片索引
        // 比如_value是:
        // ...|card_index2|card_index1|card_index0
        // 处理后的value是:
        // ...|card_index2|card_index1
        value >>= bits_per_card;
    }
}
```
