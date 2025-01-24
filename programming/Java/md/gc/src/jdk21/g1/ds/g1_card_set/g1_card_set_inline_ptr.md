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

    // 根据下标(从0开始)获取指定卡片索引在指针中的位置(从第几个比特开始)
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
};
```
