# 内联指针卡片模式容器

G1CardSetInlinePtr 类是一个用来把一些卡片索引编码到 ContainerPtr 指针中的辅助类。

指针(32 位或 64 位)被拆分为两个区域:

- 头部包含标识标记和已编码的卡片个数
- 数据区域存储卡片索引

头部(从最低位开始)以标识标记开始(固定为 `00` 的两位), 随后是 3 位的有效卡片索引个数。其余部分是数据区域, 卡片索引一个接一个地放置在递增的位位置上, 各个卡片索引仅使用足以表示覆盖整个范围(通常是一个分区)所需的位数。在指针的顶部可能存在未使用的空间。

## 示例

假设指针是 64 位, 分区大小是 8M(2^23), 每个卡片对应一个分区中的 512 字节, 则一个分区需要 2^14 个卡片(8MB / 512B = 2^23 / 2^9)。

那么就需要 14 位才能给每张卡片分配一个索引。所以最多可以在指针中编码 4 个卡片索引，使用 61 位(5 位头部 + 4 \* 14, 剩下 3 位不够编码一个卡片索引)。

```
高                                                    低
位                                                    位
+------+         +---------------+--------------+-----+
|unused|   ...   |  card_index1  | card_index0  |SSS00|
+------+         +---------------+--------------+-----+
```

## G1CardSetInlinePtr

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.hpp --- //

class G1CardSetInlinePtr : public StackObj {
    using ContainerPtr = G1CardSet::ContainerPtr;

    // 容器的地址(指向容器指针的指针)
    ContainerPtr volatile *_value_addr;
    // 容器(指向容器的指针)
    ContainerPtr _value;

    // 卡片索引个数
    static const uint SizeFieldLen = 3;
    // 标识
    static const uint SizeFieldPos = 2;
    // 指针头部大小是5位
    static const uint HeaderSize = G1CardSet::ContainerPtrHeaderSize + SizeFieldLen;

    // 指针的大小(32位或64位)
    static const uint BitsInValue = sizeof(ContainerPtr) * BitsPerByte;

    // 卡片索引个数的掩码
    // 0000000000000000000000000000000000000000000000000000000000011100
    static const uintptr_t SizeFieldMask = (((uint) 1 << SizeFieldLen) - 1) << SizeFieldPos;

    // 根据下标(从0开始)获取指定卡片索引在指针中的起始位置(从第几个比特开始)
    // 比如要获取card_index1的位置, 则传入 idx = 1, bits_per_card = 14, 返回 1 * 14 + 5 = 19
    static uint8_t card_pos_for(uint const idx, uint const bits_per_card) {
        return (idx * bits_per_card + HeaderSize);
    }

    // 获取指定下标的卡片索引
    // value: 内联指针卡片模式容器
    static uint card_at(ContainerPtr value, uint const idx, uint const bits_per_card) {
        uint8_t card_pos = card_pos_for(idx, bits_per_card);
        // 根据卡片索引的位置, 把它的值取出来
        uint result = ((uintptr_t) value >> card_pos) & (((uintptr_t) 1 << bits_per_card) - 1);
        return result;
    }

public:
    // 获取指针中卡片索引的个数
    // 例如个数为7时, 返回 111:
    // 第一步: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX111XX
    // 第二步: 00000000000000000000000000000000000000000000000000000000000111XX
    // 第三步: 0000000000000000000000000000000000000000000000000000000000000111
    static uint num_cards_in(ContainerPtr value) {
        return ((uintptr_t) value & SizeFieldMask) >> SizeFieldPos;
    }
};
```

## 查找

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

// 查找卡片索引是否在指针中, 如果存在则返回卡片索引在指针中的下标, 否则返回num_cards
// card_idx: 要查找的卡片索引
// bits_per_card: 每个卡片索引占用的比特数
// start_at: 从哪个下标开始查找
// num_cards: 查找几个卡片索引后停止查找
inline uint G1CardSetInlinePtr::find(uint card_idx, uint bits_per_card, uint start_at, uint num_cards) {
    assert(start_at < num_cards, "Precondition!");

    // 卡片索引掩码
    // 例如每个卡片索引的长度为14比特, 则card_mask的值如下:
    // 0000000000000000000000000000000000000000000000000011111111111111
    uintptr_t const card_mask = (1 << bits_per_card) - 1;
    // 找到start_at下标的位置, 并把指针中低于它的比特移除
    // 比如_value是:
    // ...|card_index2|card_index1|card_index0|11100
    // start_at是1, 处理后的value是:
    // ...|card_index2|card_index1
    uintptr_t value = ((uintptr_t) _value) >> card_pos_for(start_at, bits_per_card);

    // 遍历指针, 查找card_idx是否在指针中
    for (uint cur_idx = start_at; cur_idx < num_cards; cur_idx++) {
        if ((value & card_mask) == card_idx) {
            // 找到了, 返回下标
            return cur_idx;
        }
        // 准备遍历下一项
        // ...|card_index2|card_index1 --> ...|card_index2
        value >>= bits_per_card;
    }
    // 没找到, 返回num_cards
    return num_cards;
}
```

## 合并

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

// 向指针中添加卡片索引, 并返回新指针
// orig_value: 指针
// card_in_region: 卡片索引
// idx: card_in_region要添加到哪个下标(值为当前卡片索引总数, 即追加到末尾)
// bits_per_card: 每个卡片索引占多少比特
inline G1CardSetInlinePtr::ContainerPtr
G1CardSetInlinePtr::merge(ContainerPtr orig_value, uint card_in_region, uint idx, uint bits_per_card) {
    assert((idx & (SizeFieldMask >> SizeFieldPos)) == idx, "Index %u too large to fit into size field", idx);
    assert(card_in_region < ((uint) 1 << bits_per_card), "Card %u too large to fit into card value field",
           card_in_region);

    // 下标为idx的卡片索引在指针中的位置
    // 传进来的idx是指针中卡片索引的个数, 所以idx就是新卡片索引要添加到的位置:
    //        idx
    //         ⭣
    // ...unused|card_index2|card_index1|card_index0|01100
    uint8_t card_pos = card_pos_for(idx, bits_per_card);
    assert(card_pos + bits_per_card < BitsInValue, "Putting card at pos %u with %u bits would extend beyond pointer",
           card_pos, bits_per_card);

    // 下标为idx的卡片索引的掩码
    // 例如每个卡片索引的长度为14比特, (1 << bits_per_card) - 1:
    // 0000000000000000000000000000000000000000000000000011111111111111
    // card_pos = 9时, mask:
    // 0000000000000000000000000000000111111111111110000000000000000000
    uintptr_t mask = ((((uintptr_t) 1 << bits_per_card) - 1) << card_pos);
    // 新卡片索引要添加到的位置(在unused中)的比特需要全为0
    assert(((uintptr_t) orig_value & mask) == 0,
           "The bits in the new range should be empty; orig_value " PTR_FORMAT " mask " PTR_FORMAT, p2i(orig_value),
           mask);

    // (idx + 1) << SizeFieldPos: 计算添加card_in_region后, 指针中的卡片索引总数(idx时最后一个元素的下标, 它加一就是总数)
    // card_in_region << card_pos: 把card_in_region放到它在指针中应该在的位置
    // 例, 当前指针里有3个卡片索引, card_in_region是要添加的第4个
    // (idx + 1) << SizeFieldPos: 000 00000000000000 00000000000000 00000000000000 00000000000000 100 XX
    // card_in_region << card_pos: 000 XXXXXXXXXXXXXX 00000000000000 00000000000000 00000000000000 000 XX
    uintptr_t value = ((uintptr_t) (idx + 1) << SizeFieldPos) | ((uintptr_t) card_in_region << card_pos);
    // 把卡片索引总数和card_in_region写入指针
    // res: 000 XXXXXXXXXXXXXX XXXXXXXXXXXXXX XXXXXXXXXXXXXX XXXXXXXXXXXXXX 100 XX
    uintptr_t res = (((uintptr_t) orig_value & ~SizeFieldMask) | value);
    return (ContainerPtr) res;
}
```

## 添加

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

inline G1AddCardResult G1CardSetInlinePtr::add(uint card_idx, uint bits_per_card, uint max_cards_in_inline_ptr) {
    assert(_value_addr != nullptr, "No value address available, cannot add to set.");

    uint cur_idx = 0;
    while (true) {
        // 获取指针中卡片索引的个数
        uint num_cards = num_cards_in(_value);
        if (num_cards > 0) {
            // 查找卡片索引是否在指针中
            cur_idx = find(card_idx, bits_per_card, cur_idx, num_cards);
        }
        if (cur_idx < num_cards) {
            // 卡片索引已经在指针中, 返回Found
            return Found;
        }
        if (num_cards >= max_cards_in_inline_ptr) {
            // 指针空间不足
            return Overflow;
        }
        // 向指针中添加卡片索引, 并返回新指针
        ContainerPtr new_value = merge(_value, card_idx, num_cards, bits_per_card);
        // 把_value更新为新的指针
        ContainerPtr old_value = Atomic::cmpxchg(_value_addr, _value, new_value, memory_order_relaxed);
        if (_value == old_value) {
            // 成功
            return Added;
        }
        // 把_value重置为原来的指针, 等下一轮循环重试
        _value = old_value;
        if (G1CardSet::container_type(_value) != G1CardSet::ContainerInlinePtr) {
            return Overflow;
        }
    }
}
```
